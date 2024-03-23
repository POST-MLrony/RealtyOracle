import pandas as pd
from .utils import haversine
from .preprocessing import (
    replace_rare_categories,
    fill_missing_coordinates,
    find_nearest_neighbors,
    fill_missing_values,
    find_nearest_metro,
    label_encode_categorical,
    trim_df_by_quantiles,
    filter_outliers_with_isolation_forest,
    replace_districts_with_nearest_neighbors,
)
import datetime
from server.api.metro_info import get_metro_info_by_city, get_coordinates_by_city
from typing import List, Any
import datetime
from sklearn.model_selection import train_test_split


def preprocess_pipeline(
    df: pd.DataFrame,
    city: str,
    categories: List[str],
    replace_value: Any = 0,
    need_quantiles_trim: bool = True,
    need_isolation_trim: bool = True,
) -> pd.DataFrame:
    """Пайплайн для предобработки данных.

    Args:
        df (pd.DataFrame): DataFrame с данными.
        city (str): Название города.
        categories (List[str]): Список названий категориальных столбцов.
        replace_value (Any, optional): Значение для замены редких категорий.
            По умолчанию установлено значение 0.
        need_quantiles_trim (bool, optional): Флаг для обрезки данных по квантилям.
            По умолчанию установлено значение True.
        need_isolation_trim (bool, optional): Флаг для обрезки данных с помощью изоляционного леса.
            По умолчанию установлено значение True.

    Returns:
        pd.DataFrame: DataFrame с предобработанными данными.

    Description:
        Этот пайплайн выполняет предобработку данных, включая замену редких категорий,
        заполнение пропущенных координат, поиск ближайших соседей, вычисление расстояний
        до метро и центра города, а также обрезку данных по квантилям и с использованием изоляционного леса.

    """
    df["lo"] = df["lo"].astype(float)
    df["la"] = df["la"].astype(float)
    df["price"] = df["price"].astype(float)
    df["square"] = df["square"].astype(float)
    df = replace_rare_categories(df, "meta.district", replace_value, 10)
    df = df[
        ~((df["meta.district"] == replace_value) & (df["lo"].isna() | df["la"].isna()))
    ].reset_index(drop=True)
    df["meta.district"] = df["meta.district"].astype(str)
    df = fill_missing_coordinates(df, "meta.district", "la", "lo")
    df = find_nearest_neighbors(df, "la", "lo", n_neighbors=21)
    df["building_year"] = df.apply(
        lambda row: fill_missing_values(
            df, row, row["nearest_neighbors_haversine_no_self"], "building_year"
        ),
        axis=1,
    )
    df["wall_id"] = df.apply(
        lambda row: fill_missing_values(
            df, row, row["nearest_neighbors_haversine_no_self"], "wall_id"
        ),
        axis=1,
    )
    df["keep"] = df.apply(
        lambda row: fill_missing_values(
            df, row, row["nearest_neighbors_haversine_no_self"], "keep"
        ),
        axis=1,
    )
    metro = get_metro_info_by_city(city)
    df["nearest_metro"], df["dist_to_metro"] = zip(
        *df.apply(lambda row: find_nearest_metro(row["la"], row["lo"], metro), axis=1)
    )
    la_centre, lo_centre = get_coordinates_by_city(city)
    df["distance_to_centre"] = df.apply(
        lambda row: haversine(la_centre, lo_centre, row["la"], row["lo"]), axis=1
    )
    df["building_year"] = datetime.datetime.now().year - df["building_year"].astype(int)
    df["wall_id"] = df["wall_id"].astype(int)
    df.drop(
        ["lo", "la", "id", "nearest_neighbors_haversine_no_self"], axis=1, inplace=True
    )
    df[categories] = df[categories].astype("category")
    if need_quantiles_trim:
        df = trim_df_by_quantiles(df, "price")
    if need_isolation_trim:
        isolation_df = label_encode_categorical(df, categories)
        df = filter_outliers_with_isolation_forest(df, isolation_df)
    return df


def train_pipeline(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_val: pd.DataFrame,
    y_val: pd.Series,
    categories: List[str],
    model_type: str = "catboost",
    loss: str = "RMSE",
) -> Any:
    """Обучает модель машинного обучения.

    Args:
        x_train (pd.DataFrame): DataFrame с признаками обучающей выборки.
        y_train (pd.Series): Столбец с целевой переменной обучающей выборки.
        x_val (pd.DataFrame): DataFrame с признаками валидационной выборки.
        y_val (pd.Series): Столбец с целевой переменной валидационной выборки.
        categories (List[str]): Список названий категориальных признаков.
        model_type (str, optional): Тип модели. По умолчанию "catboost".
        loss (str, optional): Функция потерь для модели. По умолчанию "RMSE".

    Returns:
        CatBoostRegressor: Обученная модель машинного обучения.

    Description:
        Эта функция обучает модель машинного обучения с использованием
        выбранных признаков и целевой переменной.

    """
    if model_type == "catboost":
        from catboost import CatBoostRegressor

        model = CatBoostRegressor(
            cat_features=categories, verbose=100, iterations=10000, loss_function=loss
        )
    model.fit(x_train, y_train, eval_set=(x_val, y_val), use_best_model=True)
    return model


def split_pipeline(
    df: pd.DataFrame,
    train_size: float,
    test_size: float,
    y_column: str,
    random_state: int = 0,
) -> tuple:
    """Разбивает данные на обучающую и тестовую выборки.

    Args:
        df (pd.DataFrame): DataFrame с данными.
        train_size (float): Размер обучающей выборки.
        test_size (float): Размер тестовой выборки.
        y_column (str): Название столбца с целевой переменной.
        random_state (int, optional): Зерно для случайной генерации. По умолчанию 0.

    Returns:
        tuple: Кортеж, содержащий x_train, x_test, y_train, y_test.

    Description:
        Эта функция разбивает данные на обучающую и тестовую выборки
        с заданными размерами и целевой переменной.

    """
    x_train, x_test, y_train, y_test = train_test_split(
        df.drop(y_column, axis=1),
        df[y_column],
        train_size=train_size,
        test_size=test_size,
        random_state=random_state,
    )
    return x_train, x_test, y_train, y_test

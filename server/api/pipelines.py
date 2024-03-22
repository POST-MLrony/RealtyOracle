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
from typing import List
import datetime
from sklearn.model_selection import train_test_split


def preprocess_pipeline(
    df: pd.DataFrame,
    city: str,
    categories: List[str],
    replace_value=0,
    need_quantiles_trim: bool = True,
    need_isolation_trim: bool = True,
) -> pd.DataFrame:
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
    x_train, y_train, x_val, y_val, categories, model_type: str = "catboost", loss: str = "RMSE"
):
    if model_type == "catboost":
        from catboost import CatBoostRegressor

        model = CatBoostRegressor(
            cat_features=categories, verbose=100, iterations=10000, loss_function= loss
        )
    model.fit(x_train, y_train, eval_set=(x_val, y_val), use_best_model=True)
    return model



def split_pipeline(df, train_size, test_size, y_column: str, random_state: int = 0):
    x_train, x_test, y_train, y_test = train_test_split(
        df.drop(y_column, axis=1),
        df[y_column],
        train_size=train_size,
        test_size=test_size,
        random_state=random_state,
    )
    return x_train, x_test, y_train, y_test

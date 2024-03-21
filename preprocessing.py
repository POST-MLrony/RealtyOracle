import pandas as pd
from utils import haversine
from typing import Any
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest


def replace_rare_categories(
    df: pd.DataFrame,
    column: str,
    replace_value: Any = "Other",
    rare_threshold: int = 10,
):
    counts = df[column].value_counts()
    replace_dict = counts[counts < rare_threshold].to_dict()
    df[column] = df[column].apply(lambda x: replace_value if x in replace_dict else x)
    return df


def fill_missing_values(df, row, neighbors, column):
    if pd.isna(row[column]):
        neighbor_values = df.loc[neighbors, column]
        if not neighbor_values.empty:
            most_common_value = neighbor_values.mode()
            if not most_common_value.empty:
                return most_common_value.iloc[0]
            else:
                print(
                    f"Не найдено общего значения для столбца '{column}' с соседями: {neighbors}"
                )
        else:
            print(
                f"Не найдено общего значения для столбца '{column}' с соседями: {neighbors}"
            )
    return row[column]


def find_nearest_metro(building_lat, building_lon, metro_stations):
    """
    Находит ближайшую станцию метро к заданному зданию.

    Аргументы:
    building_lat (float): Широта здания.
    building_lon (float): Долгота здания.
    metro_stations (list): Список словарей с информацией о станциях метро.

    Возвращает:
    str: Название ближайшей станции метро.
    """
    nearest_metro = None
    min_distance = float("inf")
    for station in metro_stations:
        metro_lat = station["geo_lat"]
        metro_lon = station["geo_lon"]
        distance = haversine(building_lat, building_lon, metro_lat, metro_lon)
        if distance < min_distance:
            min_distance = distance
            nearest_metro = station["value"]

    return nearest_metro, min_distance


def fill_missing_coordinates(
    df: pd.DataFrame, district_column: str, lat_column: str, lon_column: str
) -> pd.DataFrame:
    district_means = df.groupby(district_column)[[lat_column, lon_column]].mean()

    for district, mean_values in district_means.iterrows():
        df.loc[
            (df[district_column] == district) & (df[lat_column].isnull()), lat_column
        ] = mean_values[lat_column]
        df.loc[
            (df[district_column] == district) & (df[lon_column].isnull()), lon_column
        ] = mean_values[lon_column]
    return df


def find_nearest_neighbors(
    df: pd.DataFrame, lat_column: str, lon_column: str, n_neighbors: int = 11
) -> pd.DataFrame:
    coords_in_radians = np.radians(df[[lat_column, lon_column]])
    nn_haversine = NearestNeighbors(n_neighbors=n_neighbors, metric="haversine")
    nn_haversine.fit(coords_in_radians)
    _, indices_haversine = nn_haversine.kneighbors(coords_in_radians)
    indices_haversine_no_self = [list(sorted(ind)[1:]) for ind in indices_haversine]
    df["nearest_neighbors_haversine_no_self"] = indices_haversine_no_self
    return df


def label_encode_categorical(
    df: pd.DataFrame, categorical_columns: list
) -> pd.DataFrame:
    non_categorical_columns = df.columns.difference(categorical_columns)
    isolation_df = df[non_categorical_columns].copy()
    for column in categorical_columns:
        label_encoder = LabelEncoder()
        isolation_df[column] = label_encoder.fit_transform(df[column])
    return isolation_df


def trim_df_by_quantiles(
    df: pd.DataFrame,
    column: str,
    low_quantile: float = 0.05,
    high_quantile: float = 0.95,
) -> pd.DataFrame:
    low, high = df[column].quantile([low_quantile, high_quantile])
    trimmed_df = df.query(
        "{low}<{column}<{high}".format(low=low, high=high, column=column)
    )
    return trimmed_df


def filter_outliers_with_isolation_forest(df: pd.DataFrame, random_state: int = 0):
    clf = IsolationForest(random_state=random_state)
    clf.fit(df)
    outliers = clf.predict(df)
    filtered_df = df[outliers == 1]
    return filtered_df


def replace_districts_with_nearest_neighbors(
    df: pd.DataFrame,
    district_column: str,
    lat_column: str,
    lon_column: str,
    replace_value: Any = 0,
):
    df["lo_rad"] = np.radians(df[lon_column])
    df["la_rad"] = np.radians(df[lat_column])
    
    is_other = df[district_column] == replace_value
    not_other = ~is_other
    
    locations_not_other = df.loc[not_other, ["lo_rad", "la_rad"]]
    
    nn = NearestNeighbors(n_neighbors=1, metric="haversine")
    nn.fit(locations_not_other)
    
    locations_other = df.loc[is_other, ["lo_rad", "la_rad"]]
    nearest_neighbors_indices = nn.kneighbors(locations_other, return_distance=False)
    nearest_districts = df.loc[not_other].iloc[nearest_neighbors_indices.flatten()][
        district_column
    ]
    df.loc[is_other, district_column] = nearest_districts.values
    df.drop(columns=["lo_rad", "la_rad"], inplace=True)
    return df

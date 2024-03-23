import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import json

def excel2dict(path: str) -> dict:
    df = pd.read_excel(path)
    return df.to_dict(orient="records")


def haversine(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками на глобусе по координатам широты и долготы.

    Аргументы:
    lat1 (float): Широта первой точки в градусах.
    lon1 (float): Долгота первой точки в градусах.
    lat2 (float): Широта второй точки в градусах.
    lon2 (float): Долгота второй точки в градусах.

    Возвращает:
    float: Расстояние между двумя точками в километрах.

    Пример использования:
    >>> haversine(52.2296756, 21.0122287, 52.406374, 16.9251681)
    279.35290160386563
    """
    # Радиус Земли в километрах
    R = 6371.0

    # Преобразование координат в радианы
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Разница между широтами и долготами
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула гаверсинусов
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Расстояние между точками
    distance = R * c

    return distance


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
    min_distance = float('inf')

    for station in metro_stations:
        metro_lat = station['geo_lat']
        metro_lon = station['geo_lon']
        distance = haversine(building_lat, building_lon, metro_lat, metro_lon)
        if distance < min_distance:
            min_distance = distance
            nearest_metro = station['value']

    return nearest_metro


def open_json(path: str) -> dict:   
    with open(path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    df = pd.json_normalize(json_data)
    return df
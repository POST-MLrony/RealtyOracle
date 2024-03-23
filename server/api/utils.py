import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import json
import shap
import io
import base64
import matplotlib.pyplot as plt


def excel2dict(path: str) -> dict:
    """Преобразует данные из Excel в словарь.

    Args:
        path (str): Путь к файлу Excel.

    Returns:
        dict: Словарь, содержащий данные из файла Excel.

    Description:
        Эта функция считывает данные из файла Excel и преобразует их в словарь.

    """
    df = pd.read_excel(path)
    return df.to_dict(orient="records")


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Вычисляет расстояние между двумя точками на глобусе по координатам широты и долготы.

    Args:
        lat1 (float): Широта первой точки в градусах.
        lon1 (float): Долгота первой точки в градусах.
        lat2 (float): Широта второй точки в градусах.
        lon2 (float): Долгота второй точки в градусах.

    Returns:
        float: Расстояние между двумя точками в километрах.

    Description:
        Эта функция вычисляет расстояние между двумя точками на глобусе
        по координатам широты и долготы с использованием формулы гаверсинусов.

    Example:
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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Расстояние между точками
    distance = R * c

    return distance


def find_nearest_metro(
    building_lat: float, building_lon: float, metro_stations: list
) -> str:
    """Находит ближайшую станцию метро к заданному зданию.

    Args:
        building_lat (float): Широта здания.
        building_lon (float): Долгота здания.
        metro_stations (list): Список словарей с информацией о станциях метро.

    Returns:
        str: Название ближайшей станции метро.

    Description:
        Эта функция находит ближайшую станцию метро к заданному зданию
        из списка станций метро, используя расстояние между координатами здания
        и координатами каждой станции метро.
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

    return nearest_metro


def open_json(path: str) -> dict:
    """Открывает JSON-файл и возвращает его содержимое в виде словаря.

    Args:
        path (str): Путь к JSON-файлу.

    Returns:
        dict: Содержимое JSON-файла в виде словаря.

    Description:
        Эта функция открывает указанный JSON-файл и возвращает его содержимое в виде словаря.

    """
    with open(path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    df = pd.json_normalize(json_data)
    return df


def generate_shap_waterfall(data, explainer):
    """Генерирует изображение водопада SHAP значений.

    Args:
        data: Данные для расчета SHAP значений.
        explainer: Объект, используемый для расчета SHAP значений.

    Returns:
        bytes: Изображение водопада SHAP значений в формате PNG в виде байтов.

    Description:
        Эта функция генерирует изображение водопада SHAP значений для данных, используя
        объект explainer для расчета SHAP значений. Изображение сохраняется в формате PNG
        и возвращается в виде байтов.

    """
    shap_values = explainer(data)
    plt.figure()
    shap.plots.waterfall(shap_values[0], show=False)
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    return buffer.getvalue()

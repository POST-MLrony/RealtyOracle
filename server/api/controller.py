from fastapi import APIRouter, Request
from .models import Town, Moscow
from .metro_info import get_metro_info_by_city, get_coordinates_by_city
from .preprocessing import find_nearest_metro
from .utils import haversine, generate_shap_waterfall
from .schemas import PredictionResponse
import pandas as pd
import shap
import io
import base64
import matplotlib.pyplot as plt

controller = APIRouter()


@controller.post("/nn/")
async def nn(town: Town, request: Request) -> PredictionResponse:
    """Обрабатывает POST-запросы по пути '/nn/'.

    Args:
        town (Town): Объект, содержащий информацию о недвижимости в Нижнем Новгороде.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Description:
        Данная функция используется для получения предсказаний по недвижимости в Нижнем Новгороде на основе переданных данных.
        Шаги, выполненные внутри функции:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Нижний Новгород")
    la = town.la
    lo = town.lo
    la_centre, lo_centre = get_coordinates_by_city("Нижний Новгород")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)
    data = {
        "meta.district": town.district,
        "floors": town.floors,
        "bedrooms_cnt": town.bedrooms_cnt,
        "euro": town.euro,
        "wall_id": town.wall_id,
        "rooms": town.rooms,
        "type": town.type,
        "floor": town.floor,
        "balcon": town.balcon,
        "studio": town.studio,
        "square": town.square,
        "building_year": 2024 - town.building_year,
        "keep": town.keep,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    print(town.euro, town.mortgage, town.studio)
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_nn.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_nn,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )


@controller.post("/spb/")
async def spb(town: Town, request: Request) -> PredictionResponse:
    """Обрабатывает POST-запросы по пути '/spb/'.

    Args:
        town (Town): Объект, содержащий информацию о недвижимости в Санкт-Петербурге.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Description:
        Данная функция используется для получения предсказаний по недвижимости в Санкт-Петербурге на основе переданных данных.
        Шаги, выполненные внутри функции:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Санкт-Петербург")
    la = town.la
    lo = town.lo
    la_centre, lo_centre = get_coordinates_by_city("Санкт-Петербург")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)

    data = {
        "meta.district": town.district,
        "floors": town.floors,
        "bedrooms_cnt": town.bedrooms_cnt,
        "euro": town.euro,
        "wall_id": town.wall_id,
        "rooms": town.rooms,
        "type": town.type,
        "floor": town.floor,
        "balcon": town.balcon,
        "studio": town.studio,
        "square": town.square,
        "building_year": 2024 - town.building_year,
        "keep": town.keep,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_spb.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_spb,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )


@controller.post("/novosibirsk/")
async def novosibirsk(town: Town, request: Request) -> PredictionResponse:
    """Этот метод обрабатывает POST-запросы по пути '/novosibirsk/'.

    Args:
        town (Town): Объект, содержащий информацию о недвижимости в Новосибирске.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Raises:
        None

    Description:
        Этот метод используется для получения предсказаний по недвижимости в Новосибирске на основе переданных данных.
        Внутри метода выполняются следующие действия:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Новосибирск")
    la = town.la
    lo = town.lo
    la_centre, lo_centre = get_coordinates_by_city("Новосибирск")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)

    data = {
        "meta.district": town.district,
        "floors": town.floors,
        "bedrooms_cnt": town.bedrooms_cnt,
        "euro": town.euro,
        "wall_id": town.wall_id,
        "rooms": town.rooms,
        "type": town.type,
        "floor": town.floor,
        "balcon": town.balcon,
        "studio": town.studio,
        "square": town.square,
        "building_year": 2024 - town.building_year,
        "keep": town.keep,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_novosibirsk.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_novosibirsk,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )


@controller.post("/kazan/")
async def kazan(town: Town, request: Request) -> PredictionResponse:
    """Этот метод обрабатывает POST-запросы по пути '/kazan/'.

    Args:
        town (Town): Объект, содержащий информацию о недвижимости в Казани.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Raises:
        None

    Description:
        Этот метод используется для получения предсказаний по недвижимости в Казани на основе переданных данных.
        Внутри метода выполняются следующие действия:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Казань")
    la = town.la
    lo = town.lo
    la_centre, lo_centre = get_coordinates_by_city("Казань")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)

    data = {
        "meta.district": town.district,
        "floors": town.floors,
        "bedrooms_cnt": town.bedrooms_cnt,
        "euro": town.euro,
        "wall_id": town.wall_id,
        "rooms": town.rooms,
        "type": town.type,
        "floor": town.floor,
        "balcon": town.balcon,
        "studio": town.studio,
        "square": town.square,
        "building_year": 2024 - town.building_year,
        "keep": town.keep,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_kazan.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_kazan,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )


@controller.post("/ekb/")
async def ekb(town: Town, request: Request) -> PredictionResponse:
    """Этот метод обрабатывает POST-запросы по пути '/ekb/'.

    Args:
        town (Town): Объект, содержащий информацию о недвижимости в Екатеринбурге.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Raises:
        None

    Description:
        Этот метод используется для получения предсказаний по недвижимости в Екатеринбурге на основе переданных данных.
        Внутри метода выполняются следующие действия:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Екатеринбург")
    la = town.la
    lo = town.lo
    la_centre, lo_centre = get_coordinates_by_city("Екатеринбург")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)

    data = {
        "meta.district": town.district,
        "floors": town.floors,
        "bedrooms_cnt": town.bedrooms_cnt,
        "euro": town.euro,
        "wall_id": town.wall_id,
        "rooms": town.rooms,
        "type": town.type,
        "floor": town.floor,
        "balcon": town.balcon,
        "studio": town.studio,
        "square": town.square,
        "building_year": 2024 - town.building_year,
        "keep": town.keep,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_ekb.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_ekb,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )


@controller.post("/msk/")
async def msk(msk: Moscow, request: Request) -> PredictionResponse:
    """Этот метод обрабатывает POST-запросы по пути '/msk/'.

    Args:
        msk (Moscow): Объект, содержащий информацию о недвижимости в Москве.
        request (Request): Объект запроса.

    Returns:
        PredictionResponse: Объект, содержащий предсказание и дополнительную информацию.

    Raises:
        None

    Description:
        Этот метод используется для получения предсказаний по недвижимости в Москве на основе переданных данных.
        Внутри метода выполняются следующие действия:
        - Получение информации о ближайшем метро.
        - Вычисление расстояния до центра города и до ближайшей станции метро.
        - Подготовка данных для передачи модели для предсказания.
        - Получение предсказания от модели.
        - Генерация изображения водопада SHAP для интерпретации предсказания.
        - Возврат объекта PredictionResponse с предсказанием и изображением водопада SHAP.

    """
    metro = get_metro_info_by_city("Москва")
    la = msk.la
    lo = msk.lo
    la_centre, lo_centre = get_coordinates_by_city("Москва")
    nearest_metro, min_distance = find_nearest_metro(la, lo, metro)
    dist_to_centre = haversine(la, lo, la_centre, lo_centre)
    data = {
        "meta.district": msk.district,
        "floors": msk.floors,
        "wall_id": msk.wall_id,
        "rooms": msk.rooms,
        "type": msk.type,
        "floor": msk.floor,
        "class": msk.building_class,
        "square": msk.square,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "distance_to_centre": dist_to_centre,
    }
    data = pd.DataFrame(data, index=[1])
    cat_ind = ["meta.district", "wall_id", "type", "class", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    y_pred = request.app.state.model_msk.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_msk,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return PredictionResponse(
        predict=float(y_pred),
        nearest_metro=str(nearest_metro),
        dist_to_metro=float(min_distance),
        dist_to_centre=float(dist_to_centre),
        shap_waterfall_image=shap_image_base64,
    )

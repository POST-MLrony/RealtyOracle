from fastapi import APIRouter, Request, UploadFile, File, FastAPI
from .models import Town
from .metro_info import get_metro_info_by_city, get_coordinates_by_city
from .preprocessing import find_nearest_metro
from .utils import haversine
from catboost import CatBoostRegressor, Pool
import pandas as pd
import shap
import io
import base64
import matplotlib.pyplot as plt

controller = APIRouter()


@controller.post("/receive_data/")
async def receive_data(town: Town):
    print(town)
    return {"message": "Data received successfully"}


def generate_shap_waterfall(data, explainer):
    shap_values = explainer(data)
    plt.figure()
    shap.plots.waterfall(shap_values[0], show=False)
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    return buffer.getvalue()


@controller.post("/nn/")
async def receive_data(town: Town, request: Request):
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
    cat_ind = ["meta.district", "wall_id", "type", "balcon", "keep", "nearest_metro"]
    data[cat_ind] = data[cat_ind].astype("category")
    feature_names = [
        "Площадь",
        "Количество этажей",
        "Количество спален",
        "Евро ремонт",
        "Тип стен",
        "Количество Комнат",
        "Тип объекта",
        "Этаж",
        "Тип балкона",
        "Студия",
        "Площадь",
        "Возраст здания",
        "Вид ремонта",
        "Ближайшее метро",
        "Расстояние до метро",
        "Расстояние до центра",
    ]
    y_pred = request.app.state.model_nn.predict(data)
    explainer = shap.TreeExplainer(
        request.app.state.model_nn,
    )
    shap_image_bytes = generate_shap_waterfall(data, explainer)
    shap_image_base64 = base64.b64encode(shap_image_bytes).decode("utf-8")
    return {
        "predict": float(y_pred),
        "nearest_metro": str(nearest_metro),
        "dist_to_metro": float(min_distance),
        "dist_to_centre": float(dist_to_centre),
        "shap_waterfall_image": shap_image_base64,
    }

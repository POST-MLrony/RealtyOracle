from fastapi import APIRouter, Request, UploadFile, File, FastAPI
from .models import Town
from .metro_info import get_metro_info_by_city, get_coordinates_by_city
from .preprocessing import find_nearest_metro
from .utils import haversine
from catboost import CatBoostRegressor
import pandas as pd

controller = APIRouter()


@controller.post("/receive_data/")
async def receive_data(town: Town):
    print(town)
    return {"message": "Data received successfully"}


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
    data = pd.Series(data)
    y_pred = request.app.state.model_nn.predict(data)
    print(y_pred)
    return {
        "predict": y_pred,
        "nearest_metro": nearest_metro,
        "dist_to_metro": min_distance,
        "dist_to_centre": dist_to_centre,
    }

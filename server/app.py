from fastapi import FastAPI
import db as database
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from client import client
from catboost import CatBoostRegressor

async def lifespan(app: FastAPI):
    """Подгрузка данных при старте приложения (подгрузка моделей)"""
    model_nn = CatBoostRegressor()
    model_nn.load_model("static/models/model_nn.cbm")
    app.state.model_nn = model_nn
    print("ML model loaded")
    yield
    # При завершении работы приложения
    del app.state.model_nn
    print("ML model unloaded")


# Создание экземпляра FastAPI
app = FastAPI(lifespan=lifespan)

# Подключение роутера из модуля api.controller с префиксом и тегом
from api.controller import controller

app.include_router(controller, prefix='/api/v1', tags=['Сюда лезь!)'])

# Подключение роутера из модуля client с тегом
from client import client

app.include_router(client, tags=['Сюда не лезь!'])

# Монтирование статических файлов из директории "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Добавление middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

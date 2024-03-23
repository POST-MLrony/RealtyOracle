from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from catboost import CatBoostRegressor

# Подключение роутера из модуля client с тегом
from client import client

# Подключение роутера из модуля api.controller с префиксом и тегом
from api.controller import controller


async def lifespan(app: FastAPI):
    """Подгрузка данных при старте приложения (подгрузка моделей)"""
    model_nn = CatBoostRegressor()
    model_nn.load_model("static/models/nn.cbm")
    app.state.model_nn = model_nn
    model_ekb = CatBoostRegressor()
    model_ekb.load_model("static/models/ekb.cbm")
    app.state.model_ekb = model_ekb
    model_novosibirsk = CatBoostRegressor()
    model_novosibirsk.load_model("static/models/novosibirsk.cbm")
    app.state.model_novosibirsk = model_novosibirsk
    model_spb = CatBoostRegressor()
    model_spb.load_model("static/models/spb.cbm")
    app.state.model_spb = model_spb
    model_kazan = CatBoostRegressor()
    model_kazan.load_model("static/models/kazan.cbm")
    app.state.model_kazan = model_kazan
    model_msk = CatBoostRegressor()
    model_msk.load_model("static/models/msk.cbm")
    app.state.model_msk = model_msk
    print("ML model loaded")
    yield
    # При завершении работы приложения
    del app.state.model_nn
    print("ML model unloaded")


# Создание экземпляра FastAPI
app = FastAPI(lifespan=lifespan)



app.include_router(controller, prefix='/api/v1', tags=['Сюда лезь!)'])



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

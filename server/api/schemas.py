from pydantic import BaseModel


class PredictionResponse(BaseModel):
    """Модель для представления ответа предсказания.

    Attributes:
        predict (float): Предсказанное значение.
        nearest_metro (str): Название ближайшей станции метро.
        dist_to_metro (float): Расстояние до ближайшей станции метро (в километрах).
        dist_to_centre (float): Расстояние до центра города (в километрах).
        shap_waterfall_image (str): Строка, представляющая изображение водопада SHAP.
    """

    predict: float
    nearest_metro: str
    dist_to_metro: float
    dist_to_centre: float
    shap_waterfall_image: str

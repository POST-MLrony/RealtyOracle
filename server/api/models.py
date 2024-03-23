from pydantic import BaseModel


class Town(BaseModel):
    """Модель для представления информации о городской недвижимости.

    Args:
        square (float): Площадь недвижимости в квадратных метрах.
        rooms (int): Количество комнат.
        building_year (int): Год постройки здания.
        keep (str): Состояние недвижимости.
        floors (int): Общее количество этажей в здании.
        type (str): Тип недвижимости.
        floor (int): Этаж, на котором расположена недвижимость.
        balcon (str): Тип балкона.
        bedrooms_cnt (int): Количество спален.
        studio (bool): Наличие студии.
        mortgage (bool): Возможность ипотеки.
        lo (float): Долгота координаты расположения недвижимости.
        la (float): Широта координаты расположения недвижимости.
        wall_id (str): Тип стен.
        euro (bool): Евроремонт.
        district (str): Район города, в котором расположена недвижимость.
    """
    square: float
    rooms: int
    building_year: int
    keep: str
    floors: int
    type: str
    floor: int
    balcon: str
    bedrooms_cnt: int
    studio: bool
    mortgage: bool
    lo: float
    la: float
    wall_id: str
    euro: bool
    district: str


class Moscow(BaseModel):
    """Модель для представления информации о недвижимости в Москве.

    Args:
        square (float): Площадь недвижимости в квадратных метрах.
        rooms (int): Количество комнат.
        floors (int): Общее количество этажей в здании.
        type (str): Тип недвижимости.
        floor (int): Этаж, на котором расположена недвижимость.
        building_class (str): Класс здания.
        lo (float): Долгота координаты расположения недвижимости.
        la (float): Широта координаты расположения недвижимости.
        wall_id (str): Тип стен.
        district (str): Район города, в котором расположена недвижимость.
    """
    square: float
    rooms: int
    floors: int
    type: str
    floor: int
    building_class: str
    lo: float
    la: float
    wall_id: str
    district: str

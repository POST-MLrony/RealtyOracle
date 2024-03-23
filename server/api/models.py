from pydantic import BaseModel

class Town(BaseModel):
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
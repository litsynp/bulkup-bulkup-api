from datetime import datetime
from ninja import Schema


class DiaryView(Schema):
    id: int
    weight: float
    breakfast: str
    lunch: str
    dinner: str
    other_meals: str
    content: str
    created_at: datetime


class DiaryCreateRequest(Schema):
    weight: float
    breakfast: str
    lunch: str
    dinner: str
    other_meals: str
    content: str


class DiaryUpdateRequest(Schema):
    weight: float
    breakfast: str
    lunch: str
    dinner: str
    other_meals: str
    content: str

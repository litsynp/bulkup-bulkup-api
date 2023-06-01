from datetime import datetime
from ninja import ModelSchema, Schema

from diary.models import Diary, Image


class ImageView(ModelSchema):
    class Config:
        model = Image
        model_fields = [
            "id",
            "url",
            "created_at",
        ]


class DiaryView(ModelSchema):
    images: list[ImageView]

    class Config:
        model = Diary
        model_fields = [
            "id",
            "weight",
            "breakfast",
            "lunch",
            "dinner",
            "other_meals",
            "content",
            "created_at",
        ]

    @staticmethod
    def resolve_images(diary: Diary):
        return [
            ImageView.from_orm(image)
            for image in Image.objects.filter(diaryimage__diary=diary).order_by(
                "diaryimage__order"
            )
        ]


class DiaryCreateRequest(Schema):
    weight: float
    breakfast: str
    lunch: str
    dinner: str
    other_meals: str
    content: str
    image_ids: list


class DiaryUpdateRequest(Schema):
    weight: float
    breakfast: str
    lunch: str
    dinner: str
    other_meals: str
    content: str
    image_ids: list

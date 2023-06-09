from datetime import datetime, timedelta
from typing import List
from django.shortcuts import get_object_or_404
from ninja import File
from ninja.files import UploadedFile
from ninja.errors import HttpError
from ninja.pagination import paginate

from app.api import api
from diary.models import Diary, DiaryImage, Image
from diary.views import DiaryCreateRequest, DiaryUpdateRequest, DiaryView, ImageView


@api.get("/diaries", response=List[DiaryView])
@paginate
def list_diaries(request):
    return Diary.objects.all()


@api.get("/diaries/stats")
def get_diary_stats(request):
    weekly_diaries = reversed(Diary.objects.filter().order_by("-created_at")[0:7])

    return {
        'type': "seven_days",
        'diaries': list(map(lambda diary: {
            'id': diary.id,
            'weight': diary.weight,
            'created_at': diary.created_at
        }, weekly_diaries))
    }


@api.get("/diaries/{diary_id}", response=DiaryView)
def retrieve_diary(request, diary_id: int):
    try:
        return Diary.objects.get(id=diary_id)
    except Diary.DoesNotExist:
        raise HttpError(404, "Diary not found")


@api.post("/diaries")
def create_diary(request, payload: DiaryCreateRequest):
    diary_payload = payload.dict()
    diary_payload.pop("image_ids")
    diary = Diary.objects.create(**diary_payload)

    diary_images = []
    for image_id in payload.image_ids:
        diary_images.append(Image.objects.get(id=image_id))

    DiaryImage.objects.bulk_create(
        [
            DiaryImage(diary=diary, image=image, order=index + 1)
            for index, image in enumerate(diary_images)
        ]
    )

    return {"id": diary.id}


@api.put("/diaries/{diary_id}")
def update_diary(request, diary_id: int, payload: DiaryUpdateRequest):
    diary_payload = payload.dict()
    diary_payload.pop("image_ids")

    diary = get_object_or_404(Diary, id=diary_id)
    for attr, value in diary_payload.items():
        setattr(diary, attr, value)
    diary.save()

    existing_diary_images = diary.diaryimage_set.all()
    existing_diary_images.delete()

    diary_images = []
    for image_id in payload.image_ids:
        diary_images.append(Image.objects.get(id=image_id))

    DiaryImage.objects.bulk_create(
        [
            DiaryImage(diary=diary, image=image, order=index + 1)
            for index, image in enumerate(diary_images)
        ]
    )

    diary.save()
    return {"success": True}


@api.delete("/diaries/{diary_id}")
def delete_diary(request, diary_id: int):
    diary = get_object_or_404(Diary, id=diary_id)
    diary.delete()
    return {"success": True}


@api.post("/images", response=List[ImageView])
def upload_image(request, files: List[UploadedFile] = File(...)):
    image_ids = []
    for file in files:
        image = Image.objects.create(url=file)
        image_ids.append(image.id)

    return Image.objects.filter(id__in=image_ids)

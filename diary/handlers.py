from typing import List
from django.shortcuts import get_object_or_404

from ninja.errors import HttpError
from ninja.pagination import paginate

from app.api import api
from diary.models import Diary
from diary.views import DiaryCreateRequest, DiaryUpdateRequest, DiaryView


@api.get("/diaries", response=List[DiaryView])
@paginate
def list_diaries(request):
    return Diary.objects.all()


@api.get("/diaries/{diary_id}", response=DiaryView)
def retrieve_diary(request, diary_id: int):
    try:
        diary = Diary.objects.get(id=diary_id)
    except Diary.DoesNotExist:
        raise HttpError(404, "Diary not found")

    return diary


@api.post("/diaries")
def create_diary(request, payload: DiaryCreateRequest):
    diary = Diary.objects.create(**payload.dict())
    return {"id": diary.id}


@api.put("/diaries/{diary_id}")
def update_diary(request, diary_id: int, payload: DiaryUpdateRequest):
    diary = get_object_or_404(Diary, id=diary_id)
    for attr, value in payload.dict().items():
        setattr(diary, attr, value)
    diary.save()

    return {"success": True}


@api.delete("/diaries/{diary_id}")
def delete_diary(request, diary_id: int):
    diary = get_object_or_404(Diary, id=diary_id)
    diary.delete()
    return {"success": True}

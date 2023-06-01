from uuid import uuid4

from django.db import models


class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.FloatField()
    breakfast = models.TextField(max_length=100)
    lunch = models.TextField(max_length=100)
    dinner = models.TextField(max_length=100)
    other_meals = models.TextField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class DiaryImage(models.Model):
    id = models.AutoField(primary_key=True)
    diary = models.ForeignKey("Diary", on_delete=models.CASCADE)
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


def get_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return f"images/{filename}"


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ImageField(upload_to=get_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

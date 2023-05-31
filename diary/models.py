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


class DiaryPhoto(models.Model):
    id = models.AutoField(primary_key=True)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="diary_photos")
    created_at = models.DateTimeField(auto_now_add=True)

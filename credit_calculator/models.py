from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Userモデルをimportするので消去
# class User(models.Model):
#     first_name = models.CharField(max_length=200, default='')
#     last_name = models.CharField(max_length=200, default='')
#     email = models.CharField(max_length=200, default='')
#     password = models.CharField(max_length=200, default='')


class Professor(models.Model):
    professor_last_name = models.CharField(max_length=200)
    professor_first_name = models.CharField(max_length=200)


class Genre(models.Model):
    genre_name = models.CharField(max_length=200)
    credit_minimum = models.IntegerField
    required_or_select = models.IntegerField


class Class(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=200)
    credit_number = models.IntegerField(default=2)
    grade = models.IntegerField
    semester = models.IntegerField
    day_of_week = models.IntegerField
    period = models.IntegerField


class Time_table(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    grade = models.IntegerField
    semester = models.IntegerField


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

import datetime

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, models.CASCADE)  # Он хранит пароль/логин и прочее
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    balance = models.IntegerField(default=10000)


class Item(models.Model):
    url = models.TextField(max_length=10)
    name = models.TextField(max_length=100)
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

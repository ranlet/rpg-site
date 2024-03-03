import datetime

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    bio = models.TextField(max_length=500)
    user = models.ForeignKey(User, models.CASCADE)  # Он хранит пароль/логин и прочее
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)


class Item(models.Model):
    url = models.TextField(max_length=10)
    name = models.TextField(max_length=100)
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)

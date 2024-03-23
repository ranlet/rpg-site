import datetime

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, models.CASCADE)  # Он хранит пароль/логин и прочее
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    balance = models.IntegerField(default=10000)


class Item(models.Model):
    item_url = models.TextField(max_length=10)
    item_name = models.TextField(max_length=100)
    item_image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    item_type = models.IntegerField(max_length=1, null=True, blank=True)
    item_price = models.IntegerField(null=True, blank=True)

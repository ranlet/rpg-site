import datetime

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, models.CASCADE)  # Он хранит пароль/логин и прочее
    image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    balance = models.IntegerField(default=10000)
    items = models.TextField(blank=True, null=True, default="")


class Item(models.Model):
    item_url = models.TextField(max_length=10)
    item_name = models.TextField(max_length=100)
    item_image = models.FileField(upload_to="profile_img/", blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    item_type = models.IntegerField(null=True, blank=True)
    item_price = models.IntegerField(null=True, blank=True)


class Inventory(models.Model):
    item = models.ForeignKey(Item, models.CASCADE, blank=True, null=True)  # Храним предмет
    item_owner = models.ForeignKey(User, models.CASCADE)  # Храним покупателя, при продаже будем его менять на нового
    item_unique_id = models.TextField(max_length=10, blank=True, null=True)  # Создание уникального предмета
    on_market = models.BooleanField(default=0)  # Продаётся ли предмет или нет
    item_price = models.IntegerField(null=True, blank=True)  # Цена на маркете

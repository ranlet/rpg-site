import secrets
import string

from django.contrib.auth.models import User

from main.models import Item


def get_random_name():  # Функция для генерации случайных url длиной 10 символов для новых предметов
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd_length = 10
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd


def default_data():
    first_money = second_money = third_money = None

    if not Item.objects.filter(item_type=3):
        first_money = Item.objects.create(
            item_url="iOpsGgMKtt",
            item_name="1000 валюты",
            item_image="../static/default_img/money.jpg",
            item_description="Валюта для покупки предметов",
            item_type=3,
            item_price=0
        )

        second_money = Item.objects.create(
            item_url="iOpsGgMKuu",
            item_name="4000 валюты",
            item_image="../static/default_img/money.jpg",
            item_description="Валюта для покупки предметов",
            item_type=3,
            item_price=0
        )

        third_money = Item.objects.create(
            item_url="iOpsGgMKgg",
            item_name="10000 валюты",
            item_image="../static/default_img/money.jpg",
            item_description="Валюта для покупки предметов",
            item_type=3,
            item_price=0
        )

    else:
        first_money = Item.objects.get(item_url="iOpsGgMKtt")
        second_money = Item.objects.get(item_url="iOpsGgMKuu")
        third_money = Item.objects.get(item_url="iOpsGgMKgg")
    return {
        'skins': None,
        'weapons': None,
        'money': [first_money, second_money, third_money]
    }


def register(username, email, password, first_name=None, last_name=None):
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    return user

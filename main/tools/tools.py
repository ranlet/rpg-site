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
    if not Item.objects.filter(item_type=2):
        Item.objects.create(
            item_url=get_random_name(),
            item_name="Посох",
            item_image="../static/default_img/magic.png",
            item_description="Волшебный посох",
            item_type=2,
            item_price=3000
        )

        Item.objects.create(
            item_url=get_random_name(),
            item_name="Меч",
            item_image="../static/default_img/blade.png",
            item_description="Волшебный посох",
            item_type=2,
            item_price=5000
        )

        Item.objects.create(
            item_url=get_random_name(),
            item_name="Пистолет",
            item_image="../static/default_img/pistol.png",
            item_description="Мощный пистолет",
            item_type=2,
            item_price=1000
        )

    if not Item.objects.filter(item_type=3):
        for price in [1000, 4000, 10000]:
            Item.objects.create(
                item_url=get_random_name(),
                item_name=f"{price} валюты",
                item_image="../static/default_img/money.png",
                item_description="Валюта для покупки предметов",
                item_type=3,
                item_price=price
            )

    return {
        'skins': Item.objects.filter(item_type=1),
        'weapons': Item.objects.filter(item_type=2),
        'money': Item.objects.filter(item_type=3)
    }


def register(username, email, password, first_name=None, last_name=None):
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    return user

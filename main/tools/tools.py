import secrets
import string

from django.contrib.auth.models import User

from main.models import Item


def get_random_name(n):  # Функция для генерации случайных url/id длиной n символов для новых предметов
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd_length = n
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd


def default_data():
    url_len = 10
    def_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    if not Item.objects.filter(item_type=1):
        for i in range(30):  # Создание заглушек
            Item.objects.create(
                item_url=get_random_name(url_len),
                item_name=f"Скин-заглушка {i}",
                item_image="../static/default_img/icon.png",
                item_description=def_text,
                item_type=1,
                item_price=1000
            )

    if not Item.objects.filter(item_type=2):
        def_weapons = [
            {
                "name": "Посох",
                "description": "Волшебный посох",
                "image": "../static/default_img/magic.png",
                "price": 3000,
            },
            {
                "name": "Меч",
                "description": "Большой меч",
                "image": "../static/default_img/blade.png",
                "price": 5000
            },
            {
                "name": "Пистолет",
                "description": "Мощный пистолет",
                "image": "../static/default_img/pistol.png",
                "price": 1000
            }
        ]
        for item in def_weapons:
            Item.objects.create(
                item_url=get_random_name(url_len),
                item_name=item["name"],
                item_image=item["image"],
                item_description=item["description"],
                item_type=2,
                item_price=item["price"]
            )

        for i in range(30):  # Создание заглушек
            Item.objects.create(
                item_url=get_random_name(url_len),
                item_name=f"Оружие-заглушка {i}",
                item_image="../static/default_img/icon.png",
                item_description=def_text,
                item_type=2,
                item_price=500
            )

    if not Item.objects.filter(item_type=3):
        for price in [1000, 4000, 10000]:
            Item.objects.create(
                item_url=get_random_name(url_len),
                item_name=f"{price} валюты",
                item_image="../static/default_img/money.png",
                item_description="Валюта для покупки предметов(пока бесплатно)",
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


def list_splitter(l):
    n = 6
    return [l[i:i + n] for i in range(0, len(l), n)]

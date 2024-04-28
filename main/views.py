from django.contrib.auth.models import User
from main.models import Profile, Item, Inventory
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from main.tools.tools import default_data, register, list_splitter, get_random_name


@login_required
def index_page(request: WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    def_data = default_data()
    default_skins = def_data['skins']
    default_weapons = def_data['weapons']

    skins = []
    weapons = []
    obj_str = profile.items.strip().split()

    for skin in default_skins:
        if skin.item_url not in obj_str:
            skins.append(skin)
    for weapon in default_weapons:
        if weapon.item_url not in obj_str:
            weapons.append(weapon)

    context = {
        'pagename': 'Покупка предметов',
        'user': request.user,
        'profile': Profile.objects.get(user=request.user),
        'money': list_splitter(def_data['money']),
        'skins': list_splitter(skins),
        'weapons': list_splitter(weapons)
    }
    return render(request, 'pages/index.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


def login_page(request: WSGIRequest):
    context = {
        'err_reason': 0
    }

    if request.method == 'GET':
        return render(request, 'registration/login.html', context)

    if 'logname' in request.POST and 'logpass' in request.POST:
        username = request.POST['logname']
        password = request.POST['logpass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'registration/login.html', {
            'err_reason': 1
        })

    elif 'regname' in request.POST and 'regpass' in request.POST:
        username = request.POST['regname']
        password = request.POST['regpass']

        checking = User.objects.filter(username=username)

        if not checking:
            first_name = 'Имя'
            last_name = 'Фамилия'
            if 'regfirst' in request.POST:
                if request.POST['regfirst'] != '':
                    first_name = request.POST['regfirst']

            if 'reglast' in request.POST:
                if request.POST['reglast'] != '':
                    last_name = request.POST['reglast']

            user = register(
                username,
                username + '@rpg.proj',
                password,
                first_name,
                last_name
            )

            profile = Profile()
            profile.user = user
            profile.save()
            return render(request, 'registration/login.html', {
                'err_reason': 3
            })
        else:
            return render(request, 'registration/login.html', {
                'err_reason': 2
            })

    return render(request, 'registration/login.html', context)


@login_required
def profile_page(request: WSGIRequest):
    context = {
        'user': request.user,
        'profile': Profile.objects.get(user=request.user)
    }

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=request.user)

        if request.POST['firstname'] != '':
            user.first_name = request.POST['firstname']
        if request.POST['lastname'] != '':
            user.last_name = request.POST['lastname']

        if 'filename' in request.FILES:
            if request.FILES['filename'] != '':
                profile.image = request.FILES['filename']

        user.save()
        profile.save()

        context = {
            'user': user,
            'profile': profile
        }

        return render(request, 'pages/profile.html', context)

    return render(request, 'pages/profile.html', context)


@login_required
def item_page(request: WSGIRequest, url):
    obj = Item.objects.get(item_url=url)
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)

    context = {
        'item': obj,
        'user': user,
        'profile': profile
    }

    if request.method == 'POST':
        if obj.item_type == 1 or obj.item_type == 2:

            new = Inventory.objects.create(  # Создание уникального предмета
                item=obj,
                item_owner=user,
                item_unique_id=get_random_name(12),
            )

            profile.items += new.item_unique_id + " "
            profile.balance -= obj.item_price
            profile.save()

            return redirect('/')

        elif obj.item_type == 3:
            profile.balance += obj.item_price
            profile.save()
            return redirect('/')

    return render(request, 'pages/item.html', context)


@login_required
def inventory_page(request: WSGIRequest):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)

    skins = []
    weapons = []
    obj_str = profile.items.strip().split()

    print(obj_str)

    for url in obj_str:
        inventory_item = Inventory.objects.get(item_unique_id=url)  # Уникальный предмет пользователя
        item = inventory_item.item  # Получаем сам предмет
        if item.item_type == 1:
            skins.append(inventory_item)
        elif item.item_type == 2:
            weapons.append(inventory_item)

    context = {
        'user': user,
        'profile': profile,
        'skins': list_splitter(skins),
        'weapons': list_splitter(weapons)
    }

    return render(request, 'pages/inventory.html', context)


@login_required
def sell_page(request: WSGIRequest, url):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)
    obj = Inventory.objects.get(item_unique_id=url)

    context = {
        'user': user,
        'profile': profile,
        'item': obj
    }

    if request.method == 'POST':
        print(request.POST)

    return render(request, 'pages/sell.html', context)


def main_page(request: WSGIRequest):
    context = {
    }
    return render(request, 'pages/main_page.html', context)

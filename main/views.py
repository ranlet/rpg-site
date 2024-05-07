from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User
from main.models import Profile, Item, Inventory
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main.tools.tools import default_data, register, list_splitter, get_random_name


@login_required
def index_page(request: WSGIRequest):
    profile = Profile.objects.get(user=request.user)
    def_data = default_data()
    default_skins = def_data['skins']
    default_weapons = def_data['weapons']

    skins = []
    weapons = []
    market = []
    obj_str = profile.items.strip().split()
    goods = Inventory.objects.filter(on_market=True)

    for skin in default_skins:
        if skin.item_url not in obj_str:
            skins.append(skin)
    for weapon in default_weapons:
        if weapon.item_url not in obj_str:
            weapons.append(weapon)
    for item in goods:
        if item.on_market and request.user != item.item_owner:
            market.append(item)

    context = {
        'pagename': 'Покупка предметов',
        'user': request.user,
        'profile': Profile.objects.get(user=request.user),
        'money': list_splitter(def_data['money']),
        'skins': list_splitter(skins),
        'weapons': list_splitter(weapons),
        'market': list_splitter(market)
    }
    return render(request, 'pages/index.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


def login_page(request: WSGIRequest):
    context = {

    }

    if request.method == 'GET':
        if request.user.username:
            return redirect('/')
        return render(request, 'registration/login.html', context)

    if 'logname' in request.POST and 'logpass' in request.POST:
        username = request.POST['logname']
        password = request.POST['logpass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.error(request, "Неправильный логин или пароль")
        return render(request, 'registration/login.html', context)

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
            messages.success(request, "Вы успешно зарегистрировались!")
            return render(request, 'registration/login.html', context)
        else:
            messages.warning(request, "Пользователь с таким именем существует")
            return render(request, 'registration/login.html', context)

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

        messages.success(request, "Изменения применены!")
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
            if profile.balance >= obj.item_price:
                new = Inventory.objects.create(  # Создание уникального предмета
                    item=obj,
                    item_owner=user,
                    item_unique_id=get_random_name(12),
                )

                profile.items += new.item_unique_id + " "
                profile.balance -= obj.item_price
                profile.save()
                messages.success(request, f"Товар {obj.item_name} успешно приобретён!")
                return redirect('/')
            else:
                messages.error(request, "Недостаточно средств!")
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

        obj.item_price = int(request.POST['price'])
        obj.on_market = True
        obj.save()
        messages.success(request, f"Товар {obj.item.item_name} теперь на маркете!")
        return redirect('/inventory')

    return render(request, 'pages/sell.html', context)


@login_required
def withdraw_func(request: WSGIRequest, url):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)
    obj = Inventory.objects.get(item_unique_id=url)

    if user == obj.item_owner:
        obj.on_market = False
        obj.save()
    else:
        messages.error(request, f"Товар {obj.item.item_name} принадлежит другому пользователю!")
        return redirect('/inventory')

    messages.warning(request, f"Товар {obj.item.item_name} снят с продажи!")
    return redirect('/inventory')


@login_required
def buy_page(request: WSGIRequest, url):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)

    obj = Inventory.objects.get(item_unique_id=url)

    seller = Profile.objects.get(user=obj.item_owner)
    print(seller.user.username)

    context = {
        'user': user,
        'profile': profile,
        'seller': seller,
        'item': obj,
    }

    return render(request, 'pages/buy.html', context)

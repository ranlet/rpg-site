from django.contrib.auth.models import User
from main.models import Profile, Item
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from main.tools.tools import default_data, register, list_splitter

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
        'money': def_data['money'],
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
            profile.items += obj.item_url + " "
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
        try:
            item = Item.objects.get(item_url=url)
        except Item.DoesNotExist:
            return None
        if item.item_type == 1:
            skins.append(item)
        elif item.item_type == 2:
            weapons.append(item)

    context = {
        'user': user,
        'profile': profile,
        'skins': skins,
        'weapons': weapons
    }

    return render(request, 'pages/inventory.html', context)

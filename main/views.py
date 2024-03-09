import random
import datetime

from django.contrib.auth.models import User
from main.models import Profile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import secrets
import string


def register(username, email, password, first_name=None, last_name=None):
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    return user


@login_required
def index_page(request: WSGIRequest):
    context = {
        'pagename': 'Покупка предметов',
        'user': request.user,
        'profile': Profile.objects.get(user=request.user)
    }
    return render(request, 'pages/index.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


def login_page(request: WSGIRequest):
    context = {
        'pagename': 'Войти',

    }

    if request.method == 'POST':
        if 'logname' in request.POST and 'logpass' in request.POST:
            username = request.POST['logname']
            password = request.POST['logpass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
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
            else:
                redirect('/')

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

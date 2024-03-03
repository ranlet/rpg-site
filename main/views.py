import random
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import secrets
import string


def index_page(request: WSGIRequest):
    context = {
        'pagename': 'Покупка предметов'
    }
    return render(request, 'pages/index.html', context)


def login_page(request: WSGIRequest):
    context = {
        'pagename': 'Войти',

    }

    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['passwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/login.html', context)

    return render(request, 'registration/login.html', context)

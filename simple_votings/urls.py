from django.contrib import admin
from django.urls import path

from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

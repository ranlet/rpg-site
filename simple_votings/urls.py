from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='Магазин'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('item/<str:url>', views.item_page, name='item'),
    path('inventory/', views.inventory_page, name='inventory')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from django.contrib.auth import views as standart_views

from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', standart_views.LoginView.as_view(), name='login'),
    path('logout/', standart_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.register, name = 'register'),
    ]

from django.urls import path

from . import views

app_name = 'bots'
urlpatterns = [
    path('create_post/', views.create_post, name = 'create_post'),
    ]

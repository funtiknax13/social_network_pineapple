from django.urls import path
from django.contrib.auth import views as standart_views

from . import views

app_name = 'dialogs'
urlpatterns = [
    path('dialog_with_<str:username>/', views.dialog, name = 'dialog'),
    path('dialog_with_<str:reciever_name>/leave_message/', views.leave_message, name = 'leave_message'),
    path('messages/', views.messages, name = 'messages'),
    path('post<str:username>/', views.post, name = 'post'),
    path('new_messages/', views.new_messages, name = 'new_messages'),

    ]

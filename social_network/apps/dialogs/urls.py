from django.urls import path
from django.contrib.auth import views as standart_views

from . import views

app_name = 'dialogs'
urlpatterns = [
    path('dialog/<str:username>/', views.dialog, name = 'dialog'),
    path('dialog/<str:reciever_name>/leave_message/', views.leave_message, name = 'leave_message'),
    path('messages/', views.messages, name = 'messages'),
    path('post<str:username>/', views.post, name = 'post'),
    path('new_messages/', views.new_messages, name = 'new_messages'),
    path('message<int:message_id>/delete/', views.delete_message, name = 'delete_message'),
    path('dialog<int:companion_id>/delete/', views.delete_dialog, name = 'delete_dialog'),
    ]

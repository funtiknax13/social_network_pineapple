from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from .models import Message
from account.models import Friend
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json

#Запрос новых сообщений
@login_required(login_url = '/')
def post(request, username):
    companion = User.objects.get(username = username)
    messages = Message.objects.filter(reciever = request.user, sender = companion, is_readed = False)
    for message in messages:
        message.is_readed = True
        message.save()
    context = {'messages': messages, 'user': request.user}
    if messages:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_list": render_to_string('dialogs/dialog_messages_block.html', context),
            }),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json"
        )

#Диалог авторизованного пользователя с username
@login_required(login_url = '/')
def dialog(request, username):
    companion = User.objects.get(username = username)
    messages = (Message.objects.filter(sender = request.user, reciever = companion) | Message.objects.filter(reciever = request.user, sender = companion)).order_by("-message_time")[:20]
    messages2 = (Message.objects.filter(sender = request.user, reciever = companion) | Message.objects.filter(reciever = request.user, sender = companion)).order_by("-message_time")[20:]
    not_readed_messages = Message.objects.filter(reciever = request.user, sender = companion, is_readed = False)
    for message in not_readed_messages:
        message.is_readed = True
        message.save()
    friend = User.objects.get(username = username)
    context = {'sort_messages':messages[::-1], 'friend': friend, 'messages2': messages2}
    return render(request, 'dialogs/dialog.html', context)


#Проверка на новые сообщения
@login_required(login_url = '/')
def new_messages(request):
    messages = Message.objects.filter(reciever = request.user, is_readed = False)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False)
    if messages or new_friends:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_count": len(messages),
                "new_friends": len(new_friends),
            }), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }), content_type="application/json")

#Отправка сообщения
@login_required(login_url = '/')
def leave_message(request, reciever_name):
    reciever_user = User.objects.get(username = reciever_name)
    if request.method == 'POST':
        message_text = request.POST['message_text']
        if len(message_text) > 500:
            save_message_text = message_text[:499]
        else:
            save_message_text = message_text
        a = Message(sender = request.user, reciever = reciever_user, message_text = save_message_text, message_time = timezone.now())
        a.save()
    messages = Message.objects.filter(id = a.id)
    context = {'messages': messages, 'user': request.user}
    if messages:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_list": render_to_string('dialogs/dialog_messages_block.html', context),
            }),
            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json")


#Вывод всех диалогов пользователя
@login_required(login_url = '/')
def messages(request):
    messages = (Message.objects.filter(sender = request.user) | Message.objects.filter(reciever = request.user)).order_by("-message_time")
    users = []
    last_messages = []
    for message in messages:
        if message.sender != request.user:
            if not message.sender in users:
                users.append(message.sender)
                last_message = (Message.objects.filter(sender = message.sender, reciever = request.user)|Message.objects.filter(reciever = message.sender, sender = request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
        if message.reciever != request.user:
            if not message.reciever in users:
                users.append(message.reciever)
                last_message = (Message.objects.filter(sender = message.reciever, reciever = request.user)|Message.objects.filter(reciever = message.reciever, sender = request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
    last_messages_list = []
    for message_query in last_messages:
        for message in message_query:
            if not message.is_readed and message.reciever == request.user:
                last_messages_list.insert(0, message)
            else:
                last_messages_list.append(message)


    context = {'users': users, 'messages': last_messages_list}
    return render(request, 'dialogs/messages.html', context)

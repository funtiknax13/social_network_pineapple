from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Friend, Follower
from posts.forms import PostForm
from posts.models import Post
from django.utils import timezone
from .forms import ProfileForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#Аккаунт пользователя
@login_required(login_url = '/')
def user_account(request):
    username = request.user
    user = User.objects.get(username = username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.post_time = timezone.now()
            new_post.save()
            return HttpResponseRedirect(request.path)
    else:
        form = PostForm()

    user_posts = Post.objects.filter(author = user).order_by("-post_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 10)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    followers = Follower.objects.filter(follower_for = request.user)
    context = {'user': user, 'form':form, 'user_posts': post_list, 'followers': followers}
    return render(request, 'account/account.html', context)

#Изменение аватара пользователя
@login_required(login_url = '/')
def account_setting(request):
    user_set = User.objects.get(id = request.user.id)
    print(user_set.profile.city)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_set.profile)
        if form.is_valid():
            user_setting = request.user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            avatar = form.cleaned_data['avatar']
            gender = form.cleaned_data['gender']
            city = form.cleaned_data['city']
            birth_date = form.cleaned_data['birth_date']
            if avatar:
                user_setting.profile.avatar = avatar
            else:
                user_setting.profile.avatar = 'images/avatar/standart.jpg'
            user_setting.profile.gender = gender
            user_setting.profile.city = city
            user_setting.profile.birth_date = birth_date
            if first_name:
                user_setting.first_name = first_name
            if last_name:
                user_setting.last_name = last_name
            user_setting.save()
            return HttpResponseRedirect(reverse('account:user_account'))
    else:
        form = ProfileForm(instance=user_set.profile)
    context = {'form': form}
    return render(request, 'account/setting.html', context)


@login_required(login_url = '/')
def friends(request):
    users_friends1 = Friend.objects.filter(user = request.user, confirmed = True)
    users_friends2 = Friend.objects.filter(users_friend = request.user, confirmed = True)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False).count()
    context = {"friends1": users_friends1, "friends2": users_friends2, "not_confirmed_friends_count": new_friends}
    return render(request, 'account/friends.html', context)


@login_required(login_url = '/')
def friend_request(request):
    not_confirmed_friends = Friend.objects.filter(users_friend = request.user, confirmed = False)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False).count()
    context = {"not_confirmed_friends": not_confirmed_friends, "not_confirmed_friends_count": new_friends}
    return render(request, 'account/friend_request.html', context)


@login_required(login_url = '/')
def add_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    is_friend = Friend.objects.filter(user = request.user, users_friend = user)|Friend.objects.filter(user = user, users_friend = request.user)
    if not is_friend:
        add_friend = Friend(user = request.user, users_friend = user)
        add_friend.save()
    return HttpResponseRedirect(reverse('account:account', args = (account_id, )))


@login_required(login_url = '/')
def confirm_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    new_friend = Friend.objects.get(user = user, users_friend = request.user)
    new_friend.confirmed = True
    new_friend.save()
    return HttpResponseRedirect(reverse('account:friends'))


@login_required(login_url = '/')
def delete_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    new_friend = Friend.objects.filter(user = user, users_friend = request.user)|Friend.objects.filter(user = request.user, users_friend = user )
    new_friend.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#Поиск/отображение всех пользователей
@login_required(login_url = '/')
def find_users(request):
    if request.method == 'POST':
        user_setting = request.user
        search = request.POST.get('search')
        queryset = User.objects.all().exclude(username = request.user)
        if search:
            search_list = search.split(' ')
            if len(search_list) == 2:
                users = queryset.filter(Q(first_name__iexact=search_list[0]) & Q(last_name__iexact=search_list[1])|Q(first_name__iexact=search_list[1]) & Q(last_name__iexact=search_list[0]))
            elif len(search_list) == 1:
                users = queryset.filter(Q(first_name__iexact=search_list[0]) | Q(last_name__iexact=search_list[0]))
            else:
                users = False
        else:
            users = False
    else:
        users = User.objects.all().exclude(username = request.user).order_by("-id")[:20]
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False).count()
    context = {
        'users': users,
        "not_confirmed_friends_count": new_friends
    }
    return render(request, 'account/users.html', context)


#Переход на аккаунт другого пользователя
@login_required(login_url = '/')
def account(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    if Friend.objects.filter(user = request.user, users_friend = user)|Friend.objects.filter(user = user, users_friend = request.user):
        is_friend = False
    else:
        is_friend = True

    if Follower.objects.filter(user = request.user, follower_for = user):
        is_follower = False
    else:
        is_follower = True

    users_friends1 = Friend.objects.filter(user = user, confirmed = True)#[:6]
    users_friends2 = Friend.objects.filter(users_friend = user, confirmed = True)#[:6-len(users_friends1)]

    user_posts = Post.objects.filter(author = user).order_by("-post_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 10)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    user_following = Follower.objects.filter(user = user)
    context = {'other_user': user, 'user_posts': post_list, 'is_friend': is_friend, "friends1": users_friends1, "friends2": users_friends2, 'is_follower': is_follower, 'user_following': user_following}
    return render(request, 'account/id.html', context)


@login_required(login_url = '/')
def add_follower(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    is_follower = Follower.objects.filter(user = request.user, follower_for = user)
    if not is_follower:
        add_follower = Follower(user = request.user, follower_for = user)
        add_follower.save()
    return HttpResponseRedirect(reverse('account:account', args = (account_id, )))


@login_required(login_url = '/')
def delete_follower(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    follower = Follower.objects.filter(user = request.user, follower_for = user)
    follower.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

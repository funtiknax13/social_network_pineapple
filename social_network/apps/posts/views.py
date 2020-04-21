from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from account.models import Friend
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url = '/')
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")
    post.delete()
    return HttpResponseRedirect(reverse('account:user_account'))


@login_required(login_url = '/')
def news(request):
    posts = Post.objects.all().exclude(author = request.user).order_by("-post_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 20)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    context = {'posts': post_list}
    return render(request, 'posts/news.html', context)


@login_required(login_url = '/')
def friend_news(request):
    posts = Post.objects.all().exclude(author = request.user).order_by("-post_time")
    friend_post = []
    for post in posts:
        if Friend.objects.filter(user = request.user, users_friend = post.author, confirmed = True)|Friend.objects.filter(user = post.author, users_friend = request.user, confirmed = True):
            friend_post.append(post)
    page = request.GET.get('page', 1)
    paginator = Paginator(friend_post, 20)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    context = {'posts': post_list}
    return render(request, 'posts/friend_news.html', context)


@login_required(login_url = '/')
def like_news(request):
    like_posts = Like.objects.filter(user = request.user, like_or_dislike = 'like')
    page = request.GET.get('page', 1)
    paginator = Paginator(like_posts, 20)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    context = {'posts': post_list}
    return render(request, 'posts/like_news.html', context)

@login_required(login_url = '/')
def like_or_dislike(request, post_id, is_like):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")
    old_like = Like.objects.filter(user = request.user, for_post = post)
    if old_like:
        like = Like.objects.get(user = request.user, for_post = post)
        if like.like_or_dislike == 'like' and is_like == 'like':
            like.delete()
            post.post_like -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'dislike':
            like.delete()
            post.post_dislike -= 1
            post.save()
        elif like.like_or_dislike == 'like' and is_like == 'dislike':
            like.like_or_dislike = 'dislike'
            like.save()
            post.post_dislike += 1
            post.post_like -= 1
            post.save()
        elif like.like_or_dislike == 'dislike' and is_like == 'like':
            like.like_or_dislike = "like"
            like.save()
            post.post_dislike -= 1
            post.post_like += 1
            post.save()
    else:
        new_like = Like(user = request.user, for_post = post, like_or_dislike = is_like)
        new_like.save()
        if is_like == 'like':
            post.post_like += 1
            post.save()
        elif is_like == 'dislike':
            post.post_dislike += 1
            post.save()

    is_like = Like.objects.filter(user = request.user, for_post = post)
    if is_like:
        user_like = True
        is_like = Like.objects.get(user = request.user, for_post = post)
        user_like_val = is_like.like_or_dislike
    else:
        user_like = False
        user_like_val = ''

    return HttpResponse(
        json.dumps({
            "result": True,
            "user_like": user_like,
            "user_like_val": user_like_val,
            "like": post.post_like,
            "dislike": post.post_dislike
        }),
        content_type="application/json"
    )


def user_like(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")

    is_like = Like.objects.filter(user = request.user, for_post = post)
    if is_like:
        user_like = True
        is_like = Like.objects.get(user = request.user, for_post = post)
        user_like_val = is_like.like_or_dislike
    else:
        user_like = False
        user_like_val = ''

    return HttpResponse(
        json.dumps({
            "result": True,
            "user_like": user_like,
            "user_like_val": user_like_val,
            "like": post.post_like,
            "dislike": post.post_dislike
        }),
        content_type="application/json"
    )

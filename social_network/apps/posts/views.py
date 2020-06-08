from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from account.models import Friend, Follower
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from django.utils import timezone
from django.template.loader import render_to_string

@login_required(login_url = '/')
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")
    if post.author == request.user:
        post.delete()
    return HttpResponseRedirect(reverse('account:user_account'))


@login_required(login_url = '/')
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")

    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post.post_title = form.cleaned_data['post_title']
                post.post_text = form.cleaned_data['post_text']
                image = form.cleaned_data['post_image']
                if image:
                    post.post_image = image
                else:
                    post.post_image = ''
                post.save()

                return HttpResponseRedirect(reverse('account:user_account'))
        else:
            form = PostForm(instance=post)
        context = {'form': form, "post": post}
        return render(request, 'posts/edit_post.html', context)
    else:
        return HttpResponseRedirect(reverse('account:user_account'))


@login_required(login_url = '/')
def post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")

    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/news'+str(post_id)+'/' or request.META.get('HTTP_REFERER') == 'http://mypineapple.pythonanywhere.com/news'+str(post_id)+'/':
        pass
    else:
        request.session['return_path'] = request.META.get('HTTP_REFERER','/')

    context = {"post": post}
    return render(request, 'posts/post.html', context)


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
        if Friend.objects.filter(user = request.user, users_friend = post.author, confirmed = True)|Friend.objects.filter(user = post.author, users_friend = request.user, confirmed = True) or Follower.objects.filter(user = request.user, follower_for = post.author):
            friend_post.append(post)
    page = request.GET.get('page', 1)
    paginator = Paginator(friend_post, 20)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)

    follow_list = Follower.objects.filter(user = request.user)
    context = {'posts': post_list, 'follow_list': follow_list}
    return render(request, 'posts/friend_news.html', context)


@login_required(login_url = '/')
def like_news(request):
    like_posts = request.user.post_liked.all().order_by("-post_time")
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
def like_or_dislike(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.post_like.add(request.user)
            else:
                post.post_like.remove(request.user)
            if action == 'dislike':
                post.post_dislike.add(request.user)
            else:
                post.post_dislike.remove(request.user)
                return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})


@login_required(login_url = '/')
def user_like(request):
    likes = Like.objects.all()
    for like in likes:
        if like.like_or_dislike == "like":
            like.for_post.post_like.add(like.user)
        if like.like_or_dislike == "dislike":
            like.for_post.post_dislike.add(like.user)
    return HttpResponse("Complete")


@login_required(login_url = '/')
def leave_comment(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except:
        raise Http404("Пост не найден!")

    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        comment = post.post_comments.create(comment_author = request.user, comment_text = comment_text, comment_pubdate = timezone.now())

    if comment:
        context = {'comment': comment, 'post': post}
        return HttpResponse(
            json.dumps({
                "result": True,
                "comment": render_to_string('posts/create_comment.html', context),
            }),
            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json")


@login_required(login_url = '/')
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id = comment_id)
    except:
        raise Http404("Комментарий не найден!")
    if comment.comment_author == request.user:
        comment.delete()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no'})


def back(request):
    return redirect(request.session['return_path'])

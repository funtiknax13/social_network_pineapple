from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('delete<int:post_id>/', views.delete_post, name = 'delete_post'),
    path('edit_post<int:post_id>/', views.edit_post, name = 'edit_post'),
    path('news/', views.news, name = 'news'),
    path('like_news/', views.like_news, name = 'like_news'),
    path('friend_news/', views.friend_news, name = 'friend_news'),
    path('news/like/', views.like_or_dislike, name = 'like_or_dislike'),
    path('news/user_like', views.user_like, name = 'user_like'),
    path('news<int:post_id>/leave_comment', views.leave_comment, name = 'leave_comment'),
    path('comment<int:comment_id>/delete', views.delete_comment, name = 'delete_comment'),
    path('news<int:post_id>/', views.post, name = 'post'),
    path('back/', views.back, name = 'back'),
]

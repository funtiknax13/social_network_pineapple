from django.contrib import admin

from .models import Profile, Friend, Follower


admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(Follower)

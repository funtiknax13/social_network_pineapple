from django.contrib import admin

from .models import Profile, Friend, Follower, Status


admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Friend)
admin.site.register(Follower)

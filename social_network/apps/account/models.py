from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    GENDER_CHOICE = (
    ("M", "М"),
    ("F", "Ж"),
    (None, "-")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар', blank=True, upload_to = 'images/avatar/')
    gender =  models.CharField('Пол', max_length=1,
                  choices=GENDER_CHOICE,
                  blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Friend(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    users_friend = models.ForeignKey(User, related_name = 'users_friend', on_delete = models.CASCADE)
    confirmed = models.BooleanField('Подтверждено', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    follower_for = models.ForeignKey(User, related_name = 'follower_for', on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

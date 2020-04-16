from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    reciever = models.ForeignKey(User, related_name = 'to_reciever', on_delete = models.DO_NOTHING)
    message_text = models.TextField('Текст сообщения')
    message_image = models.ImageField('Изображение', blank = True, upload_to = 'images/messages/')
    message_time = models.DateTimeField('Время отправления')
    is_readed = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return str(self.sender)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

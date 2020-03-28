from django.db import models


class FeedBack(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email_or_phone = models.CharField(max_length=250, verbose_name='E-mail или телефон')
    text = models.TextField(verbose_name='Текст сообщения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.email_or_phone)

from django.db import models
from users.models import User


class FeedBack(models.Model):
    name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    email = models.EmailField(max_length=150, verbose_name='Электронная почта')
    text = models.TextField(verbose_name='Текст сообщения')
    doc = models.FileField('Файл', upload_to='feedback/', max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Интернет-приёмная'

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.email)


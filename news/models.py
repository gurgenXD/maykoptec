from django.db import models
from django.urls import reverse
from core.models import SEO


class News(SEO):
    title = models.CharField(max_length=250, unique=True, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('created',)

    def __str__(self):
        return self.title

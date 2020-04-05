from django.db import models
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from core.models import Position


class Page(MPTTModel, Position):
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, related_name='children',
                            verbose_name='Родительская страница', blank=True, null=True)
    title = models.CharField(max_length=250, verbose_name='Название страницы', unique=True)
    url = models.CharField(max_length=250, verbose_name='URL', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Показывать в меню')
    in_footer = models.BooleanField(default=True, verbose_name='Показывать в футере')

    def __str__(self):
        return self.title

    @property
    def sub_pages(self):
        return Page.objects.filter(parent=self, is_active=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

mptt.register(Page,)

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe


class User(AbstractUser):
    USERS_TYPES = [
        ('individual', 'Физическое лицо'),
        ('entity', 'Юридическое лицо'),
        ('businessman', 'Индивидуальный предприниматель'),
    ]

    user_type = models.CharField('Тип пользователя', max_length=250, choices=USERS_TYPES, blank=True, null=True)
    new_email = models.EmailField('Новый E-mail', max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'
    
    def get_profile_link(self):
        if self.user_type == 'individual':
            a = '<a href="/admin/users/individual/{0}/change/">Ссылка на профиль</a>'.format(self.individual.id)
        elif self.user_type == 'entity':
            a = '<a href="/admin/users/entity/{0}/change/">Ссылка на профиль</a>'.format(self.entity.id)
        elif self.user_type == 'businessman':
            a = '<a href="/admin/users/businessman/{0}/change/">Ссылка на профиль</a>'.format(self.businessman.id)
        else:
            a = '-'

        return mark_safe(a)
    get_profile_link.short_description = 'Подробная информация'
    get_profile_link.allow_tags = True


class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='individual', verbose_name='Пользователь')
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=150)
    patronymic = models.CharField('Отчество', max_length=150)
    phone = models.CharField('Телефон', max_length=20)

    series_number = models.CharField('Серия и номер', max_length=20)
    issue_date = models.DateField('Дата выдачи')
    issued_by = models.CharField('Кем выдан', max_length=250)
    address = models.CharField('Адрес прописки', max_length=250)
    address_fact = models.CharField('Адрес фактического проживния', max_length=250)

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'
        ordering = ('created',)

    @property
    def get_full_name(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.patronymic)

    @property
    def get_series(self):
        return self.series_number.split()[0] if self.series_number else None

    @property
    def get_number(self):
        return self.series_number.split()[1] if self.series_number else None

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_name, self.last_name, self.patronymic)


class BaseEntity(models.Model):
    inn = models.CharField('ИНН', max_length=50)
    kpp = models.CharField('КПП', max_length=50)
    e_address = models.CharField('Юридический адрес', max_length=250)
    p_address = models.CharField('Почтовый адрес', max_length=250)

    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=150, blank=True, null=True)
    phone = models.CharField('Контактный телефон', max_length=20, blank=True, null=True)
    fax = models.CharField('Факс', max_length=20, blank=True, null=True)

    bank = models.CharField('Название банка', max_length=150, blank=True, null=True)
    bik = models.CharField('БИК', max_length=50, blank=True, null=True)
    check = models.CharField('Расчётный стёт', max_length=50, blank=True, null=True)
    korr = models.CharField('Корр. счёт', max_length=50, blank=True, null=True)

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True

    @property
    def get_full_name(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.patronymic)

    def __str__(self):
        return '{0} ({1})'.format(self.user.username, self.user.email)


class Entity(BaseEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='entity', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Юридичское лицо'
        verbose_name_plural = 'Юридичские лица'


class BusinessMan(BaseEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='businessman', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальные предприниматели'

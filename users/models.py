from django.db import models
from django.contrib.auth.models import AbstractUser


class UserType(models.Model):
    name = models.CharField('Тип пользователя', max_length=250)

    class Meta:
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Типы пользователей'

    def __str__(self):
        return self.name


class User(AbstractUser):
    USERS_TYPES = [
        ('individual', 'Физическое лицо'),
        ('entity', 'Юридическое лицо'),
        ('businessman', 'Индивидуальный предприниматель'),
    ]

    patronymic = models.CharField('Отчество', max_length=150, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    user_type = models.CharField('Тип пользователя', max_length=250, choices=USERS_TYPES, blank=True, null=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'

    # def __str__(self):
    #     return self.title


class Individual(models.Model):
    CATEGORIES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'C'),
        ('be', 'BE'),
        ('ce', 'CE'),
        ('tm', 'Tm'),
        ('rb', 'Tb'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='individuals', verbose_name='Пользователь')
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=150, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)

    p_series_number = models.CharField('Серия и номер', max_length=20, blank=True, null=True)
    p_issue_date = models.DateField('Дата выдачи', blank=True, null=True)
    p_issued_by = models.CharField('Кем выдан', max_length=250, blank=True, null=True)
    p_address = models.CharField('Адрес прописки', max_length=250, blank=True, null=True)
    p_address_fact = models.CharField('Адрес фактического проживния', max_length=250, blank=True, null=True)

    v_number = models.CharField('Номер', max_length=20, blank=True, null=True)
    v_code = models.CharField('Код подразделения', max_length=20, blank=True, null=True)
    v_issue_date = models.DateField('Дата выдачи', blank=True, null=True)
    v_end_date = models.DateField('Дата окончания действия', blank=True, null=True)
    v_region = models.CharField('Регион', max_length=250, blank=True, null=True)
    v_category = models.CharField('Категория', max_length=5, choices=CATEGORIES, blank=True, null=True)

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'
        ordering = ('created',)

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_name, self.last_name, self.patronymic)


class Entity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entities', verbose_name='Пользователь')
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
        verbose_name = 'Юридичское лицо'
        verbose_name_plural = 'Юридичское лицо'

    def __str__(self):
        return '{0} ({1})'.format(self.user.username, self.user.email)


class BusinessMan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businessmans', verbose_name='Пользователь')
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
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальный предприниматель'

    def __str__(self):
        return '{0} ({1})'.format(self.user.username, self.user.email)
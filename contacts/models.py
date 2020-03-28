from django.db import models


class Address(models.Model):
    value = models.CharField(max_length=250, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.value


class Phone(models.Model):
    PHONE_TYPES = [
        ('customers', 'Центр ослуживания клиентов'),
        ('dispatch', 'Оперативно диспетчерская служба'),
    ]

    phone_type = models.CharField(max_length=250, choices=PHONE_TYPES, verbose_name='Тип телефона')
    value = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return self.value


class Email(models.Model):
    value = models.EmailField(max_length=250, verbose_name='E-mail')

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'E-mails'

    def __str__(self):
        return self.value


class MapCode(models.Model):
    MAP_TYPE = [
        ('contacts', 'Контакты '),
        ('area', 'Зона деятельности'),
    ]

    map_type = models.CharField(max_length=250, choices=MAP_TYPE, verbose_name='Тип карты')
    value = models.TextField(verbose_name='Карта')

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.value


class Schedule(models.Model):
    days = models.CharField(max_length=250, verbose_name='Дни недели')
    time = models.CharField(max_length=250, verbose_name='Время работы')

    class Meta:
        verbose_name = 'Пункт'
        verbose_name_plural = 'Режим работы'

    def __str__(self):
        return '{0} {1}'.format(self.days, self.time)


class ActivityArea(models.Model):
    city = models.CharField(max_length=250, verbose_name='Насленный пункт')
    desc = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Зона деятельности'
        verbose_name_plural = 'Зоны деятельности'

    def __str__(self):
        return self.city

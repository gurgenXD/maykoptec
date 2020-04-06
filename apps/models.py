from django.db import models
from users.models import User
from django.utils.html import mark_safe
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.models import MailToString, MailFromString
from django.urls import reverse


class ReqApp(models.Model):
    DEVICE_TYPES = [
        ('vru', 'ВРУ 0.4 кВ'),
        ('ru', 'РУ 6/10 кВ'),
        ('ktp', 'КТП'),
        ('tp', 'ТП'),
    ]

    RELIABILITY_LVLS = [
        ('first', 'Первая категория'),
        ('second', 'Вторая категория'),
        ('third', 'Третья категория'),
    ]

    VOLTAGE_LVLS = [
        ('lvl1', '0.22 кВ (220 Вольт)'),
        ('lvl2', '0.4 кВ (380 Вольт)'),
        ('lvl3', '6/10 кВ'),
        ('lvl4', 'Иное'),
    ]

    REASONS = [
        ('r1', 'Новое строительство'),
        ('r2', 'Увеличение максимальной мощности устройств, присоединенных ранее'),
        ('r3', 'Изменение точки присоединения'),
        ('r4', 'Изменение схемы внешнего электроснабжения'),
        ('r5', 'Изменение категории надежности электроснабжени'),
        ('r6', 'Иное'),
    ]

    STATUSES = [
        ('st1', 'Не рассмотрена'),
        ('st2', 'Получена'),
        ('st3', 'Комплект документов неполный'),
        ('st4', 'Проверен комплект документов'),
        ('st5', 'Подготовка технических условий и проекта договора'),
        ('st6', 'Технические условия и проект договора отправлены заявителю'),
        ('st7', 'Согласование замечаний к ТУ и договору'),
        ('st8', 'Договор получен'),
        ('st9', 'Заявка отменена'),
        ('st10', 'Договор зарегистрирован'),
        ('st11', 'Работы по технологическому присоединению выполнены'),
        ('st12', 'Осуществлено фактическое присоединение к сети'),
        ('st13', 'Отправлены отчетные документы'),
        ('st14', 'Акты получены'),
        ('st15', 'Заявка закрыта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reqapps', verbose_name='Пользователь')
    status = models.CharField('Статус', max_length=250, choices=STATUSES, default='st1')
    device_type = models.CharField('Тип энергопринимающего устройства', max_length=30, choices=DEVICE_TYPES, default='vru')
    address = models.CharField('Адрес принимающих устройств для присоединения', max_length=250)
    max_power = models.CharField('Максимальная мощность энергопринимающих устройств (кВт)', max_length=250)
    reliasbility_lvl = models.CharField('Заявленный уровень надежности', max_length=30, choices=RELIABILITY_LVLS, default='first')
    voltage_lvl = models.CharField('Заявленный уровень напряжения', max_length=30, choices=VOLTAGE_LVLS, default='lvl1')
    reason = models.CharField('Причина подачи заявления', max_length=250, choices=REASONS, default='r1')
    points_count = models.TextField('Количество точек присоединения к электрической сети с указанием технических параметров элементов энергопринимающих устройст (класс напряжения и др.)')
    load_type = models.TextField('Характер нагрузки (вид экономической деятельности хозяйствующего субъекта)')
    file1 = models.FileField('Название документа', upload_to='requests/', max_length=150, null=True, blank=True)
    file2 = models.FileField('Название другого документа', upload_to='requests/', max_length=150, null=True, blank=True)

    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('created',)

    def get_absolute_url(self):
        return reverse('update_request', args=[self.id])

    def req_nmb(self):
        return 'Заявка №{0}'.format(self.id)
    req_nmb.short_description = 'Номер заявки'
    req_nmb.allow_tags = True

    def get_profile_link(self):
        if self.user.user_type == 'individual':
            a = '<a href="/admin/users/individual/{0}/change/">{1}</a>'.format(self.user.individual.id, self.user.username)
        elif self.user.user_type == 'entity':
            a = '<a href="/admin/users/entity/{0}/change/">{1}</a>'.format(self.user.entity.id, self.user.username)
        elif self.user.user_type == 'businessman':
            a = '<a href="/admin/users/businessman/{0}/change/">{1}</a>'.format(self.user.businessman.id, self.user.username)
        else:
            a = '-'
        return mark_safe(a)
    get_profile_link.short_description = 'Пользователь'
    get_profile_link.allow_tags = True

    def __str__(self):
        return 'Заявка №{0} (Пользователь: {1})'.format(self.id, self.user.username)


@receiver(pre_save, sender=ReqApp, dispatch_uid="send_email")
def send_email(sender, instance, **kwargs):
    old = ReqApp.objects.get(pk=instance.pk)
    if old.status != instance.status:
        current_site = Site.objects.get_current()
        mail_subject = 'Изменен статус: ' + current_site.domain
        message = render_to_string('requests/change-status-message.html', {
            'domain': current_site.domain,
            'id': instance.id,
            'old': old,
            'new': instance,
        })
        to_email = old.user.email
        from_email = MailFromString.objects.first().host_user
        email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
        email.send()


class ChatMessage(models.Model):
    req = models.ForeignKey(ReqApp, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='Сообщения')
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_from', verbose_name='От кого', blank=True, null=True)
    msg_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_to', verbose_name='Кому', blank=True, null=True)
    text = models.TextField(verbose_name='Текст сообщения')

    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Чат'
        ordering = ('created',)

    def __str__(self):
        return 'От: {0}, Кому: {1}'.format(self.msg_from, self.msg_to)

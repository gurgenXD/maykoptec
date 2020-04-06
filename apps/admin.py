from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.models import MailToString, MailFromString
from apps.models import *


class ChatMessageInlime(admin.StackedInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('msg_from', 'msg_to', 'created')


@admin.register(ReqApp)
class ReqAppAdmin(admin.ModelAdmin):
    list_display = ('req_nmb', 'get_profile_link', 'status', 'created', 'updated')
    search_fields = ('user__username', 'reason', 'load_type', 'points_count', 'status', 'device_type', 'reliasbility_lvl', 'voltage_lvl')
    list_filter = ('status', 'device_type', 'reliasbility_lvl', 'voltage_lvl', 'reason')
    list_editable =('status',)
    inlines = (ChatMessageInlime,)

    def save_formset(self, request, form, formset, change):
        formset.save(commit=False)
        for f in formset.forms:
            obj = f.instance
            if not obj.msg_from and not obj.msg_to:
                obj.msg_from = request.user
                obj.msg_to = obj.req.user
                obj.save()

                current_site = get_current_site(request)
                mail_subject = 'Новое сообщение на сайте: ' + current_site.domain
                message = render_to_string('requests/chat-message.html', {
                    'domain': current_site.domain,
                    'req': obj.req,
                    'msg': obj,
                })
                to_email = [obj.req.user.email]
                from_email = MailFromString.objects.first().host_user
                email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
                email.send()


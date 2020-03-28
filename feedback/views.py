from django.views import View
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from feedback.forms import *
from core.models import MailToString


class FeedBackView(View):
    def post(self, request):
        feedback_form = FeedBackForm(request.POST)
        status = 0

        if feedback_form.is_valid() and request.recaptcha_is_valid:
            current_site = get_current_site(request)
            mail_subject = 'Новое сообщение на сайте: ' + current_site.domain
            message = render_to_string('feedback/feedback_message.html', {
                'domain': current_site.domain,
                'email_or_phone': request.POST.get('email_or_phone'),
                'name': request.POST.get('name'),
                'text': request.POST.get('text'),
            })
            to_email = MailToString.objects.first().email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            feedback_form.save()
            status = 1
            
        context = {
            'status': status,
        }
        return JsonResponse(context)

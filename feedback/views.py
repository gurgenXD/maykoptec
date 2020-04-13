from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from feedback.forms import *
from core.models import MailToString, MailFromString


class FeedBackView(View):
    def get(self, request):
        user = request.user
        user_info = None

        if user.is_authenticated:
            if user.user_type == 'individual':
                user_info = user.individual
            if user.user_type == 'entity':
                user_info = user.entity
            if user.user_type == 'businessman':
                user_info = user.businessman

        if user_info:
            feedback_form = FeedBackForm(initial={
                'name': user_info.get_full_name,
                'phone': user_info.phone,
                'email': user.email,
            })
        else:
            feedback_form = FeedBackForm()

        context = {
            'feedback_form': feedback_form,
            'feedback_done': False,
        }
        return render(request, 'feedback/feedback.html', context)

    def post(self, request):
        feedback_form = FeedBackForm(request.POST, request.FILES)
        feedback_done = False
        print(request.FILES)

        if feedback_form.is_valid():
            current_site = get_current_site(request)
            mail_subject = 'Новое обращение на сайте: ' + current_site.domain
            message = render_to_string('feedback/feedback-message.html', {
                'domain': current_site.domain,
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'name': request.POST.get('name'),
                'text': request.POST.get('text'),
            })
            to_email = [item.email for item in MailToString.objects.filter(email_type='all')]
            from_email = MailFromString.objects.first().host_user
            email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
            email.send()
            feedback_form.save()
            feedback_done = True
            feedback_form = FeedBackForm()
            
        context = {
            'feedback_form': feedback_form,
            'feedback_done': feedback_done,
        }
        return render(request, 'feedback/feedback.html', context)

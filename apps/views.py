from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.models import MailToString, MailFromString
from apps.models import ReqApp
from apps.forms import ReqForm
from django.http import Http404


class ProfileRequestView(View):
    def get(self, request):
        user = request.user
        reqs = ReqApp.objects.filter(user=user)

        context = {
            'reqs': reqs,
        }

        return render(request, 'requests/profile-request.html', context)


class CreateRequestView(View):
    def get(self, request):
        create_req_form = ReqForm()

        context = {
            'create_req_form': create_req_form,
        }

        return render(request, 'requests/create-request.html', context)

    def post(self, request):
        user = request.user
        create_req_form = ReqForm(request.POST, request.FILES)

        if create_req_form.is_valid():
            new_req = create_req_form.save(commit=False)
            new_req.user = user
            new_req.save()

            current_site = get_current_site(request)
            mail_subject = 'Новая заявка на сайте: ' + current_site.domain
            message = render_to_string('requests/request-message.html', {
                'domain': current_site.domain,
                'id': new_req.id,
                'address': new_req.address,
                'username': new_req.user.username,
            })
            to_email = [item.email for item in MailToString.objects.all()]
            from_email = MailFromString.objects.first().host_user
            email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
            email.send()

            return redirect('profile')

        context = {
            'create_req_form': create_req_form,
        }

        return render(request, 'requests/create-request.html', context)


class UpdateRequestView(View):
    def get(self, request, req_id):
        user = request.user
        req = get_object_or_404(ReqApp, id=req_id)

        if req.user != user:
            raise Http404('Страница не найдена')

        create_req_form = ReqForm(initial={
            'device_type': req.device_type,
            'address': req.address,
            'max_power': req.max_power,
            'reliasbility_lvl': req.reliasbility_lvl,
            'voltage_lvl': req.voltage_lvl,
            'reason': req.reason,
            'points_count': req.points_count,
            'load_type': req.load_type,
        })

        context = {
            'create_req_form': create_req_form,
            'req': req,
            'updated': False,
        }

        return render(request, 'requests/update-request.html', context)

    def post(self, request, req_id):
        user = request.user
        req = get_object_or_404(ReqApp, id=req_id)
        updated = False

        if req.user != user:
            raise Http404('Страница не найдена')

        create_req_form = ReqForm(request.POST, request.FILES, instance=req)

        if create_req_form.is_valid():
            create_req_form.save()
            updated = True


        context = {
            'create_req_form': create_req_form,
            'req': req,
            'updated': updated,
        }

        return render(request, 'requests/update-request.html', context)


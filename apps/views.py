from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.models import MailToString, MailFromString
from apps.models import ReqApp
from apps.forms import *
from django.http import Http404
from core.pagination import pagination
from core.pdf_generator import generate_pdf
from core.models import Index


def send_pdf(request, new_req):
    current_site = get_current_site(request)
    mail_subject = 'Новая заявка на сайте: ' + current_site.domain
    message = render_to_string('requests/request-message.html', {
        'domain': current_site.domain,
        'id': new_req.id,
        'address': new_req.address,
        'username': new_req.user.username,
    })
    to_email = [item.email for item in MailToString.objects.filter(email_type='req')]
    to_email.append(new_req.user.email)
    from_email = MailFromString.objects.first().host_user
    email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
    email.attach_file(new_req.pdf.path)
    for item in new_req.documents.all():
        email.attach_file(item.document.path)
    email.send()


class ProfileRequestView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('/')
        reqs = ReqApp.objects.filter(user=user)

        context = {
            'reqs': reqs,
        }

        return render(request, 'requests/profile-request.html', context)


class CreateRequestView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        create_req_form = ReqForm()
        doc_list = Index.objects.first().file

        context = {
            'create_req_form': create_req_form,
            'doc_list': doc_list,
        }

        return render(request, 'requests/create-request.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        create_req_form = ReqForm(request.POST, request.FILES)
        doc_list = Index.objects.first().file

        if create_req_form.is_valid():
            new_req = create_req_form.save(commit=False)
            new_req.user = user
            new_req.save()

            for item in request.FILES:
                if item.find('doc') != -1:
                    ReqDocuments.objects.create(
                        req=new_req,
                        title=request.POST[item + '_name'] or 'Без названия',
                        document=request.FILES[item]
                    )

            generate_pdf({'req': new_req})
            send_pdf(request, new_req)

            return redirect('profile')

        context = {
            'doc_list': doc_list,
            'create_req_form': create_req_form,
        }

        return render(request, 'requests/create-request.html', context)


class UpdateRequestView(View):
    def get(self, request, req_id):
        if not request.user.is_authenticated:
            return redirect('/')
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

        chat_form = ChatForm()
        chat_messages = ChatMessage.objects.filter(req=req).order_by('-created')

        page_number = request.GET.get('page', 1)
        pag_res = pagination(chat_messages, page_number)
        chat = True if int(page_number) > 1 else False

        context = {
            'create_req_form': create_req_form,
            'req': req,
            'updated': False,
            'chat_form': chat_form,
            'chat_messages': chat_messages,
            'chat': chat,

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }

        return render(request, 'requests/update-request.html', context)

    def post(self, request, req_id):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        req = get_object_or_404(ReqApp, id=req_id)
        updated = False

        if req.user != user:
            raise Http404('Страница не найдена')

        create_req_form = ReqForm(request.POST, request.FILES, instance=req)
        chat_form = ChatForm()

        if create_req_form.is_valid():
            create_req_form.save()

            for item in request.FILES:
                if item.find('doc') != -1:
                    ReqDocuments.objects.create(
                        req=req,
                        title=request.POST[item + '_name'] or 'Без названия',
                        document=request.FILES[item]
                    )

            generate_pdf({'req': req})

            updated = True

        chat_messages = ChatMessage.objects.filter(req=req).order_by('-created')

        page_number = request.GET.get('page', 1)
        pag_res = pagination(chat_messages, page_number)

        context = {
            'create_req_form': create_req_form,
            'req': req,
            'updated': updated,
            'chat_form': chat_form,
            'chat_messages': chat_messages,
            'chat': False,

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }

        return render(request, 'requests/update-request.html', context)


class AddChatMessage(View):
    def post(self, request, req_id):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        req = get_object_or_404(ReqApp, id=req_id)

        if req.user != user:
            raise Http404('Страница не найдена')

        chat_form = ChatForm(request.POST)

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

        if chat_form.is_valid():
            msg = chat_form.save(commit=False)
            msg.msg_from = req.user
            staff = User.objects.filter(is_staff=True).first()
            msg.msg_to = staff
            msg.req = req
            msg.save()

            current_site = get_current_site(request)
            mail_subject = 'Новое обращение в тех. поддержку: ' + current_site.domain
            message = render_to_string('requests/chat-message.html', {
                'domain': current_site.domain,
                'req': req,
                'msg': msg,
            })
            to_email = [item.email for item in MailToString.objects.filter(emaiL_type='req')]
            from_email = MailFromString.objects.first().host_user
            email = EmailMessage(mail_subject, message, from_email=from_email, to=to_email)
            email.send()

            return redirect('/requests/update-request/{0}/'.format(req.id))

        chat_messages = ChatMessage.objects.filter(req=req).order_by('-created')

        page_number = request.GET.get('page', 1)
        pag_res = pagination(chat_messages, page_number)

        context = {
            'create_req_form': create_req_form,
            'chat_form': chat_form,
            'chat_messages': chat_messages,
            'req': req,
            'updated': False,
            'chat': True,

            'page_object': pag_res['page'],
            'is_paginated': pag_res['is_paginated'],
            'next_url': pag_res['next_url'],
            'prev_url': pag_res['prev_url'],
        }

        return render(request, 'requests/update-request.html', context)
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from users.forms import *
from core.tokens import account_activation_token, change_email_token
from core.models import MailFromString
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


User = get_user_model()


def send_mail(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Подтверждение почты'
    message = render_to_string('users/activate-message.html', {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    from_email = MailFromString.objects.first().host_user
    email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
    email.send()


def send_mail2(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Подтверждение почты'
    message = render_to_string('users/change-email-message.html', {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': change_email_token.make_token(user),
    })
    to_email = user.new_email
    from_email = MailFromString.objects.first().host_user
    email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
    email.send()


class SignUpView(View):
    def get(self, request):
        individual_form = IndividualSignUpForm()
        entity_form = EntitySignUpForm()
        businessman_form = BusinessManSignUpForm()

        context = {
            'individual_form': individual_form,
            'entity_form': entity_form,
            'businessman_form': businessman_form,
            'tab': 1,
        }
        return render(request, 'users/signup.html', context)


class IndividualSignUpView(View):
    def post(self, request):
        individual_form = IndividualSignUpForm(request.POST)
        entity_form = EntitySignUpForm()
        businessman_form = BusinessManSignUpForm()

        if individual_form.is_valid() and request.recaptcha_is_valid:
            new_user = individual_form.save()
            send_mail(request, new_user)
            return render(request, 'users/signup-confirm.html')

        context = {
            'individual_form': individual_form,
            'entity_form': entity_form,
            'businessman_form': businessman_form,
            'tab': 1,
        }
        return render(request, 'users/signup.html', context)


class EntitySignUpView(View):
    def post(self, request):
        individual_form = IndividualSignUpForm()
        entity_form = EntitySignUpForm(request.POST)
        businessman_form = BusinessManSignUpForm()

        if entity_form.is_valid() and request.recaptcha_is_valid:
            new_user = entity_form.save()
            send_mail(request, new_user)
            return render(request, 'users/signup-confirm.html')

        context = {
            'individual_form': individual_form,
            'entity_form': entity_form,
            'businessman_form': businessman_form,
            'tab': 2,
        }
        return render(request, 'users/signup.html', context)


class BusinessManSignUpView(View):
    def post(self, request):
        individual_form = IndividualSignUpForm()
        entity_form = EntitySignUpForm()
        businessman_form = BusinessManSignUpForm(request.POST)

        if businessman_form.is_valid() and request.recaptcha_is_valid:
            new_user = businessman_form.save()
            send_mail(request, new_user)
            return render(request, 'users/signup-confirm.html')

        context = {
            'individual_form': individual_form,
            'entity_form': entity_form,
            'businessman_form': businessman_form,
            'tab': 3,
        }
        return render(request, 'users/signup.html', context)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/activate-complete.html')
        else:
            return render(request, 'users/activate-old.html')


class ChangeEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and change_email_token.check_token(user, token):
            user.email = user.new_email
            user.new_email = None
            user.save()
            return render(request, 'users/activate-complete.html')
        else:
            return render(request, 'users/activate-old.html')


class LogoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        logout(request)
        return redirect('/')


class SignInView(View):
    def post(self, request):
        form = IndividualSignInForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)
            success = True
        else:
            success = False

        context = {
            'success': success,
            'domain': get_current_site(request).domain,
        }

        return JsonResponse(context)


class ProfileInfoView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        change_pass_form = ChangePasswordForm(user)

        businessman_form = None
        entity_form = None
        individual_form = None

        if user.user_type == 'businessman':
            businessman_form = BusinessmanUpdateForm(user)

        if user.user_type == 'entity':
            entity_form = EntityUpdateForm(user)

        if user.user_type == 'individual':
            individual_form = IndividualUpdateForm(user)

        context = {
            'businessman_form': businessman_form,
            'entity_form': entity_form,
            'individual_form': individual_form,
            'change_pass_form': change_pass_form,
        }

        return render(request, 'users/profile-info.html', context)


class ChangePasswordView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        change_pass_form = ChangePasswordForm(user, request.POST)

        if change_pass_form.is_valid():
            password = change_pass_form.cleaned_data.get('new_password1')
            user.set_password(password)
            user.save()
            return redirect('/')
        context = {
            'change_pass_form': change_pass_form,
        }
        return render(request, 'users/profile-info.html', context)


class UpdateProfileInfoView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user

        change_pass_form = ChangePasswordForm(user)

        businessman_form = None
        entity_form = None
        individual_form = None

        if user.user_type == 'businessman':
            businessman_form = BusinessmanUpdateForm(user, request.POST)
            if businessman_form.is_valid():
                businessman_form.save()
                if user.email != businessman_form.cleaned_data['email']:
                    user.new_email = businessman_form.cleaned_data['email']
                    user.save()
                    send_mail2(request, user)
                    return render(request, 'users/signup-confirm.html')
                else:
                    return redirect('profile_info')
        if user.user_type == 'entity':
            entity_form = EntityUpdateForm(user, request.POST)
            if entity_form.is_valid():
                entity_form.save()
                if user.email != entity_form.cleaned_data['email']:
                    user.new_email = entity_form.cleaned_data['email']
                    user.save()
                    send_mail2(request, user)
                    return render(request, 'users/signup-confirm.html')
                else:
                    return redirect('profile_info')
        if user.user_type == 'individual':
            individual_form = IndividualUpdateForm(user, request.POST)
            if individual_form.is_valid():
                individual_form.save()
                if user.email != individual_form.cleaned_data['email']:
                    user.new_email = individual_form.cleaned_data['email']
                    user.save()
                    send_mail2(request, user)
                    return render(request, 'users/signup-confirm.html')
                else:
                    return redirect('profile_info')

        context = {
            'businessman_form': businessman_form,
            'entity_form': entity_form,
            'individual_form': individual_form,
            'change_pass_form': change_pass_form,
        }

        messages.info(request, 'Ваши данные изменены')

        return render(request, 'users/profile-info.html', context)


class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            form.save()
            return redirect('password_reset_done')
        return render(self.request, self.template_name, self.get_context_data())


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
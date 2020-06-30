import re
from datetime import datetime
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.models import Individual, Entity, BusinessMan
from core.models import MailFromString
from core.tokens import account_activation_token

User = get_user_model()


class IndividualSignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'id': 'i-username', 'class': 'form-control SNILS-input', 'placeholder': 'СНИЛС'}),
            'password': forms.PasswordInput(attrs={'id': 'i-password', 'class': 'form-control', 'placeholder': 'Пароль'}),
        }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError('Неправильный СНИЛС или пароль')
        except User.DoesNotExist:
            raise forms.ValidationError('Неправильный СНИЛС или пароль')


class EntitySignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'id': 'e-username', 'class': 'form-control OGRN-input', 'placeholder': 'ОГРН'}),
            'password': forms.PasswordInput(attrs={'id': 'e-password', 'class': 'form-control', 'placeholder': 'Пароль'}),
        }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError('Неправильный ОГРН или пароль')
        except User.DoesNotExist:
            raise forms.ValidationError('Неправильный ОГРН или пароль')


class BusinessManSignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'id': 'b-username', 'class': 'form-control OGRNIP-input', 'placeholder': 'ОГРНИП'}),
            'password': forms.PasswordInput(attrs={'id': 'b-password', 'class': 'form-control', 'placeholder': 'Пароль'}),
        }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError('Неправильный ОГРНИП или пароль')
        except User.DoesNotExist:
            raise forms.ValidationError('Неправильный ОГРНИП или пароль')


class IndividualSignUpForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i1-username', 'class': 'form-control SNILS-input', 'placeholder': 'СНИЛС'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'i-password1', 'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'i-password2', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-last_name', 'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-first_name', 'class': 'form-control', 'placeholder': 'Имя'}))
    patronymic = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-patronymic', 'class': 'form-control', 'placeholder': 'Отчество'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'i-email', 'class': 'form-control', 'placeholder': 'Электронная почта'}))

    series_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-series_number', 'class': 'form-control PASSPORTNUMBER-input', 'placeholder': 'Серия и номер'}))
    issue_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'id': 'i-issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи'}))
    issued_by = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-issued_by', 'class': 'form-control', 'placeholder': 'Кем выдан'}))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-address', 'class': 'form-control', 'placeholder': 'Адрес прописки'}))
    address_fact = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-address_fact', 'class': 'form-control', 'placeholder': 'Адрес фактического проживания'}))

    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'SNILSRegAgreementCheck'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        def check_snils(snils):
            if len(snils) != 14:
                return False

            k = range(9, 0, -1)
            pairs = zip(k, [int(x) for x in snils.replace('-', '').replace(' ', '')[:-2]])
            csum = sum([k * v for k, v in pairs])

            while csum > 101:
                csum %= 101
            if csum in (100, 101):
                csum = 0

            return csum == int(snils[-2:])

        if not check_snils(username):
            raise forms.ValidationError('Укажите правильный СНИЛС')

        username = re.sub(r'\D', '', username)
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        if password2:
            password_validation.validate_password(password2)
        return password2

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            user_type='individual',
            email=self.cleaned_data['email'],
            is_active=False
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()

        try:
            user_info = Individual.objects.create(
                user=user,
                last_name=self.cleaned_data['last_name'],
                first_name=self.cleaned_data['first_name'],
                patronymic=self.cleaned_data['patronymic'],
                phone=self.cleaned_data['phone'],
                series_number=self.cleaned_data['series_number'],
                issue_date=self.cleaned_data['issue_date'],
                issued_by=self.cleaned_data['issued_by'],
                address=self.cleaned_data['address'],
                address_fact=self.cleaned_data['address_fact'],
            )
        except:
            user.delete()
        else:
            return user

class BaseEntitySignUpForm(forms.Form):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'e-password1', 'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'e-password2', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'e-email', 'class': 'form-control', 'placeholder': 'Электронная почта'}))

    inn = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-inn', 'class': 'form-control INN-input', 'placeholder': 'ИНН'}))
    kpp = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-kpp', 'class': 'form-control KPP-input', 'placeholder': 'КПП'}))
    e_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-e_address', 'class': 'form-control', 'placeholder': 'Юридический адрес'}))
    p_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-p_address', 'class': 'form-control', 'placeholder': 'Почтовый адрес'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-last_name', 'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-first_name', 'class': 'form-control', 'placeholder': 'Имя'}))
    patronymic = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-patronymic', 'class': 'form-control', 'placeholder': 'Отчество'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон'}))
    fax = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-fax', 'class': 'form-control PHONE-input', 'placeholder': 'Факс'}))

    bank = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bank', 'class': 'form-control', 'placeholder': 'Название банка'}))
    bik = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bik', 'class': 'form-control', 'placeholder BIK-input': 'БИК'}))
    check = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-check', 'class': 'form-control', 'placeholder RASCH-input': 'Расчётный счёт'}))
    korr = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-korr', 'class': 'form-control', 'placeholder KORR-input': 'Корр. счёт'}))

    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'OGRNRegAgreementCheck'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        if password2:
            password_validation.validate_password(password2)
        return password2


class EntitySignUpForm(BaseEntitySignUpForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e1-username', 'class': 'form-control OGRN-input', 'placeholder': 'ОГРН'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'\D', '', username)

        def check_ogrn(ogrn):
            if len(ogrn) != 13:
                return False

            nmb = int(ogrn[:-1])
            csum = int(ogrn[-1])

            return nmb % 11 % 10 == csum

        if not check_ogrn(username):
            raise forms.ValidationError('Укажите правильный ОГРН')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            user_type='entity',
            email=self.cleaned_data['email'],
            is_active=False
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()

        try:
            Entity.objects.create(
                user=user,
                inn=self.cleaned_data['inn'],
                kpp=self.cleaned_data['kpp'],
                e_address=self.cleaned_data['e_address'],
                p_address=self.cleaned_data['p_address'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                patronymic=self.cleaned_data['patronymic'],
                phone=self.cleaned_data['phone'],
                fax=self.cleaned_data['fax'],
                bank=self.cleaned_data['bank'],
                bik=self.cleaned_data['bik'],
                check=self.cleaned_data['check'],
                korr=self.cleaned_data['korr'],
            )
        except:
            user.delete()
        else:
            return user


class BusinessManSignUpForm(BaseEntitySignUpForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b1-username', 'class': 'form-control OGRNIP-input', 'placeholder': 'ОГРН'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'\D', '', username)

        def check_ogrn(ogrn):
            if len(ogrn) != 15:
                return False

            nmb = int(ogrn[:-1])
            csum = int(ogrn[-1])

            return nmb % 13 % 10 == csum

        if not check_ogrn(username):
            raise forms.ValidationError('Укажите правильный ОГРНИП')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            user_type='businessman',
            email=self.cleaned_data['email'],
            is_active=False
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()

        try:
            user_info = BusinessMan.objects.create(
                user=user,
                inn=self.cleaned_data['inn'],
                kpp=self.cleaned_data['kpp'],
                e_address=self.cleaned_data['e_address'],
                p_address=self.cleaned_data['p_address'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                patronymic=self.cleaned_data['patronymic'],
                phone=self.cleaned_data['phone'],
                fax=self.cleaned_data['fax'],
                bank=self.cleaned_data['bank'],
                bik=self.cleaned_data['bik'],
                check=self.cleaned_data['check'],
                korr=self.cleaned_data['korr'],
            )
        except:
            user.delete()
        else:
            return user


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтной не найден')

        return email
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        from_email = MailFromString.objects.first().host_user

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение нового пароля'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пароль'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}))


class IndividualUpdateForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(IndividualUpdateForm, self).__init__(*args, **kwargs)
        self.user = user
        self.user_info = user.individual
        self.fields['username'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i1-username', 'class': 'form-control SNILS-input', 'placeholder': 'СНИЛС', 'value': self.user.username}))
        self.fields['last_name'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-last_name', 'class': 'form-control', 'placeholder': 'Фамилия', 'value': self.user_info.last_name}))
        self.fields['first_name'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-first_name', 'class': 'form-control', 'placeholder': 'Имя', 'value': self.user_info.first_name}))
        self.fields['patronymic'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-patronymic', 'class': 'form-control', 'placeholder': 'Отчество', 'value': self.user_info.patronymic}))
        self.fields['phone'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон', 'value': self.user_info.phone}))
        self.fields['email'] = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'i-email', 'class': 'form-control', 'placeholder': 'Электронная почта', 'value': self.user.email}))

        self.fields['series_number'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-series_number', 'class': 'form-control PASSPORTNUMBER-input', 'placeholder': 'Серия и номер', 'value': self.user_info.series_number}))
        self.fields['issue_date'] = forms.DateField(required=True, widget=forms.TextInput(attrs={'id': 'i-issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи', 'value': self.user_info.issue_date.strftime('%d.%m.%Y')}))
        self.fields['issued_by'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-issued_by', 'class': 'form-control', 'placeholder': 'Кем выдан', 'value': self.user_info.issued_by}))
        self.fields['address'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-address', 'class': 'form-control', 'placeholder': 'Адрес прописки', 'value': self.user_info.address}))
        self.fields['address_fact'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-address_fact', 'class': 'form-control', 'placeholder': 'Адрес фактического проживания', 'value': self.user_info.address_fact}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'\D', '', username)
        if User.objects.exclude(username=self.user.username).filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(email=self.user.email).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email

    def save(self):
        self.user.username=self.cleaned_data['username']
        self.user.save()

        self.user_info.last_name=self.cleaned_data['last_name']
        self.user_info.first_name=self.cleaned_data['first_name']
        self.user_info.patronymic=self.cleaned_data['patronymic']
        self.user_info.phone=self.cleaned_data['phone']

        self.user_info.series_number=self.cleaned_data['series_number']
        self.user_info.issue_date=self.cleaned_data['issue_date']
        self.user_info.issued_by=self.cleaned_data['issued_by']
        self.user_info.address=self.cleaned_data['address']
        self.user_info.address_fact=self.cleaned_data['address_fact']

        self.user_info.save()


class EntityUpdateForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EntityUpdateForm, self).__init__(*args, **kwargs)
        self.user = user
        self.user_info = user.entity
        self.fields['username'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e1-username', 'class': 'form-control OGRN-input', 'placeholder': 'ОГРН', 'value': self.user.username}))
        self.fields['email'] = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'e-email', 'class': 'form-control', 'placeholder': 'Электронная почта', 'value': self.user.email}))

        self.fields['inn'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-inn', 'class': 'form-control INN-input', 'placeholder': 'ИНН', 'value': self.user_info.inn}))
        self.fields['kpp'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-kpp', 'class': 'form-control KPP-input', 'placeholder': 'КПП', 'value': self.user_info.kpp}))
        self.fields['e_address'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-e_address', 'class': 'form-control', 'placeholder': 'Юридический адрес', 'value': self.user_info.e_address}))
        self.fields['p_address'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-p_address', 'class': 'form-control', 'placeholder': 'Почтовый адрес', 'value': self.user_info.p_address}))

        self.fields['last_name'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-last_name', 'class': 'form-control', 'placeholder': 'Фамилия', 'value': self.user_info.last_name}))
        self.fields['first_name'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-first_name', 'class': 'form-control', 'placeholder': 'Имя', 'value': self.user_info.first_name}))
        self.fields['patronymic'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-patronymic', 'class': 'form-control', 'placeholder': 'Отчество', 'value': self.user_info.patronymic}))
        self.fields['phone'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон', 'value': self.user_info.phone}))
        self.fields['fax'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-fax', 'class': 'form-control PHONE-input', 'placeholder': 'Факс', 'value': self.user_info.fax}))

        self.fields['bank'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bank', 'class': 'form-control', 'placeholder': 'Название банка', 'value': self.user_info.bank}))
        self.fields['bik'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bik', 'class': 'form-control', 'placeholder BIK-input': 'БИК', 'value': self.user_info.bik}))
        self.fields['check'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-check', 'class': 'form-control', 'placeholder RASCH-input': 'Расчётный счёт', 'value': self.user_info.check}))
        self.fields['korr'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-korr', 'class': 'form-control', 'placeholder KORR-input': 'Корр. счёт', 'value': self.user_info.korr}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'\D', '', username)
        if User.objects.exclude(username=self.user.username).filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(email=self.user.email).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email

    def save(self):
        self.user.username=self.cleaned_data['username']
        self.user.save()

        self.user_info.inn=self.cleaned_data['inn']
        self.user_info.kpp=self.cleaned_data['kpp']
        self.user_info.e_address=self.cleaned_data['e_address']
        self.user_info.p_address=self.cleaned_data['p_address']

        self.user_info.last_name=self.cleaned_data['last_name']
        self.user_info.first_name=self.cleaned_data['first_name']
        self.user_info.patronymic=self.cleaned_data['patronymic']
        self.user_info.phone=self.cleaned_data['phone']
        self.user_info.fax=self.cleaned_data['fax']

        self.user_info.bank=self.cleaned_data['bank']
        self.user_info.bik=self.cleaned_data['bik']
        self.user_info.check=self.cleaned_data['check']
        self.user_info.korr=self.cleaned_data['korr']

        self.user_info.save()


class BusinessmanUpdateForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(BusinessmanUpdateForm, self).__init__(*args, **kwargs)
        self.user = user
        self.user_info = user.businessman
        self.fields['username'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e1-username', 'class': 'form-control OGRNIP-input', 'placeholder': 'ОГРН', 'value': self.user.username}))
        self.fields['email'] = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'e-email', 'class': 'form-control', 'placeholder': 'Электронная почта', 'value': self.user.email}))

        self.fields['inn'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-inn', 'class': 'form-control INN-input', 'placeholder': 'ИНН', 'value': self.user_info.inn}))
        self.fields['kpp'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-kpp', 'class': 'form-control KPP-input', 'placeholder': 'КПП', 'value': self.user_info.kpp}))
        self.fields['e_address'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-e_address', 'class': 'form-control', 'placeholder': 'Юридический адрес', 'value': self.user_info.e_address}))
        self.fields['p_address'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-p_address', 'class': 'form-control', 'placeholder': 'Почтовый адрес', 'value': self.user_info.p_address}))

        self.fields['last_name'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-last_name', 'class': 'form-control', 'placeholder': 'Фамилия', 'value': self.user_info.last_name}))
        self.fields['first_name'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-first_name', 'class': 'form-control', 'placeholder': 'Имя', 'value': self.user_info.first_name}))
        self.fields['patronymic'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-patronymic', 'class': 'form-control', 'placeholder': 'Отчество', 'value': self.user_info.patronymic}))
        self.fields['phone'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон', 'value': self.user_info.phone}))
        self.fields['fax'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-fax', 'class': 'form-control PHONE-input', 'placeholder': 'Факс', 'value': self.user_info.fax}))

        self.fields['bank'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bank', 'class': 'form-control', 'placeholder': 'Название банка', 'value': self.user_info.bank}))
        self.fields['bik'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-bik', 'class': 'form-control', 'placeholder BIK-input': 'БИК', 'value': self.user_info.bik}))
        self.fields['check'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-check', 'class': 'form-control', 'placeholder RASCH-input': 'Расчётный счёт', 'value': self.user_info.check}))
        self.fields['korr'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'e-korr', 'class': 'form-control', 'placeholder KORR-input': 'Корр. счёт', 'value': self.user_info.korr}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'\D', '', username)
        if User.objects.exclude(username=self.user.username).filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(email=self.user.email).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует')
        return email

    def save(self):
        self.user.username=self.cleaned_data['username']
        self.user.save()

        self.user_info.inn=self.cleaned_data['inn']
        self.user_info.kpp=self.cleaned_data['kpp']
        self.user_info.e_address=self.cleaned_data['e_address']
        self.user_info.p_address=self.cleaned_data['p_address']

        self.user_info.last_name=self.cleaned_data['last_name']
        self.user_info.first_name=self.cleaned_data['first_name']
        self.user_info.patronymic=self.cleaned_data['patronymic']
        self.user_info.phone=self.cleaned_data['phone']
        self.user_info.fax=self.cleaned_data['fax']

        self.user_info.bank=self.cleaned_data['bank']
        self.user_info.bik=self.cleaned_data['bik']
        self.user_info.check=self.cleaned_data['check']
        self.user_info.korr=self.cleaned_data['korr']

        self.user_info.save()


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
    CATEGORIES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('be', 'BE'),
        ('ce', 'CE'),
        ('tm', 'Tm'),
        ('rb', 'Tb'),
    ]

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i1-username', 'class': 'form-control SNILS-input', 'placeholder': 'СНИЛС'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'i-password1', 'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'i-password2', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-last_name', 'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-first_name', 'class': 'form-control', 'placeholder': 'Имя'}))
    patronymic = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-patronymic', 'class': 'form-control', 'placeholder': 'Отчество'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'i-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'i-email', 'class': 'form-control', 'placeholder': 'Электронная почта'}))

    p_series_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_series_number', 'class': 'form-control PASSPORTNUMBER-input', 'placeholder': 'Серия и номер'}))
    p_issue_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи'}))
    p_issued_by = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_issued_by', 'class': 'form-control', 'placeholder': 'Кем выдан'}))
    p_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_address', 'class': 'form-control', 'placeholder': 'Адрес прописки'}))
    p_address_fact = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_address_fact', 'class': 'form-control', 'placeholder': 'Адрес фактического проживания'}))

    v_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_number', 'class': 'form-control DRIVERCARDNUMBER-input', 'placeholder': 'Номер'}))
    v_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_code', 'class': 'form-control DRIVERCARDGIBDD-input', 'placeholder': 'Код подразделения'}))
    v_issue_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи'}))
    v_end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_end_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата окончания действия'}))
    v_region = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_region', 'class': 'form-control', 'placeholder': 'Регион'}))
    CheckGroup = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'}), choices=CATEGORIES)
    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'SNILSRegAgreementCheck'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
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
                p_series_number=self.cleaned_data['p_series_number'],
                p_issue_date=self.cleaned_data['p_issue_date'],
                p_issued_by=self.cleaned_data['p_issued_by'],
                p_address=self.cleaned_data['p_address'],
                p_address_fact=self.cleaned_data['p_address_fact'],
                v_number= self.cleaned_data['v_number'],
                v_code=self.cleaned_data['v_code'],
                v_issue_date=self.cleaned_data['v_issue_date'],
                v_end_date=self.cleaned_data['v_end_date'],
                v_region=self.cleaned_data['v_region'],
                v_category=', '.join(self.cleaned_data['CheckGroup']),
            )
        except:
            user.delete()
        else:
            return user


class EntitySignUpForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e1-username', 'class': 'form-control OGRN-input', 'placeholder': 'ОГРН'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'e-password1', 'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'e-password2', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'e-email', 'class': 'form-control', 'placeholder': 'Электронная почта'}))

    inn = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-inn', 'class': 'form-control INN-input', 'placeholder': 'ИНН'}))
    kpp = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'e-kpp', 'class': 'form-control KPP-input', 'placeholder': 'КПП'}))
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
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
            user_type='entity',
            email=self.cleaned_data['email'],
            is_active=False
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()

        try:
            user_info = Entity.objects.create(
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


class BusinessManSignUpForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b1-username', 'class': 'form-control OGRNIP-input', 'placeholder': 'ОГРН'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'b-password1', 'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'b-password2', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id': 'b-email', 'class': 'form-control', 'placeholder': 'Электронная почта'}))

    inn = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b-inn', 'class': 'form-control INN-input', 'placeholder': 'ИНН'}))
    kpp = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b-kpp', 'class': 'form-control KPP-input', 'placeholder': 'КПП'}))
    e_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b-e_address', 'class': 'form-control', 'placeholder': 'Юридический адрес'}))
    p_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'b-p_address', 'class': 'form-control', 'placeholder': 'Почтовый адрес'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-last_name', 'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-first_name', 'class': 'form-control', 'placeholder': 'Имя'}))
    patronymic = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-patronymic', 'class': 'form-control', 'placeholder': 'Отчество'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-phone', 'class': 'form-control PHONE-input', 'placeholder': 'Контактный телефон'}))
    fax = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-fax', 'class': 'form-control PHONE-input', 'placeholder': 'Факс'}))

    bank = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-bank', 'class': 'form-control', 'placeholder': 'Название банка'}))
    bik = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-bik', 'class': 'form-control', 'placeholder BIK-input': 'БИК'}))
    check = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-check', 'class': 'form-control', 'placeholder RASCH-input': 'Расчётный счёт'}))
    korr = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'b-korr', 'class': 'form-control', 'placeholder KORR-input': 'Корр. счёт'}))

    agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'OGRNIPRegAgreementCheck'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
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
    CATEGORIES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('be', 'BE'),
        ('ce', 'CE'),
        ('tm', 'Tm'),
        ('rb', 'Tb'),
    ]

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

        self.fields['p_series_number'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_series_number', 'class': 'form-control PASSPORTNUMBER-input', 'placeholder': 'Серия и номер', 'value': self.user_info.p_series_number}))
        self.fields['p_issue_date'] = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи', 'value': self.user_info.p_issue_date.strftime('%d.%m.%Y')}))
        self.fields['p_issued_by'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_issued_by', 'class': 'form-control', 'placeholder': 'Кем выдан', 'value': self.user_info.p_issued_by}))
        self.fields['p_address'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_address', 'class': 'form-control', 'placeholder': 'Адрес прописки', 'value': self.user_info.p_address}))
        self.fields['p_address_fact'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-p_address_fact', 'class': 'form-control', 'placeholder': 'Адрес фактического проживания', 'value': self.user_info.p_address_fact}))

        self.fields['v_number'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_number', 'class': 'form-control DRIVERCARDNUMBER-input', 'placeholder': 'Номер', 'value': self.user_info.v_number}))
        self.fields['v_code'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_code', 'class': 'form-control DRIVERCARDGIBDD-input', 'placeholder': 'Код подразделения', 'value': self.user_info.v_code}))
        self.fields['v_issue_date'] = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_issue_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата выдачи', 'value': self.user_info.v_issue_date.strftime('%d.%m.%Y')}))
        self.fields['v_end_date'] = forms.DateField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_end_date', 'class': 'form-control DATE-input', 'placeholder': 'Дата окончания действия', 'value': self.user_info.v_end_date.strftime('%d.%m.%Y')}))
        self.fields['v_region'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'i-v_region', 'class': 'form-control', 'placeholder': 'Регион', 'value': self.user_info.v_region}))
        self.fields['CheckGroup'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'}), choices=self.CATEGORIES)
        self.fields['CheckGroup'].initial = self.user_info.v_category.split(', ')

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

    def clean(self):
        if (not all((self.cleaned_data['p_series_number'], self.cleaned_data['p_issue_date'], self.cleaned_data['p_issued_by'], self.cleaned_data['p_address'], self.cleaned_data['p_address_fact']))
            and not all((self.cleaned_data['v_number'], self.cleaned_data['v_code'], self.cleaned_data['v_issue_date'], self.cleaned_data['v_end_date'], self.cleaned_data['v_region'], self.cleaned_data['CheckGroup']))):
            raise forms.ValidationError('Введите данные паспорта или водительских прав')


    def save(self):
        self.user.username=self.cleaned_data['username']
        self.user.save()

        self.user_info.last_name=self.cleaned_data['last_name']
        self.user_info.first_name=self.cleaned_data['first_name']
        self.user_info.patronymic=self.cleaned_data['patronymic']
        self.user_info.phone=self.cleaned_data['phone']

        self.user_info.p_series_number=self.cleaned_data['p_series_number']
        self.user_info.p_issue_date=self.cleaned_data['p_issue_date']
        self.user_info.p_issued_by=self.cleaned_data['p_issued_by']
        self.user_info.p_address=self.cleaned_data['p_address']
        self.user_info.p_address_fact=self.cleaned_data['p_address_fact']

        self.user_info.v_number= self.cleaned_data['v_number']
        self.user_info.v_code=self.cleaned_data['v_code']
        self.user_info.v_issue_date=self.cleaned_data['v_issue_date']
        self.user_info.v_end_date=self.cleaned_data['v_end_date']
        self.user_info.v_region=self.cleaned_data['v_region']
        self.user_info.v_category=', '.join(self.cleaned_data['CheckGroup'])

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


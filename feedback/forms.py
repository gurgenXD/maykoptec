from django import forms
from feedback.models import *


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('name', 'email', 'phone', 'text', 'doc')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия Имя Отчество'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder PHONE-input': 'Контактный телефон'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст обращения', 'rows': 4}),
            'doc': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
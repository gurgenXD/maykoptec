from django.shortcuts import render
from django.views import View
from news.models import News
from core.models import Index
from contacts.models import *


class IndexView(View):
    def get(self, request):
        news = News.objects.filter(is_active=True)[:3]
        index = Index.objects.first()

        addresses = Address.objects.all()
        phones_customers = Phone.objects.filter(phone_type='customers')
        phones_dispatch = Phone.objects.filter(phone_type='dispatch')
        emails = Email.objects.all()
        schedule = Schedule.objects.all()
        map_code = MapCode.objects.filter(map_type='contacts').first()

        areas = ActivityArea.objects.all()
        area_code = MapCode.objects.filter(map_type='area').first()

        context = {
            'news': news,
            'index': index,
            'addresses': addresses,
            'phones_customers': phones_customers,
            'phones_dispatch': phones_dispatch,
            'emails': emails,
            'schedule': schedule,
            'map_code': map_code,
            'areas': areas,
            'area_code': area_code,
        }
        return render(request, 'core/index.html', context)


class CalcView(View):
    def get(self, request):
        index = Index.objects.first()
        koef = str(index.koef).replace(',', '.')

        context = {
            'koef': koef,
        }
        return render(request, 'core/calc.html', context)
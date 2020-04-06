from django.shortcuts import render, get_object_or_404
from django.views import View
from news.models import News
from core.models import Index
from contacts.models import *
from pages.models import Page
from django.http import Http404


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


class DropMenuView(View):
    def get(self, request, drop_menu):
        drop_page = Page.objects.filter(url__icontains=drop_menu, parent=None).first()

        if not drop_page:
            raise Http404('Страница не найдена')

        pages = Page.objects.filter(parent=drop_page)

        if not pages:
            raise Http404('Страница не найдена')

        context = {
            'pages': pages,
            'drop_page': drop_page,
        }
        return render(request, 'core/drop_menu.html', context)
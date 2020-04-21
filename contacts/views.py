from django.shortcuts import render
from django.views import View
from contacts.models import *
from pages.models import Page


class ContactsView(View):
    def get(self, request):
        addresses = Address.objects.all()
        ptypes = PhoneType.objects.all()
        emails = Email.objects.all()
        schedule = Schedule.objects.all()
        map_code = MapCode.objects.filter(map_type='contacts').first()
        parent = Page.objects.get(action='contacts').parent

        context = {
            'addresses': addresses,
            'ptypes': ptypes,
            'emails': emails,
            'schedule': schedule,
            'map_code': map_code,
            'parent': parent,
        }
        return render(request, 'contacts/contacts.html', context)


class ActivityAreaView(View):
    def get(self, request):
        areas = ActivityArea.objects.all()
        map_code = MapCode.objects.filter(map_type='area').first()
        parent = Page.objects.get(action='activity_area').parent

        context = {
            'areas': areas,
            'map_code': map_code,
            'parent': parent,
        }
        return render(request, 'contacts/activity-area.html', context)

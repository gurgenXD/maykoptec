from django.shortcuts import render
from django.views import View
from contacts.models import *


class ContactsView(View):
    def get(self, request):
        addresses = Address.objects.all()
        phones_customers = Phone.objects.filter(phone_type='customers')
        phones_dispatch = Phone.objects.filter(phone_type='dispatch')
        emails = Email.objects.all()
        schedule = Schedule.objects.all()
        map_code = MapCode.objects.filter(map_type='contacts').first()

        context = {
            'addresses': addresses,
            'phones_customers': phones_customers,
            'phones_dispatch': phones_dispatch,
            'emails': emails,
            'schedule': schedule,
            'map_code': map_code,
        }
        return render(request, 'contacts/contacts.html', context)

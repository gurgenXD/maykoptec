from django.contrib import admin
from contacts.models import *


admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(MapCode)
admin.site.register(ActivityArea)
admin.site.register(Schedule)
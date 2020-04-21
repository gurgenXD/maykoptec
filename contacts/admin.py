from django.contrib import admin
from contacts.models import *


admin.site.register(Address)
admin.site.register(Email)
admin.site.register(MapCode)
admin.site.register(ActivityArea)
admin.site.register(Schedule)


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    classes = ('grp-collapse grp-opened',)


@admin.register(PhoneType)
class PhoneTypeAdmin(admin.ModelAdmin):
    inlines = (PhoneInline, )
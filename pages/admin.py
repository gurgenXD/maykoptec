from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from pages.models import Page


@admin.register(Page)
class PageAdmin(DjangoMpttAdmin):
    group_fieldsets = True
    sortable_field_name = 'position'
    fields = ('parent', 'title', 'url', 'is_active', 'in_footer')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from users.models import *


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('user_type', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # readonly_fields = ('country',)
    # list_display = ('username', 'full_name', 'phone', 'email', 'is_active')


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'patronymic', 'phone')}),
        ('Паспорт', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('p_series_number', 'p_issue_date', 'p_issued_by', 'p_address', 'p_address_fact')
        }),
        ('Водительские права', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('v_number', 'v_code', 'v_issue_date', 'v_end_date', 'v_region', 'v_category'),
        }),
    )


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('inn', 'kpp', 'e_address', 'p_address')}),
        ('Данные контактного лица', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'fax')
        }),
        ('Банковские реквизиты', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('bank', 'bik', 'check', 'korr'),
        }),
    )


@admin.register(BusinessMan)
class BusinessManAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('inn', 'kpp', 'e_address', 'p_address')}),
        ('Данные контактного лица', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'fax')
        }),
        ('Банковские реквизиты', {
            'classes': ('grp-collapse grp-opened',),
            'fields': ('bank', 'bik', 'check', 'korr'),
        }),
    )

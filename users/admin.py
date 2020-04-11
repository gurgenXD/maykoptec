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

    list_display = ('username', 'user_type', 'email', 'is_active', 'is_staff', 'get_profile_link')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'user_type')
    search_fields = ('user_type', 'username', 'email')


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'patronymic', 'phone')}),
        ('Паспорт', {
            'fields': ('series_number', 'issue_date', 'issued_by', 'address', 'address_fact')
        }),
    )

    list_display = ('user', 'first_name', 'last_name', 'patronymic', 'phone')
    search_fields = ('user__username', 'first_name', 'user__email', 'last_name', 'patronymic')


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'inn', 'kpp', 'e_address', 'p_address')}),
        ('Данные контактного лица', {
            'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'fax')
        }),
        ('Банковские реквизиты', {
            'fields': ('bank', 'bik', 'check', 'korr'),
        }),
    )

    list_display = ('user', 'inn', 'kpp', 'e_address', 'p_address')
    search_fields = ('user__username', 'first_name', 'user__email', 'last_name', 'patronymic', 'inn', 'kpp')


@admin.register(BusinessMan)
class BusinessManAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'inn', 'kpp', 'e_address', 'p_address')}),
        ('Данные контактного лица', {
            'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'fax')
        }),
        ('Банковские реквизиты', {
            'fields': ('bank', 'bik', 'check', 'korr'),
        }),
    )

    list_display = ('user', 'inn', 'kpp', 'e_address', 'p_address')
    search_fields = ('user__username', 'first_name', 'user__email', 'last_name', 'patronymic', 'inn', 'kpp')

from django.contrib import admin
from apps.models import ReqApp


@admin.register(ReqApp)
class ReqAppAdmin(admin.ModelAdmin):
    list_display = ('req_nmb', 'get_profile_link', 'status', 'created', 'updated')
    search_fields = ('user__username', 'reason', 'load_type', 'points_count', 'status', 'device_type', 'reliasbility_lvl', 'voltage_lvl')
    list_filter = ('status', 'device_type', 'reliasbility_lvl', 'voltage_lvl', 'reason')
    list_editable =('status',)

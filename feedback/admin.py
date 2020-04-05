from django.contrib import admin
from feedback.models import *


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'email', 'phone', 'created')

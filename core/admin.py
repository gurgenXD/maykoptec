from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from core.models import *


admin.site.register(MailFromString)
admin.site.register(MailToString)
admin.site.register(TitleTag)


# class ProcessInline(admin.TabularInline):
#     model = Process
#     extra = 0
#     classes = ('grp-collapse grp-closed',)


# class IndexWorkInline(admin.TabularInline):
#     model = IndexWork
#     extra = 0
#     classes = ('grp-collapse grp-closed',)


# @admin.register(Index)
# class IndexAdmin(admin.ModelAdmin):
#     inlines = (ProcessInline, IndexWorkInline)


admin.site.unregister(FlatPage)

@admin.register(FlatPage)
class ExtendedFlatPageAdmin(FlatPageAdmin):
    class Media:
        js = (
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        )

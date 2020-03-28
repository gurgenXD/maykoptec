from django.contrib import admin
from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'is_active')
        }),
        ('SEO', {
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
            'classes': ('grp-collapse grp-closed',),
        }),
    )

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'is_active', 'created')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'text')

    class Media:
        js = (
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        )

from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'image', 'is_active', 'order']
    list_editable = ['price', 'duration', 'is_active', 'order', 'image']
    list_filter = ['is_active', 'image']
    search_fields = ['title', 'description']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image')
        }),
        ('Детали услуги', {
            'fields': ('price', 'duration', 'is_active', 'order')
        }),
    )
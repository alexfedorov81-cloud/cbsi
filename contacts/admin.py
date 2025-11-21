from django.contrib import admin
from .models import CallbackRequest

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service', 'created_at', 'is_processed']
    list_editable = ['is_processed']
    list_filter = ['is_processed', 'created_at', 'service']
    search_fields = ['name', 'phone', 'service__title']
    readonly_fields = ['created_at']
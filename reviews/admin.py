from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'rating', 'created_at', 'is_published']
    list_editable = ['is_published']
    list_filter = ['is_published', 'rating', 'created_at']
    search_fields = ['author_name', 'text']
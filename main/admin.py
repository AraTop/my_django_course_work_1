from django.contrib import admin
from main.models import Blog


@admin.register(Blog)
class SettingsAdmin(admin.ModelAdmin):
   list_display = ('header', 'content', 'image', 'publication_date', 'views')
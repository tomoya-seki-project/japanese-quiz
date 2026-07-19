from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'event_type',
        'title',
    )
    readonly_fields = ('event_type', 'title',)
    list_filter = ('event_type',)

    def has_add_permission(self, request):
        return False
    

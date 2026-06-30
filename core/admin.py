from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
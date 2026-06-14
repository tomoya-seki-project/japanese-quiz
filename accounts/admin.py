from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile
User = get_user_model()

@admin.register(User)
class CustomizedUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'last_login',
        'create_at',
        'is_active',
        'is_staff',
    )


    ordering = ('id',)
    search_fields = ('username', 'email',)

    @admin.display(description="Join at")
    def create_at(self, obj):
        return obj.date_joined

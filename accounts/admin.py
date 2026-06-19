from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile
from .forms import UserCreationAdminForm, UserChangeAdminForm
User = get_user_model()

@admin.register(User)
class CustomizedUserAdmin(UserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    list_display = (
        'username',
        'email',
        'last_login',
        'create_at',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    fieldsets = (
        (
            'User Info', {
                'fields':('username', 'email', 'password')
            }
        ),
        (
            'Premission',{
                'fields':('is_staff',"is_active",'is_superuser')
            }
        )
    )

    add_fieldsets = (
        (
            'User Info', {
                'classes': ("wide",),
                'fields': ('username', 'email', 'password1', 'password2')
            }
        ),
    )

    ordering = ('id',)
    search_fields = ('username', 'email',)

    @admin.display(description="Join at")
    def create_at(self, obj):
        return obj.date_joined
    


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

from .models import UserProfile
from .forms import UserCreationAdminForm, UserChangeAdminForm

from dictionary.models import UserVocab
User = get_user_model()

class UserVocabInline(admin.TabularInline):
    model = UserVocab
    extra = 0
    fields = ('vocab', 'in_use')
    readonly_fields = ('vocab',)
    can_delete = False
    def has_view_permission(self, request, obj = ...):
        return False
    
class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    fields = ('last_vocab_sync_at',)
    readonly_fields = ('last_vocab_sync_at',)
    can_delete = False

@admin.register(User)
class CustomizedUserAdmin(UserAdmin):
    #inlines = [UserVocabInline]
    #inlines = [UserProfileInline]
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    list_display = (
        'username',
        'email',
        'last_login',
        'date_joined',
        'is_active',
        'is_staff',
        'is_superuser',
        'user_vocab_count',
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
        ),
        (
            'Profile',{
                'fields':('user_vocab_count','last_sync_at','date_joined','last_login')
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

    readonly_fields = ('user_vocab_count','last_sync_at','date_joined','last_login')

    @admin.display(description="Last Vocab Sync At")
    def last_sync_at(self, obj):
        if not obj.profile.last_vocab_sync_at:
            return "There are not syncing record yet!"
        return timezone.localtime(obj.profile.last_vocab_sync_at).strftime("%B %d, %Y, %H:%M:%S")
    
    @admin.display(description="User Vocab Count")
    def user_vocab_count(self, obj):
        count = obj.user_vocabs.count()
        url = (
            reverse("admin:dictionary_uservocab_changelist")
            + f"?user__id__exact={obj.id}"
        )
        return format_html(
            '{} items<br><a href="{}">View user vocab</a>',
            count,
            url,
        )

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import (
    VocabType,
    VocabCategory,
    VocabLevel,
    VocabRequestStatus,
    VocabRequestType,
)
from .models import (
    Vocab,
    UserVocab,
    VocabDetail,
    KatakanaDetail,
    VocabRequest,
)
@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'word',
        'type',
        'level',
        'created_by',
        'is_active',
        'native_japanese',
        'create_at',
    )
    ordering = ('id',)
    list_display_links = ('id',)
    search_fields = ('word', 'level', 'type')
    list_editable = ('level',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('vocab_detail','katakana_detail')

    @admin.display(description="Native Japanese")
    def native_japanese(self, obj):
        try:
            detail = obj.katakana_detail
        except KatakanaDetail.DoesNotExist:
            detail = None
        return detail.native_japanese if detail else "---"
    

@admin.register(UserVocab)
class UserVocabAdmin(admin.ModelAdmin):
    list_display = (
        'vocab',
        'user',
        'weight',
        'correct_count',
        'incorrect_count',
        'streak',
        'last_quiz_at',
    )
    list_editable = ('weight',)
    ordering = ('user__id',)
    search_fields = ('user__username', 'vocab__word')
    autocomplete_fields = ('user', 'vocab')

@admin.register(VocabRequest)
class VocabRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'request_type',
        'proposed_word',
        'proposed_kana',
        'status',
        'created_by',
    )




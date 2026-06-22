from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404, redirect

from django.urls import path, reverse

from django.views.decorators.http import require_POST

from django.utils.decorators import method_decorator
from django.utils.html import format_html

from .service.vocab_request import VocabRequestService

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
    change_form_template = "admin/dictionary/vocabrequest/change_form.html"
    list_display = (
        'id',
        'request_type',
        'proposed_word',
        'proposed_kana',
        'status',
        'created_by',
    )
    list_filter = (
        'request_type',
        'status',
    )
    search_fields=('proposed_word',)

    readonly_fields = (
        #'review_buttons',
        'created_by',
        'request_type',
        'status',
        'proposed_vocab_type',
        'reviewed_by',
        'original_vocab',
    )

    fields = (
        'request_type',
        'status',
        'original_vocab',
        'proposed_vocab_type',
        'proposed_word',
        'proposed_kana',
        'proposed_meaning',
        'proposed_level',
        'proposed_category',
        #'proposed_similar_word',
        'proposed_native_japanese',
        'created_by',
        #'review_buttons',
    )

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            try:
                is_success = VocabRequestService.approve_vocab_request(
                    vocab_request=obj,
                    reviewed_by=request.user,
                )
            except ValidationError as e:
                self.message_user(
                    request,
                    "; ".join(e.messages),
                    messages.ERROR,
                )
                return redirect(
                    reverse(
                        "admin:dictionary_vocabrequest_change",
                        args=[obj.pk],
                    )
                )
            if is_success:
                self.message_user(
                    request,
                    f"Vocab request approved by {request.user}",
                    messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    f"Vocab request reviewed by {request.user}",
                    messages.WARNING,
                )
            
            return redirect(
                reverse(
                    "admin:dictionary_vocabrequest_changelist"
                )
            )
        if "_reject" in request.POST:
            is_success = VocabRequestService.reject_vocab_request(
                vocab_request=obj,
                reviewed_by=request.user,
            )
            if is_success:
                self.message_user(
                    request,
                    f"Vocab request rejected by {request.user}",
                    messages.WARNING,
                )
            else:
                self.message_user(
                    request,
                    f"Vocab request reviewed by {request.user}",
                    messages.WARNING,
                )
            return redirect(
                reverse(
                    "admin:dictionary_vocabrequest_changelist"
                )
            )
        return super().response_change(request, obj)

    
    ########################################################
    # different way to approve / reject vocab request on each vocab request page
    # kept it for learning reference
    # @admin.display(description="Review")
    # def review_buttons(self, obj):
    #     if not obj.pk:
    #         return "---"
        
    #     if obj.status != VocabRequestStatus.PENDING:
    #         return "Already Reviewed"
        
    #     approve_url = reverse(
    #         "admin:vocabrequest_approve",
    #         args=[obj.pk],
    #     )

    #     reject_url = reverse(
    #         "admin:vocabrequest_reject",
    #         args=[obj.pk],
    #     )

    #     return format_html(
    #         '<a class="button" href="{}">Approve</a>&nbsp;'
    #         '<a class="button" href="{}">Reject</a>',
    #         approve_url,
    #         reject_url,
    #     )
    
    # def get_urls(self):
    #     urls = super().get_urls()

    #     custom_urls = [
    #         path("<int:object_id>/approve/", self.admin_site.admin_view(self.approve_view), name="vocabrequest_approve"),
    #         path("<int:object_id>/reject/", self.admin_site.admin_view(self.reject_view), name="vocabrequest_reject"),
            
    #     ]
    #     return custom_urls + urls
    
    # @method_decorator(require_POST)
    # def approve_view(self, request, object_id):
    #     vocab_request = get_object_or_404(
    #         VocabRequest,
    #         pk = object_id,
    #     )
        
    #     VocabRequestService.approve_vocab_request(
    #         vocab_request=vocab_request,
    #         reviewed_by=request.user
    #     )

    #     self.message_user(
    #         request,
    #         f"Vocab request approved by : {request.user}",
    #         messages.SUCCESS,
    #     )

    #     return redirect(
    #         reverse(
    #             "admin:dictionary_vocabrequest_changelist",
    #         )
    #     )
    
    # @method_decorator(require_POST)
    # def reject_view(self, request, object_id):
    #     vocab_request = get_object_or_404(
    #         VocabRequest,
    #         pk = object_id,
    #     )

    #     VocabRequestService.reject_vocab_request(
    #         vocab_request=vocab_request,
    #         reviewed_by=request.user
    #     )

    #     self.message_user(
    #         request,
    #         f"Vocab request rejected by : {request.user}",
    #         messages.WARNING,
    #     )

    #     return redirect(
    #         reverse(
    #             "admin:dictionary_vocabrequest_changelist",
    #         )
    #     )
    ########################################################


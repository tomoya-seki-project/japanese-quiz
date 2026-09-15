import logging
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404, redirect

from django.urls import path, reverse

from django import forms

from django.views.decorators.http import require_POST

from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils import timezone

from .service.vocab_request import VocabRequestService

from .models import (
    VocabType,
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
    Category,
)

from .forms import VocabRequestChangeAdminForm, VocabChangeAdminForm

logger = logging.getLogger(__name__)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'display',
        'create_at',
    )
    readonly_fields = (
        'create_at',
        'update_at',
    )

@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    form = VocabChangeAdminForm
    list_display = (
        'id',
        'word',
        'type',
        'level',
        'created_by',
        'is_active',
        'create_at',
    )
    readonly_fields = (
        "type",
        "created_by",
        "approved_by",
    )
    ordering = ('id',)
    list_display_links = ('id',)
    search_fields = ('word', 'level', 'type')
    list_filter = (
        'level',
        'type',
        'is_active',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj = ...):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('vocab_detail','katakana_detail')

    @admin.display(description="Japanese equivalent")
    def native_japanese(self, obj):
        try:
            detail = obj.katakana_detail
        except KatakanaDetail.DoesNotExist:
            detail = None
        return detail.native_japanese if detail else "---"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = forms.CheckboxSelectMultiple
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(UserVocab)
class UserVocabAdmin(admin.ModelAdmin):
    list_display = (
        'in_use',
        'vocab',
        'user',
        'weight',
        'correct_count',
        'incorrect_count',
        'streak',
        'last_quiz_at',
    )

    readonly_fields = (
        'vocab',
        'user',
        'correct_count',
        'incorrect_count',
        'last_quiz_at',
        'last_answer',
    )

    list_display_links = ('vocab',)

    list_editable = ('in_use', 'weight',)
    ordering = ('user__id',)
    search_fields = ('user__username', 'vocab__word')
    autocomplete_fields = ('user', 'vocab')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj = ...):
        return False

@admin.register(VocabRequest)
class VocabRequestAdmin(admin.ModelAdmin):
    form = VocabRequestChangeAdminForm
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
        'created_by',
        'request_type',
        'status',
        'proposed_vocab_type',
        'reviewed_by',
        'original_vocab',
        'create_at',
        'update_at',
        'request_reason',
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
        'proposed_categories',
        'proposed_native_japanese',
        'created_by',
        'create_at',
        'update_at',
        'request_reason',
        'review_note',
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "proposed_categories":
            kwargs["widget"] = forms.CheckboxSelectMultiple
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj = ...):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if (request.method == "POST"
            and ("_approve" in request.POST
                or "_reject" in request.POST
                )
        ):
            qs = qs.select_for_update()
        return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj is not None and obj.status != VocabRequestStatus.PENDING:
            return [field.name for field in self.model._meta.fields]
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if change and obj.status != VocabRequestStatus.PENDING:
            self.message_user(
                request,
                "A request cannot be changed after it has been reviewed.",
                messages.ERROR,
            )
            return
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "_reject" in request.POST:
            if "review_note" in form.base_fields:
                form.base_fields["review_note"].required = True
                form.base_fields["review_note"].error_messages["required"] = (
                    "A review note is required when rejecting a request."
                )
        if obj is not None and obj.status != VocabRequestStatus.PENDING:
            if "proposed_categories" in form.base_fields:
                form.base_fields["proposed_categories"].disabled = True
        return form

    def log_review_result(self, *, request, review_action, vocab_request, result, level=logging.INFO):
        logger.log(
            level,
            "Vocab request review result: "
            "operation=%s reviewer_user_id=%s review_action=%s vocab_request_id=%s request_type=%s result=%s",
            "vocab_request_review",
            request.user.pk,
            review_action,
            vocab_request.pk,
            vocab_request.request_type,
            result,
        )

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            if obj.proposed_vocab_type != VocabType.VOCAB and obj.proposed_vocab_type != VocabType.KATAKANA:
                self.log_review_result(request=request, review_action="approve", vocab_request=obj, result="vocab type unsupported", level=logging.WARNING)
                return redirect(
                    reverse(
                        "admin:dictionary_vocabrequest_changelist"
                    )
                )
            if self.has_change_permission(request=request, obj=obj):
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
                    self.log_review_result(request=request, review_action="approve", vocab_request=obj, result="validation_rejected")
                    return redirect(
                        reverse(
                            "admin:dictionary_vocabrequest_change",
                            args=[obj.pk],
                        )
                    )
                if is_success:
                    self.log_review_result(request=request, review_action="approve", vocab_request=obj, result="approved")
                    self.message_user(
                        request,
                        f"Vocabulary request approved by {request.user}.",
                        messages.SUCCESS,
                    )
                else:
                    self.log_review_result(request=request, review_action="approve", vocab_request=obj, result="skipped")
                    self.message_user(
                        request,
                        f"This request has already been reviewed. No changes were made.",
                        messages.WARNING,
                    )
                return redirect(
                    reverse(
                        "admin:dictionary_vocabrequest_changelist"
                    )
                )
            else:
                self.log_review_result(request=request, review_action="approve", vocab_request=obj, result="permission_denied", level=logging.WARNING)
                return self.handle_no_change_permission(request=request, obj=obj)
        if "_reject" in request.POST:
            if self.has_change_permission(request=request, obj=obj):
                is_success = VocabRequestService.reject_vocab_request(
                    vocab_request=obj,
                    reviewed_by=request.user,
                )
                if is_success:
                    self.log_review_result(request=request, review_action="reject", vocab_request=obj, result="rejected")
                    self.message_user(
                        request,
                        f"Vocabulary request rejected by {request.user}.",
                        messages.WARNING,
                    )
                else:
                    self.log_review_result(request=request, review_action="reject", vocab_request=obj, result="skipped")
                    self.message_user(
                        request,
                        f"This request has already been reviewed. No changes were made.",
                        messages.WARNING,
                    )
                return redirect(
                    reverse(
                        "admin:dictionary_vocabrequest_changelist"
                    )
                )
            else:
                self.log_review_result(request=request, review_action="reject", vocab_request=obj, result="permission_denied", level=logging.WARNING)
                return self.handle_no_change_permission(request=request, obj=obj)
        return super().response_change(request, obj)

    def handle_no_change_permission(self, *, request, obj):
        self.message_user(
            request,
            "You do not have permission to review this request.",
            messages.ERROR,
        )
        return redirect(
            reverse(
                "admin:dictionary_vocabrequest_change",
                args=[obj.pk],
            )
        )

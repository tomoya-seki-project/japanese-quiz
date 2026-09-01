import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.utils import timezone

from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.decorators import method_decorator

from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
)
from django.views.generic.detail import DetailView

from .forms import (
    VocabCreateRequestForm,
    VocabUpdateRequestForm,
    VocabDeleteRequestForm,
    VocabSearchForm,
    UserVocabSearchForm,
    UserVocabSelectForm,
    UserVocabInUseUpdateForm,
    UserVocabInUseSingleUpdateForm,
    UserVocabInUse,
)
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
)

from .service.vocab_request import VocabRequestService
from .service.user_vocab_action import UserVocabService
from quiz.service.quiz import QuizService

logger = logging.getLogger(__name__)

class VocabHomeView(TemplateView):
    template_name = "dictionary/vocab_home.html"

class VocabCreateRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/vocab_create.html"
    form_class = VocabCreateRequestForm
    success_url = reverse_lazy("HomePage")

    def form_valid(self, form):
        self.has_restore_vocab = False
        if hasattr(form, "deactived_vocab"):
            self.has_restore_vocab = True
            try:
                created = VocabRequestService.gen_restore_vocab_request(
                    user=self.request.user,
                    vocab=form.deactived_vocab,
                )
            except ValidationError as e:
                form.add_error(None, e)
                logger.info(
                    "Vocab restoration request rejected by business validation: "
                    "operation=%s user_id=%s vocab_id=%s error=%s",
                    "vocab_request_restore",
                    self.request.user.pk,
                    form.deactived_vocab.pk,
                    e,
                )
                return self.form_invalid(form)
            if created:
                logger.info(
                    "Vocab restoration request created: "
                    "operation=%s user_id=%s vocab_id=%s",
                    "vocab_request_restore",
                    self.request.user.pk,
                    form.deactived_vocab.pk,
                )
                messages.success(self.request, "The same word already exists on the list. A restore request has been sent to admin for review.")
            else:
                logger.info(
                    "Vocab restoration request skipped: "
                    "operation=%s user_id=%s vocab_id=%s reason=%s",
                    "vocab_request_restore",
                    self.request.user.pk,
                    form.deactived_vocab.pk,
                    "pending_request_exists",
                )
                messages.info(self.request, "The same word already exists on the list, and a review request is already waiting for admin review.")
            return redirect(self.get_success_url())
        else:
            try:
                created = VocabRequestService.gen_create_vocab_request(
                    user=self.request.user,
                    form=form,
                )
            except ValidationError as e:
                form.add_error(None, e)
                logger.info(
                    "Vocab creation request rejected by business validation: "
                    "operation=%s user_id=%s word=%s kana=%s error=%s",
                    "vocab_request_create",
                    self.request.user.pk,
                    form.cleaned_data["word"],
                    form.cleaned_data["kana"],
                    e,
                )
                return self.form_invalid(form)
            if created:
                logger.info(
                    "Vocab creation request created: "
                    "operation=%s user_id=%s word=%s kana=%s",
                    "vocab_request_create",
                    self.request.user.pk,
                    form.cleaned_data["word"],
                    form.cleaned_data["kana"],
                )
                messages.success(self.request, "A new word request has been sent to admin for confirmation.")
            else:
                logger.info(
                    "Vocab creation request skipped: "
                    "operation=%s user_id=%s word=%s kana=%s reason=%s",
                    "vocab_request_create",
                    self.request.user.pk,
                    form.cleaned_data["word"],
                    form.cleaned_data["kana"],
                    "pending_request_exists",
                )
                messages.info(self.request, "Another user has already requested the same word. It is waiting for admin confirmation.")
            return redirect(self.get_success_url())

    def get_success_url(self):
        if getattr(self, "has_restore_vocab", False):
            return reverse_lazy("dictionary:vocab_home")
        return super().get_success_url()

class VocabUpdateRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/vocab_update.html"
    form_class = VocabUpdateRequestForm
    success_url = reverse_lazy("dictionary:vocab_home")

    @property
    def target_vocab(self):
        if not hasattr(self, "_target_vocab"):
            self._target_vocab = get_object_or_404(
                Vocab,
                is_active=True,
                pk = self.kwargs["vocab_id"]
            )
        return self._target_vocab

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["target_vocab"] = self.target_vocab
        return kwargs

    def get_initial(self):
        initial_data = super().get_initial()
        vocab = self.target_vocab
        initial_data.update({
            "vocab_type" : vocab.type,
            "word" : vocab.word,
            "meaning" : vocab.meaning,
            "kana" : vocab.kana,
            "level" : vocab.level,
            "categories" : vocab.categories.all(),
            #"similar_word" : vocab.similar_word
        })
        match vocab.type:
            case VocabType.VOCAB:
                pass
            case VocabType.KATAKANA:
                initial_data.update({
                    "native_japanese" : vocab.katakana_detail.native_japanese
                })
            # case VocabType.ADVERB | VocabType.MIMETIC | VocabType.CONJUNCTION | VocabType.COLLOQUIAL:
            #     pass
        return initial_data

    def form_valid(self, form):
        try:
            created = VocabRequestService.gen_update_vocab_request(
                user=self.request.user,
                form=form
            )
        except ValidationError as e:
            form.add_error(None, e)
            logger.info(
                "Vocab update request rejected by business validation: "
                "operation=%s user_id=%s vocab_id=%s error=%s",
                "vocab_request_update",
                self.request.user.pk,
                self.target_vocab.pk,
                e,
            )
            return self.form_invalid(form)
        if created:
            logger.info(
                "Vocab update request created: "
                "operation=%s user_id=%s vocab_id=%s",
                "vocab_request_update",
                self.request.user.pk,
                self.target_vocab.pk,
            )
        else:
            logger.info(
                "Vocab update request skipped: "
                "operation=%s user_id=%s vocab_id=%s reason=%s",
                "vocab_request_update",
                self.request.user.pk,
                self.target_vocab.pk,
                "pending_request_exists",
            )
        return super().form_valid(form)

class VocabDeleteRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/vocab_delete.html"
    form_class = VocabDeleteRequestForm
    success_url = reverse_lazy("dictionary:vocab_home")

    @property
    def target_vocab(self):
        if not hasattr(self, "_target_vocab"):
            self._target_vocab = get_object_or_404(
                Vocab,
                is_active=True,
                pk = self.kwargs["vocab_id"]
            )
        return self._target_vocab

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vocab"] = self.target_vocab
        return context

    def form_valid(self, form):
        try:
            created = VocabRequestService.gen_delete_vocab_request(
                user=self.request.user,
                vocab=self.target_vocab
            )
        except ValidationError as e:
            form.add_error(None, e)
            logger.info(
                "Vocab deletion request rejected by business validation: "
                "operation=%s user_id=%s vocab_id=%s error=%s",
                "vocab_request_delete",
                self.request.user.pk,
                self.target_vocab.pk,
                e,
            )
            return self.form_invalid(form)
        if created:
            logger.info(
                "Vocab deletion request created: "
                "operation=%s user_id=%s vocab_id=%s",
                "vocab_request_delete",
                self.request.user.pk,
                self.target_vocab.pk,
            )
        else:
            logger.info(
                "Vocab deletion request skipped: "
                "operation=%s user_id=%s vocab_id=%s reason=%s",
                "vocab_request_delete",
                self.request.user.pk,
                self.target_vocab.pk,
                "pending_request_exists",
            )
        return super().form_valid(form)


class VocabDetailView(DetailView):
    model = Vocab
    template_name = "dictionary/vocab_detail.html"
    context_object_name = "vocab"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["vocab"] = get_object_or_404(
    #         Vocab,
    #         pk = self.kwargs["vocab_id"]
    #     )
    #     return context


class VocabListView(ListView):
    model = Vocab
    template_name = "dictionary/vocab_list.html"
    context_object_name = "vocabs"
    ordering = ['pk',]
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = VocabSearchForm(
            self.request.GET
        )
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_string"] = query_params.urlencode()
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)

        form = VocabSearchForm(self.request.GET)

        if form.is_valid():

            word = form.cleaned_data.get("word")
            if word:
                qs = qs.filter(word__icontains=word)
            kana = form.cleaned_data.get("kana")
            if kana:
                qs = qs.filter(kana__icontains=kana)
            vocab_type = form.cleaned_data.get("vocab_type")
            if vocab_type:
                qs = qs.filter(type=vocab_type)
            lv = form.cleaned_data.get("level")
            if lv:
                qs = qs.filter(level=lv)
            category = form.cleaned_data.get("category")
            if category:
                qs = qs.filter(categories=category)

        return qs

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == "XMLHttpRequest":
            return render(self.request, 'dictionary/partials/vocab_list_partial.html', context)
        return super().render_to_response(context, **response_kwargs)

class UserVocabListView(LoginRequiredMixin, ListView):
    model = UserVocab
    template_name = 'dictionary/user_vocab_list.html'
    context_object_name = 'user_vocabs'
    ordering = ['pk',]
    paginate_by = 30

    def post(self, request, *args, **kwargs):
        user_vocab_queryset = self.get_queryset()

        form = UserVocabInUseUpdateForm(
            request.POST,
            user_vocab_queryset=user_vocab_queryset,
        )

        if form.is_valid():
            selectable_ids = form.cleaned_data["selectable_ids"]
            selected_ids = form.cleaned_data["selected_ids"]

            selectable_qs = UserVocab.objects.filter(
                user=request.user,
                id__in=selectable_ids,
            )

            get_unselect_qs = selectable_qs.filter(
                in_use=True,
            ).exclude(
                id__in=selected_ids,
            )
            get_select_qs = selectable_qs.filter(
                in_use=False,
                id__in=selected_ids,
            )
            now = timezone.now()
            deactivated_count = get_unselect_qs.update(in_use=False, update_at=now)
            activated_count = get_select_qs.update(in_use=True, update_at=now)
            if (activated_count + deactivated_count) > 0:
                logger.info(
                    "User vocab usage updated: "
                    "operation=%s user_id=%s activated_count=%s deactivated_count=%s",
                    "user_vocab_in_use",
                    self.request.user.pk,
                    activated_count,
                    deactivated_count,
                )
        return redirect(request.get_full_path())

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == "XMLHttpRequest":
            return render(self.request, 'dictionary/partials/user_vocab_list_partial.html', context)
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = UserVocabSearchForm(
            self.request.GET
        )

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context['query_string'] = query_params.urlencode()

        return context

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = UserVocab.objects.filter(user=self.request.user, vocab__is_active=True).select_related("vocab")
        form = UserVocabSearchForm(self.request.GET)

        if form.is_valid():

            is_use = form.cleaned_data.get("in_use")
            if is_use == UserVocabInUse.YES:
                qs = qs.filter(in_use=True)
            elif is_use == UserVocabInUse.NO:
                qs = qs.filter(in_use=False)

            word = form.cleaned_data.get("word")
            if word:
                qs = qs.filter(vocab__word__icontains=word)

            kana = form.cleaned_data.get("kana")
            if kana:
                qs = qs.filter(vocab__kana__icontains=kana)
            vocab_type = form.cleaned_data.get("vocab_type")
            if vocab_type:
                qs = qs.filter(vocab__type=vocab_type)
            lv = form.cleaned_data.get("level")
            if lv:
                qs = qs.filter(vocab__level=lv)
            category = form.cleaned_data.get("category")
            if category:
                qs = qs.filter(vocab__categories=category)

        return qs

class UserVocabDetailView(LoginRequiredMixin, DetailView):
    model = UserVocab
    template_name = "dictionary/user_vocab_detail.html"
    context_object_name = "user_vocab"

    def post(self, request, *args, **kwargs):
        user_vocab = self.get_object()

        form = UserVocabInUseSingleUpdateForm(
            request.POST
        )

        if form.is_valid():
            new_in_use = form.cleaned_data["in_use"]
            if user_vocab.in_use != new_in_use:
                user_vocab.in_use = new_in_use
                user_vocab.save(update_fields=["in_use","update_at"])

                logger.info(
                    "User vocab usage updated: "
                    "operation=%s user_id=%s vocab_id=%s in_use=%s",
                    "user_vocab_in_use",
                    self.request.user.pk,
                    user_vocab.vocab_id,
                    user_vocab.in_use,
                )

            return redirect(request.get_full_path())
        self.object = user_vocab
        context = self.get_context_data(object=user_vocab)
        context["in_use_form"] = form
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user_vocab = context["user_vocab"]
        if target_user_vocab.last_answer is not None:
            if target_user_vocab.vocab.type == VocabType.VOCAB or target_user_vocab.vocab.type == VocabType.KATAKANA:
                compared_data = QuizService.compare_kana_answer(
                                    correct_answer=target_user_vocab.vocab.kana,
                                    user_answer=target_user_vocab.last_answer
                                )
                compared_result = QuizService.gen_answer_image(compared_result=compared_data)
            else:
                compared_result = None

            if compared_result:
                context["compared_result"] = compared_result
        if "in_use_form" not in context:
            context["in_use_form"] = UserVocabInUseSingleUpdateForm(
                initial={"in_use":self.object.in_use}
            )
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, vocab__is_active=True)

class UserVocabSelectVocabView(LoginRequiredMixin, FormView):
    template_name = "dictionary/select_vocab.html"
    form_class = UserVocabSelectForm
    success_url = reverse_lazy("dictionary:user_vocab_list")

    def get_new_vocab(self):
        return UserVocabService.get_new_vocab(user=self.request.user,limit=50)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["vocab_queryset"] = self.get_new_vocab()
        return kwargs

    def form_valid(self, form):
        UserVocabService.create_user_vocabs(
            user=self.request.user,
            vocabs=form.cleaned_data["vocabs"],
        )
        return super().form_valid(form)


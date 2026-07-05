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
    UserVocabInUse,
)
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

from .service.vocab_request import VocabRequestService
from .service.user_vocab_action import UserVocabService

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
                return self.form_invalid(form)
            if created:
                messages.success(self.request, "There was the same word on the list, passed to admin to review")
            else:
                messages.info(self.request, "There was the same word on the list and We got the review request already, waiting for admin review")
            return redirect(self.get_success_url())
        else:
            try:
                created = VocabRequestService.gen_create_vocab_request(
                    user=self.request.user,
                    form=form,
                )
            except ValidationError as e:
                form.add_error(None, e)
                return self.form_invalid(form)
            if created:
                messages.success(self.request, "Created New Word request to admin, waiting for confirm")
            else:
                messages.info(self.request, "There are other user ask for the same word already, waiting for admin confirm")
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
            "category" : vocab.category, 
            #"similar_word" : vocab.similar_word
        })
        match vocab.type:
            case VocabType.VOCAB:
                pass
            case VocabType.KATAKANA:
                initial_data.update({
                    "native_japanese" : vocab.katakana_detail.native_japanese
                })
        return initial_data
    
    def form_valid(self, form):
        try:
            VocabRequestService.gen_update_vocab_request(
                user=self.request.user,
                form=form
            )
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
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
                pk = self.kwargs["vocab_id"]
            )
        return self._target_vocab

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vocab"] = self.target_vocab
        return context
    
    def form_valid(self, form):
        try:
            VocabRequestService.gen_delete_vocab_request(
                user=self.request.user,
                vocab=self.target_vocab
            )
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return super().form_valid(form)
    

class VocabDetailView(DetailView):
    model = Vocab
    template_name = "dictionary/vocab_detail.html"
    context_object_name = "vocab"

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
            lv = form.cleaned_data.get("level")
            if lv:
                qs = qs.filter(level=lv)
            category = form.cleaned_data.get("category")
            if category:
                qs = qs.filter(category=category)

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
            get_unselect_qs.update(in_use=False, update_at=now)
            get_select_qs.update(in_use=True, update_at=now)

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
            qs = UserVocab.objects.filter(user=self.request.user).select_related("vocab")
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
            lv = form.cleaned_data.get("level")
            if lv:
                qs = qs.filter(vocab__level=lv)
            category = form.cleaned_data.get("category")
            if category:
                qs = qs.filter(vocab__category=category)

        return qs
    
class UserVocabDetailView(LoginRequiredMixin, DetailView):
    model = UserVocab
    template_name = "dictionary/user_vocab_detail.html"
    context_object_name = "user_vocab"

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
    
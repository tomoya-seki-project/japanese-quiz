from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.decorators import method_decorator

from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
)

from ..forms import (
    VocabCreateRequestForm,
    VocabUpdateRequestForm,
    VocabDeleteRequestForm,
    VocabSearchForm,
)
from ..models import (
    Vocab,
    UserVocab,
    VocabType,
    VocabCategory,
    VocabLevel,
    KanjiDetail,
    KatakanaDetail,
    VocabRequest,
    VocabRequestStatus,
    VocabRequestType,
)

from .request import (
    genCreateVocabRequest,
    genUpdateVocabRequest,
    genDeleteVocabRequest,
    genRestoreVocabRequest,
)

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
            created = genRestoreVocabRequest(
                user=self.request.user,
                vocab=form.deactived_vocab,
            )
            if created:
                messages.success(self.request, "There was the same word on the list, passed to admin to review")
            else:
                messages.info(self.request, "There was the same word on the list and We got the review request already, waiting for admin review")
            return redirect(self.get_success_url())
        else:
            created = genCreateVocabRequest(
                user=self.request.user,
                form=form,
            )
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
        })
        match vocab.type:
            case VocabType.KANJI:
                initial_data.update({
                    "similar_kanji" : vocab.kanji_detail.similar_kanji
                })
            case VocabType.KATAKANA:
                initial_data.update({
                    "original_word" : vocab.katakana_detail.original_word,
                    "native_japanese" : vocab.katakana_detail.native_japanese
                })
        return initial_data
    
    def form_valid(self, form):
        genUpdateVocabRequest(
            user=self.request.user,
            form=form
        )
        return super().form_valid(form)

class VocabDeleteRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/vocab_delete.html"
    form_class = VocabDeleteRequestForm
    success_url = reverse_lazy("dictionary:vocab_home")

class VocabDetailView(TemplateView):
    template_name = "dictionary/vocab_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vocab"] = get_object_or_404(
            Vocab,
            pk = self.kwargs["vocab_id"]
        )
        return context
    

class VocabListView(ListView):
    model = Vocab
    template_name = "dictionary/vocab_list.html"
    context_object_name = "vocabs"
    ordering = ['pk',]
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = VocabSearchForm(
            self.request.GET
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()

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
    
class UserVocabListView(LoginRequiredMixin, ListView):
    model = UserVocab
    template_name = 'dictionary/user_vocab_list.html'
    context_object_name = 'vocabs'
    ordering = ['pk',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = VocabSearchForm(
            self.request.GET
        )
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = UserVocab.objects.filter(user=self.request.user).select_related("vocab")
        form = VocabSearchForm(self.request.GET)

        if form.is_valid():

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

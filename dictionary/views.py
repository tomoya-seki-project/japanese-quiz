from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.generic import (
    TemplateView,
    FormView,
)

from .forms import (
    VocabCreateForm
)
from .models import (
    Vocab,
    UserVocab,
    VocabType,
    VocabStatus,
    VocabCategory,
    VocabLevel,
    KanjiDetail,
    KatakanaDetail,
)

class VocabHomeView(TemplateView):
    template_name = "dictionary/vocab_home.html"

class VocabCreateView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_create.html"
    form_class = VocabCreateForm
    success_url = reverse_lazy("dictionary:vocab_home")

    def form_valid(self, form):
        # create vocab and {vocab}Detail
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if hasattr(form, "pending_vocab"):
            vocab = form.pending_vocab
            vocab.status = VocabStatus.PENDING
            vocab.save()
            # create admin message
        return super().form_invalid(form) 
    
class VocabEditView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_edit.html"
    
    
    

    

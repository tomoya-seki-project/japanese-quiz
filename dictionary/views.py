from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.decorators import method_decorator

from django.views.generic import (
    TemplateView,
    FormView,
)

from .forms import (
    VocabCreateRequestForm,
    VocabUpdateRequestForm,
    VocabDeleteRequestForm,
)
from .models import (
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

class VocabHomeView(TemplateView):
    template_name = "dictionary/vocab_home.html"

class VocabCreateRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_create.html"
    form_class = VocabCreateRequestForm
    success_url = reverse_lazy("dictionary:vocab_home")

    def form_valid(self, form):
        # create vocab and {vocab}Detail
        word = form.cleaned_data["word"]
        kana = form.cleaned_data["kana"]
        vocab_type = form.cleaned_data["vocab_type"]
        request = VocabRequest.objects.filter(
            request_type = VocabRequestType.CREATE,
            status = VocabRequestStatus.PENDING,
            proposed_word = word,
            proposed_kana = kana,
        ).first()
        if request:
            # messages and redirect
            messages.warning(self.request, "There are the same word on pending now")
        else:
            create_request = VocabRequest.objects.create(
                create_by = self.request.user,
                type = VocabRequestType.CREATE,
                status = VocabRequestStatus.PENDING,
                proposed_word = word,
                proposed_vocab_type = vocab_type,
                proposed_meaning = form.cleaned_data["meaning"],
                proposed_kana = kana,
                proposed_level = form.cleaned_data["level"],
                proposed_catagory = form.cleaned_data["catagory"]
            )
            match vocab_type:
                case VocabType.KANJI:
                    create_request.proposed_similar_word = form.cleaned_data["similar_word"]
                    create_request.save()
                case VocabType.KATAKANA:
                    create_request.proposed_original_word = form.cleaned_data["original_word"]
                    create_request.proposed_native_japanese = form.cleaned_data["native_japanese"]
                    create_request.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if hasattr(form, "deactived_vocab"):
            vocab = form.deactived_vocab
            vocab.save()
            # create admin message
        return super().form_invalid(form) 
    
class VocabUpdateRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_edit.html"
    success_url = reverse_lazy("dictionary:vocab_home")

class VocabDeleteRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_delete.html"
    success_url = reverse_lazy("dictionary:vocab_home")

class VocabDetailView(TemplateView):
    template_name = "dictionary/Vocab_detail.html"

    
    
    

    

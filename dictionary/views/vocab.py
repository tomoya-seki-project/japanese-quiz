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

from ..forms import (
    VocabCreateRequestForm,
    VocabUpdateRequestForm,
    VocabDeleteRequestForm,
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
    template_name = "dictionary/Vocab_create.html"
    form_class = VocabCreateRequestForm
    success_url = reverse_lazy("dictionary:vocab_home")

    def form_valid(self, form):
        has_restore_vocab = False
        if hasattr(form, "deactived_vocab"):
            has_restore_vocab = True
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
    template_name = "dictionary/Vocab_edit.html"
    success_url = reverse_lazy("dictionary:vocab_home")

class VocabDeleteRequestView(LoginRequiredMixin, FormView):
    template_name = "dictionary/Vocab_delete.html"
    success_url = reverse_lazy("dictionary:vocab_home")

class VocabDetailView(TemplateView):
    template_name = "dictionary/Vocab_detail.html"

    
    
    

    

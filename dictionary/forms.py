from django import forms

from django.core.exceptions import ValidationError

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

class BaseVocabRequestForm(forms.Form):
    #--- vocab table ---#
    vocab_type = forms.ChoiceField(choices=VocabType.choices, label='type')
    word = forms.CharField(max_length=50, label='Word')
    meaning = forms.CharField(max_length=255, label="Meaning")
    kana = forms.CharField(max_length=255, label='Kana')
    level = forms.ChoiceField(choices=VocabLevel.choices)
    category = forms.ChoiceField(choices=VocabCategory.choices)
    similar_word = forms.CharField(max_length=255, required=False)

    #--- kanji detail table ---#
    #nothing special right now
    
    #--- katakana detail table ---#
    native_japanese = forms.CharField(max_length=255, required=False)

class VocabCreateRequestForm(BaseVocabRequestForm):
    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).first()

        if existing_vocab:
            if existing_vocab.is_active:
                self.add_error('word', 'There is the same word on the list and active.')
            else:
                self.deactived_vocab = existing_vocab

        return cleaned_data
    
class VocabUpdateRequestForm(BaseVocabRequestForm):
    def __init__(self, *args, target_vocab=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_vocab = target_vocab

    def clean(self):
        cleaned_data = super().clean()

        if self.target_vocab is None:
            raise ValidationError("Target vocab is missing")
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')
        pk = cleaned_data.get('pk')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).exclude(pk=self.target_vocab.pk).first()

        if existing_vocab:
            self.add_error('word', 'There is the same word on the list and active')

        return cleaned_data

class VocabDeleteRequestForm(forms.Form):
    confirm = forms.BooleanField(required=False)

    def clean_confirm(self):
        confirm = self.cleaned_data.get("confirm")
        if confirm == False:
            raise ValidationError("Please confirm the action")
        return confirm

class VocabSearchForm(forms.Form):
    word = forms.CharField(max_length=50, required=False)
    kana = forms.CharField(max_length=255, required=False)
    level = forms.ChoiceField(
        choices=[("","-----")] + list(VocabLevel.choices),
        required=False,
    )
    category = forms.ChoiceField(
        choices=[("","-----")] + list(VocabCategory.choices),
        required=False,
    )

from django import forms

from django.core.exceptions import ValidationError

from .models import (
    Vocab,
    VocabCategory,
    VocabLevel,
    VocabType,
    UserVocab,
    KanjiDetail,
    KatakanaDetail,
    VocabRequest,
    VocabRequestType,
    VocabRequestStatus
)

class BaseVocabRequestForm(forms.Form):
    #--- vocab table ---#
    vocab_type = forms.ChoiceField(choices=VocabType.choices, label='type')
    word = forms.CharField(max_length=50, label='Word')
    meaning = forms.CharField(max_length=255, label="Meaning")
    kana = forms.CharField(max_length=255, label='Kana')
    level = forms.ChoiceField(choices=VocabLevel.choices)
    category = forms.ChoiceField(choices=VocabCategory.choices)

    #--- kanji detail table ---#
    similar_kanji = forms.CharField(max_length=255, required=False)
    
    #--- katakana detail table ---#
    original_word = forms.CharField(max_length=255, required=False)
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
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')
        pk = cleaned_data.get('pk')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).exclude(pk=self.target_vocab.pk).first()

        if existing_vocab:
            self.add_error('word', 'There is the same word on the list and active')

        return cleaned_data

class VocabDeleteRequestForm(forms.Form):
    pass
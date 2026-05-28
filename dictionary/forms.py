from django import forms

from django.core.exceptions import ValidationError

from .models import (
    Vocab,
    VocabCategory,
    VocabLevel,
    VocabStatus,
    VocabType,
    UserVocab,
    KanjiDetail,
    KatakanaDetail,
)

class VocabCreateForm(forms.Form):
    #--- vocab table ---#
    type = forms.ChoiceField(choices=VocabType.choices)
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

    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).first()

        if existing_vocab:
            if existing_vocab.is_active:
                self.add_error('word', 'There is the same word on the list and active.')
            else:
                self.add_error(None, 'There was the same word on the list, Passed to the admin to review.')
                self.pending_vocab = existing_vocab

        return cleaned_data
from django import forms

from django.core.exceptions import ValidationError

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

class BaseVocabRequestForm(forms.Form):
    # Vocab fields
    vocab_type = forms.ChoiceField(choices=VocabType.choices, label='種類')
    word = forms.CharField(max_length=50, label='単語')
    meaning = forms.CharField(max_length=255, label="意味")
    kana = forms.CharField(max_length=255, label='読み方（かな）')
    level = forms.ChoiceField(label="JLPTレベル", choices=VocabLevel.choices)
    # similar_word = forms.CharField(max_length=255, required=False)

    categories = forms.ModelMultipleChoiceField(label="カテゴリー",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    # Kanji detail fields
    # No special fields right now.

    # Katakana detail fields
    native_japanese = forms.CharField(label="対応する日本語表現", max_length=255, required=False)

    def clean_vocab_type(self):
        vocab_type = self.cleaned_data.get("vocab_type")
        if vocab_type != VocabType.VOCAB and vocab_type != VocabType.KATAKANA:
            raise forms.ValidationError(
                "この単語の種類には対応していません。"
            )
        return vocab_type

    def clean_categories(self):
        categories = self.cleaned_data["categories"]
        if categories.count() > 3:
            raise forms.ValidationError(
                "カテゴリーは3つまで選択できます。"
            )
        return categories

class VocabCreateRequestForm(BaseVocabRequestForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["meaning"].required = False
        self.fields["level"].required = False

    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).first()

        if existing_vocab:
            if existing_vocab.is_active:
                self.add_error('word', '同じ単語と読み方の有効な項目がすでに登録されています。')
            else:
                self.deactived_vocab = existing_vocab

        return cleaned_data

class VocabUpdateRequestForm(BaseVocabRequestForm):
    def __init__(self, *args, target_vocab=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_vocab = target_vocab
        self.fields["vocab_type"].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        if self.target_vocab is None:
            raise ValidationError("更新対象の単語が見つかりません。")
        word = cleaned_data.get('word')
        kana = cleaned_data.get('kana')
        pk = cleaned_data.get('pk')

        existing_vocab = Vocab.objects.filter(word=word, kana=kana).exclude(pk=self.target_vocab.pk).first()

        if existing_vocab:
            if existing_vocab.is_active:
                self.add_error('word', '同じ単語と読み方の有効な項目がすでに登録されています。')
            else:
                self.add_error('word', '同じ単語と読み方の無効な項目がすでに登録されています。')

        return cleaned_data

class VocabDeleteRequestForm(forms.Form):
    confirm = forms.BooleanField(label="削除申請を確認しました", required=False)

    def clean_confirm(self):
        confirm = self.cleaned_data.get("confirm")
        if confirm == False:
            raise ValidationError("この単語の削除を申請する場合は、確認欄にチェックを入れてください。")
        return confirm

class VocabSearchForm(forms.Form):
    word = forms.CharField(label="単語", max_length=50, required=False)
    kana = forms.CharField(label="読み方（かな）", max_length=255, required=False)
    vocab_type = forms.ChoiceField(
        choices=[("","すべて")] + VocabType.choices,
        required=False,
        label="種類",
    )
    level = forms.ChoiceField(label="JLPTレベル",
        choices=[("","すべて")] + VocabLevel.choices,
        required=False,
    )
    category = forms.ModelChoiceField(label="カテゴリー",
        queryset=Category.objects.all(),
        required=False,
        empty_label="すべて"
    )
class UserVocabInUse:
    NO_MATTER = ""
    YES = "yes"
    NO = "no"
    choices = [
        (NO_MATTER, "すべて"),
        (YES, "はい"),
        (NO, "いいえ"),
    ]

class UserVocabSearchForm(forms.Form):
    in_use = forms.ChoiceField(label="出題対象",
        choices=UserVocabInUse.choices,
        required=False,
    )
    word = forms.CharField(label="単語", max_length=50, required=False)
    kana = forms.CharField(label="読み方（かな）", max_length=255, required=False)
    vocab_type = forms.ChoiceField(
        choices=[("","すべて")] + VocabType.choices,
        required=False,
        label="種類",
    )
    level = forms.ChoiceField(label="JLPTレベル",
        choices=[("","すべて")] + VocabLevel.choices,
        required=False,
    )
    category = forms.ModelChoiceField(label="カテゴリー",
        queryset=Category.objects.all(),
        required=False,
        empty_label="すべて",
    )

class UserVocabSelectForm(forms.Form):
    vocabs = forms.ModelMultipleChoiceField(label="単語帳",
        queryset=Vocab.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, vocab_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if vocab_queryset is not None:
            self.fields["vocabs"].queryset = vocab_queryset

class UserVocabInUseUpdateForm(forms.Form):
    selectable_ids = forms.ModelMultipleChoiceField(
        queryset=UserVocab.objects.none(),
        required=False,
    )
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=UserVocab.objects.none(),
        required=False,
    )

    def __init__(self, *args, user_vocab_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user_vocab_queryset is not None:
            self.fields["selectable_ids"].queryset = user_vocab_queryset
            self.fields["selected_ids"].queryset = user_vocab_queryset

class UserVocabInUseSingleUpdateForm(forms.Form):
    in_use = forms.BooleanField(label="出題対象", required=False)

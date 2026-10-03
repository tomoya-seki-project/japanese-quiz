from django import forms

from django.core.exceptions import ValidationError

from dictionary.models import (
    VocabType,
    VocabLevel,
    Category,
)

class QuizSettingForm(forms.Form):
    quiz_num = forms.TypedChoiceField(label="問題数",
        choices=[(10,"10"), (20,"20"), (30, "30")],
        coerce=int,
        required=False,
        empty_value=-1,
    )
    vocab_type = forms.MultipleChoiceField(
        choices=VocabType.choices,
        required=False,
        label="種類",
        widget= forms.CheckboxSelectMultiple,
    )
    level = forms.MultipleChoiceField(label="JLPTレベル",
        choices=VocabLevel.choices,
        required=False,
        widget= forms.CheckboxSelectMultiple,
    )
    categories = forms.ModelMultipleChoiceField(label="カテゴリー",
        queryset=Category.objects.all(),
        required=False,
        widget = forms.CheckboxSelectMultiple,
    )

class QuizForm(forms.Form):
    user_vocab_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.CharField(max_length=25, required=True, widget=forms.HiddenInput)
    tips_count = forms.IntegerField(min_value=0, max_value=50, widget=forms.HiddenInput)
    attempt_token = forms.UUIDField(widget=forms.HiddenInput)

class QuizAttemptForm(forms.Form):
    attempt_token = forms.UUIDField(widget=forms.HiddenInput)
    tips_count = forms.IntegerField(min_value=0, max_value=50, widget=forms.HiddenInput)
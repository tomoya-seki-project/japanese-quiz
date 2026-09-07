from django import forms

from django.core.exceptions import ValidationError

from dictionary.models import (
    VocabType,
    VocabLevel,
    Category,
)

class QuizSettingForm(forms.Form):
    quiz_num = forms.TypedChoiceField(label="問題数",
        choices=[(-1,"無制限"), (10,"10"), (20,"20"), (30, "30")],
        coerce=int,
        required=True,
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
    use_last_setting = forms.BooleanField(label="前回の設定を使用", required=False)

class QuizForm(forms.Form):
    user_vocab_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.CharField(max_length=25, required=True, widget=forms.HiddenInput)
    tips_count = forms.IntegerField(min_value=0, max_value=50, widget=forms.HiddenInput)

class QuizNextForm(forms.Form):
    pass

class QuizSkipForm(forms.Form):
    pass

class QuizSummaryForm(forms.Form):
    pass

class QuizFullPoolConfirmForm(forms.Form):
    pass

from django import forms

from django.core.exceptions import ValidationError

from dictionary.models import (
    VocabType,
    VocabLevel,
    Category,
)

class QuizSettingForm(forms.Form):
    quiz_num = forms.TypedChoiceField(
        choices=[(-1,"No Limit"), (10,"10"), (20,"20"), (30, "30")],
        coerce=int,
        required=True,
    )
    vocab_type = forms.MultipleChoiceField(
        choices=VocabType.choices,
        required=False,
        label="Type",
        widget= forms.CheckboxSelectMultiple,
    )
    level = forms.MultipleChoiceField(
        choices=VocabLevel.choices,
        required=False,
        widget= forms.CheckboxSelectMultiple,
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget = forms.CheckboxSelectMultiple,
    )
    use_last_setting = forms.BooleanField(required=False)

class QuizForm(forms.Form):
    user_vocab_id = forms.IntegerField(widget=forms.HiddenInput)
    answer = forms.CharField(max_length=50, required=True, widget=forms.HiddenInput)
    tips_count = forms.IntegerField(min_value=0, max_value=50, widget=forms.HiddenInput)

class QuizNextForm(forms.Form):
    pass

class QuizSkipForm(forms.Form):
    pass

class QuizSummaryForm(forms.Form):
    pass

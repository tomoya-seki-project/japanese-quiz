from django import forms

from .models import UserEvent, FeedbackType

class UserEventIsReadedUpdateForm(forms.Form):
    selectable_ids = forms.ModelMultipleChoiceField(
        queryset=UserEvent.objects.none(),
        required=False,
    )
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=UserEvent.objects.none(),
        required=False,
    )

    def __init__(self, *args, user_event_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user_event_queryset is not None:
            self.fields["selectable_ids"].queryset = user_event_queryset
            self.fields["selected_ids"].queryset = user_event_queryset

class FeedbackCreateForm(forms.Form):
    feedback_type = forms.ChoiceField(label="種類", choices=FeedbackType.choices)
    context = forms.CharField(label="内容", max_length=255, widget=forms.Textarea)

class FeedbackReplyForm(forms.Form):
    is_close = forms.BooleanField(label="終了", required=False)
    context = forms.CharField(label="返信内容", max_length=255, widget=forms.Textarea)

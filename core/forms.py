from django import forms

from .models import Event, UserEvent, FeedbackType, Feedback

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
    feedback_type = forms.ChoiceField(choices=FeedbackType.choices)
    context = forms.CharField(max_length=255, widget=forms.Textarea)

class FeedbackReplyForm(forms.Form):
    context = forms.CharField(max_length=255, widget=forms.Textarea)
from django import forms

from .models import Event, UserEvent

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
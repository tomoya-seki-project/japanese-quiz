from django import forms

from .models import Event, UserEvent, FAQType, FAQ

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

class FAQCreateForm(forms.Form):
    FAQ_TYPE = forms.ChoiceField(choices=FAQType.choices)
    context = forms.CharField(max_length=255, widget=forms.Textarea)

class FAQReplyForm(forms.Form):
    context = forms.Textarea()
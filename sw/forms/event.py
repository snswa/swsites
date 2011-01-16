from django import forms
from django.forms.widgets import DateInput

from dregni.forms import EventForm as BaseEventForm


class EventForm(BaseEventForm):

    start_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(required=False, widget=DateInput(attrs={'class': 'datepicker'}))

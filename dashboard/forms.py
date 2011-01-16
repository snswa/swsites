from django import forms

from sw.fields import JqSplitDateTimeField
from sw.widgets import JqSplitDateTimeWidget


class DigestRangeForm(forms.Form):
    """A range of dates for showing in a digest."""

    start_date = JqSplitDateTimeField(
        widget=JqSplitDateTimeWidget(
            attrs=dict(date_class='datepicker', time_class='timepicker'),
        ),
    )
    end_date = JqSplitDateTimeField(
        widget=JqSplitDateTimeWidget(
            attrs=dict(date_class='datepicker', time_class='timepicker'),
        ),
    )

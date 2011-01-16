# http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/

from time import strftime

from django.db import models
from django import forms
from django.forms.widgets import Select, MultiWidget, DateInput, TextInput
from django.template.loader import render_to_string


class JqSplitDateTimeWidget(MultiWidget):

    def __init__(self, attrs=None, date_format=None, time_format=None):
        date_class = attrs['date_class']
        time_class = attrs['time_class']
        del attrs['date_class']
        del attrs['time_class']

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        widgets = (DateInput(attrs=date_attrs, format=date_format),
                   TextInput(attrs=time_attrs), TextInput(attrs=time_attrs),
                   Select(attrs=attrs, choices=[('AM','AM'),('PM','PM')]))

        super(JqSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, tuple) and len(value) == 1:
                value = value[0]
            d = strftime("%Y-%m-%d", value.timetuple())
            hour = strftime("%I", value.timetuple())
            minute = strftime("%M", value.timetuple())
            meridian = strftime("%p", value.timetuple())
            return (d, hour, minute, meridian)
        else:
            return (None, None, None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "Date: %s<br/>Time: %s:%s %s" % (rendered_widgets[0], rendered_widgets[1],
                                                rendered_widgets[2], rendered_widgets[3])

    class Media:
        css = {
            }
        js = (
            )

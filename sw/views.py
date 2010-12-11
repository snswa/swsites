from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from actstream import action

from sw.tasks import report_ok

from teams.models import Team

from wakawaka.models import WikiPage


def report_ok_view(request):
    content = report_ok.delay().get()
    return HttpResponse(content, mimetype='text/plain')

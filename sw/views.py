from django.http import HttpResponse

from sw.tasks import report_ok
from django.shortcuts import render_to_response
from django.template.context import RequestContext




def report_ok_view(request):
    content = report_ok.delay().get()
    return HttpResponse(content, mimetype='text/plain')

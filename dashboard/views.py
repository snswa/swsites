from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    template_name = 'dashboard/index.html'
    template_context = {}
    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

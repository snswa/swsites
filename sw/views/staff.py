import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from django.contrib.auth.models import User


def allvolunteers(request, template_name="staff/allvolunteers.html", extra_context=None, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied()
    extra_context = extra_context or {}
    now = datetime.datetime.now()
    template_context = dict(
        extra_context,
        now=now,
        user_list=User.objects.order_by('profile__last_name', 'profile__first_name', 'profile__preferred_name', 'username'),
    )
    response = render_to_response(template_name, template_context, RequestContext(request))
    if request.GET.get('excel') == '1':
        filename = 'sensible_washington_all_volunteers_{0}.xls'.format(now.strftime('%Y%m%d-%H%M%S'))
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    return response

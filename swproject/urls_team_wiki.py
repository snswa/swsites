from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from wakawaka.urls import decorated_urlpatterns


def require_team_membership_if_private(fn):
    @login_required
    def view(request, *args, **kw):
        if (request.group is not None
            and (request.group.user_is_member(request.user)
                 or not request.group.is_private)
            ):
            return fn(request, *args, **kw)
        return HttpResponseForbidden("You don't have permission to view this page.")
    return view


urlpatterns = decorated_urlpatterns(require_team_membership_if_private)

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect


class HqPredicateMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        login_required = view_kwargs.pop('login_required', False)
        email_required = view_kwargs.pop('email_required', False)
        profile_required = view_kwargs.pop('profile_required', False)
        #
        # Check for login necessity first.
        if login_required:
            if not request.user.is_authenticated():
                return HttpResponseRedirect(
                    reverse('account_login')
                    + '?next={0}'.format(request.META['PATH_INFO'])
                )
            # Check for private team membership.
            if (request.group is not None
                and getattr(request.group, 'is_private', False)
                and not request.group.user_is_member(request.user)
                ):
                return HttpResponseForbidden("You don't have permission to view this page.")

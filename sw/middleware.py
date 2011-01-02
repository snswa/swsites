from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect


class HqPredicateMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        login_required = view_kwargs.pop('login_required', False)
        email_preferred = view_kwargs.pop('email_preferred', False)
        email_required = view_kwargs.pop('email_required', False)
        profile_preferred = view_kwargs.pop('profile_preferred', False)
        profile_required = view_kwargs.pop('profile_required', False)
        #
        # Pass-through quickly if no requirements or preferences.
        if not (login_required or email_preferred or email_required or profile_preferred or profile_required):
            return
        #
        # Check for login requirement first.
        request.missing_info = {}
        if login_required:
            if not request.user.is_authenticated():
                return HttpResponseRedirect(
                    reverse('account_login')
                    + '?next={0}'.format(request.META['PATH_INFO'])
                )
        #
        # Check for other requirements.
        user = request.user
        if user.is_authenticated():
            profile = user.get_profile()
            has_verified_email = user.emailaddress_set.filter(verified=True).count() > 0
            has_preferred_name = profile.preferred_name and profile.preferred_name.strip()
            has_zip_code = profile.zip_code and profile.zip_code.strip()
        else:
            has_verified_email = False
            has_preferred_name = False
            has_zip_code = False
        #
        if not user.is_superuser:
            # Redirect to profile edit if profile is not complete.
            if (profile_required
                and not (has_preferred_name and has_zip_code)
                and not request.GET.get('gather_profile', False)
                ):
                return HttpResponseRedirect(
                    reverse('profile_edit')
                    + '?gather_profile=1'
                )
            #
            # Redirect to email if no verified email.
            if (email_required
                and not has_verified_email
                and not request.GET.get('gather_email', False)
                ):
                return HttpResponseRedirect(
                    reverse('account_email')
                    + '?gather_email=1'
                )
        #
        # Check for private team membership.
        if (request.group is not None
            and getattr(request.group, 'is_private', False)
            and not request.group.user_is_member(request.user)
            ):
            return HttpResponseForbidden("You don't have permission to view this page.")
        #
        # Set up missing info for nags.
        request.missing_info = {
            'email': not has_verified_email,
            'preferred_name': not has_preferred_name,
            'zip_code': not has_zip_code,
        }

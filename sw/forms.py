import re

from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from allauth.account.forms import SignupForm


class HqSignupForm(SignupForm):

    preferred_name = forms.CharField(
        label=_("Preferred Name"),
        help_text=_('This is how your name will appear to other volunteers.'),
        max_length=50,
        widget=forms.TextInput(),
    )
    zip_code = forms.CharField(
        label=_("ZIP Code"),
        max_length=30,
        help_text=_('If you are outside the U.S., please enter the name of your location instead.')
    )
    email = forms.EmailField(
        widget=forms.TextInput(),
        help_text=_('We keep your contact information private. You can change privacy settings after signing up.'),
    )
    # Needs to be new_ prefixed so as to not collide with a login form on
    # the same page.
    new_username = forms.CharField(
        label=_("Username"),
        help_text=_('The account name you use to log into the website.'),
        max_length=30,
        widget=forms.TextInput(),
    )
    password1 = forms.CharField(
        label=_("Password"),
        help_text=_('Choose a strong password to help prevent identity theft.'),
        widget=forms.PasswordInput(render_value=False),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False),
    )

    def __init__(self, *args, **kwargs):
        super(HqSignupForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'preferred_name',
            'zip_code',
            'email',
            'new_username',
            'password1',
            'password2',
        ]

    def clean(self):
        super(HqSignupForm, self).clean()
        self.cleaned_data['username'] = self.cleaned_data['new_username']
        return self.cleaned_data

    def after_signup(self, user, **kwargs):
        # Put everything into the user's profile.
        profile = user.get_profile()
        profile.preferred_name = self.cleaned_data['preferred_name']
        profile.zip_code = self.cleaned_data['zip_code']
        profile.save()

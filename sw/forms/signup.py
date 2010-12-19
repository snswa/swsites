import re

from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from allauth.account.forms import SignupForm


class HqSignupForm(SignupForm):

    preferred_name = forms.CharField(
        label=_("Preferred Name"),
        help_text=_('How your name will appear to other volunteers. Example: Your first name, or a personal nickname.'),
        max_length=50,
        widget=forms.TextInput(),
    )
    zip_code = forms.CharField(
        label=_("ZIP Code"),
        max_length=30,
        help_text=_('Outside the U.S.? Please name your location instead.')
    )
    email = forms.EmailField(
        widget=forms.TextInput(),
        help_text=_('Used to verify the account and receive email updates.'),
    )
    phone_number = forms.CharField(
        label=_("Phone Number"),
        help_text=_('Strongly preferred.'),
        max_length=20,
        widget=forms.TextInput(),
        required=False,
    )
    # Needs to be new_ prefixed so as to not collide with a login form on
    # the same page.
    new_username = forms.CharField(
        label=_("Username"),
        help_text=_('The account name you will use to log into the website.'),
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
            'phone_number',
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
        profile.phone_number = self.cleaned_data['phone_number']
        profile.save()

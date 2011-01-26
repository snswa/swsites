import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from allauth.account.forms import SignupForm

from sw.models import Profile
from sw.decorators import autostrip


def username_not_in_use(username):
    if User.objects.filter(username__iexact=username).exists():
        raise forms.ValidationError('This username is already in use.')


@autostrip
class HqSignupForm(SignupForm):

    # Needs to be new_ prefixed so as to not collide with a login form on
    # the same page.
    new_username = forms.RegexField(
        label=_("Username"),
        help_text=_('The account name you will use to log into the website.'),
        max_length=30,
        regex=r'^[\w\._-]+$',
        error_messages=dict(
            invalid='Your username may not contain spaces. Use only letters, numbers, periods, underscores, and dashes.',
        ),
        validators=[
            username_not_in_use,
        ],
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
    preferred_name = forms.CharField(
        label=_("Preferred Name"),
        help_text=_('How your name will appear to other volunteers. Example: Your first name, or a personal nickname. Leave blank to use your username.'),
        max_length=50,
        required=False,
        widget=forms.TextInput(),
    )
    zip_code = forms.CharField(
        label=_("ZIP Code"),
        max_length=30,
        help_text=_('Outside the U.S.? Please name your location instead.'),
    )
    email = forms.EmailField(
        widget=forms.TextInput(),
        help_text=_('Used to verify the account and receive email updates.'),
    )
    email_delivery = forms.ChoiceField(choices=Profile.EMAIL_DELIVERY_CHOICES, initial='00/48')
    phone_number = forms.CharField(
        label=_("Phone Number"),
        help_text=_('Strongly preferred. Available to coordinators only until you change privacy settings.'),
        max_length=20,
        widget=forms.TextInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(HqSignupForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'new_username',
            'password1',
            'password2',
            'preferred_name',
            'zip_code',
            'email',
            'email_delivery',
            'phone_number',
        ]

    def clean(self):
        super(HqSignupForm, self).clean()
        if 'new_username' in self.cleaned_data:
            self.cleaned_data['username'] = self.cleaned_data['new_username']
        return self.cleaned_data

    def after_signup(self, user, **kwargs):
        # Put everything into the user's profile.
        preferred_name = self.cleaned_data['preferred_name']
        profile = user.get_profile()
        if preferred_name:
            profile.preferred_name = preferred_name
        else:
            profile.preferred_name = self.cleaned_data['new_username']
        profile.zip_code = self.cleaned_data['zip_code']
        profile.phone_number = self.cleaned_data['phone_number']
        profile.email_delivery = self.cleaned_data['email_delivery']
        profile.save()

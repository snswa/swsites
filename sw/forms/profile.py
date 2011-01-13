from django import forms

from idios.utils import get_profile_form
from sw.decorators import autostrip
from sw.models import Interest
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML


BaseProfileForm = get_profile_form()


@autostrip
class ProfileForm(BaseProfileForm):

    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)

    helper = FormHelper()

    layout = Layout(
        Fieldset('Online Name/Nickname',
            'preferred_name',
        ),
        Fieldset('Real Name',
            Row('first_name', 'last_name'),
            'name_privacy',
        ),
        Fieldset('More about yourself',
            'zip_code',
            'zip_code_privacy',
            'interests',
            'interests_privacy',
            'bio',
            'bio_privacy',
        ),
        Fieldset('Email',
            'email_privacy',
        ),
        Fieldset('Phone',
            'phone_number',
            'phone_number_accepts_texts',
            'phone_number_privacy',
        ),
        Fieldset('Instant messaging',
            'yahoo_messenger',
            'aim',
            'msn_messenger',
            'skype',
            'messaging_privacy',
        ),
        Fieldset('Address',
            'mailing_address',
            'mailing_address_privacy',
        ),
        Fieldset('Preferences',
            'preferred_contact_methods',
            'preferred_contact_methods_privacy',
        ),
        Fieldset('Profession / Occupation',
            'occupation',
            'occupation_privacy',
            'employer',
            'employer_privacy',
        ),
        Fieldset('Union Outreach',
            'union_name',
            'union_local_number',
            'union_privacy',
        ),
    )
    helper.add_layout(layout)
    submit = Submit('save', 'Save profile')
    helper.add_input(submit)

    def save(self, *args, **kw):
        # If we already have an instance, override commit so we can
        # save interests set by the user.
        if self.instance:
            kw['commit'] = True
        return super(ProfileForm, self).save(*args, **kw)

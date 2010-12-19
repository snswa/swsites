from idios.utils import get_profile_form

from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML


BaseProfileForm = get_profile_form()
class ProfileForm(BaseProfileForm):

    helper = FormHelper()

    layout = Layout(
        Fieldset('Name',
            'preferred_name',
            Row('first_name', 'last_name'),
            'name_privacy',
        ),
        Fieldset('Location',
            'zip_code',
            'zip_code_privacy',
            'mailing_address',
            'mailing_address_privacy',
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
        Fieldset('Preferences',
            'preferred_contact_methods',
            'preferred_contact_methods_privacy',
        ),
        Fieldset('More about yourself',
            'bio',
            'bio_privacy',
        ),
    )
    helper.add_layout(layout)
    submit = Submit('save', 'Save profile')
    helper.add_input(submit)
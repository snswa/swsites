import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery.decorators import task
from dashboard import digests
from emailconfirmation.models import EmailAddress


@task
def send_email(user_id, start_date, end_date):
    user = User.objects.get(pk=user_id)
    print 'Found user', user
    # First find the user's verified, primary email address.
    primary_email = EmailAddress.objects.get_primary(user)
    print 'Primary email', primary_email
    if not primary_email or not primary_email.verified:
        # No email found; skip.
        return
    # Now see if there are any updates.
    template_context = digests.daily_context(user, start_date, end_date)
    if not template_context['any_with_activity']:
        # No activity found; skip.
        return
    # Build email.
    print 'Building email'
    html_content = render_to_string('dashboard/digest_html.html', template_context)
    text_content = render_to_string('dashboard/digest_plaintext.txt', template_context)
    # Send email.
    print 'Sending email'
    subject = '[Volunteer HQ] Updates for {0}'.format(start_date.date())
    from_email = 'webmaster@sensiblewashington.org'
    to_email = primary_email.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@task
def send_emails_to_schedule(schedule):
    hour, frequency = schedule.split('/')
    hour, frequency = int(hour), int(frequency)
    frequency /= 24
    now = datetime.datetime.now()
    if now.date().toordinal() % frequency != 0:
        # Every other day schedule only on even numbered days
        # according to Gregorian ordinal.
        return
    end_date = datetime.datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    start_date = end_date - datetime.timedelta(days=frequency)
    for user in User.objects.filter(profile__email_delivery=schedule):
        print 'Will possibly send email to', user
        send_email.delay(user.id, start_date, end_date)

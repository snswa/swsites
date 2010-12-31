from django.core import management

from celery.decorators import task


@task
def report_ok():
    return 'OK'


@task
def update_all_planet_feeds():
    management.call_command('update_all_feeds')

@task
def update_planet_feed(url):
    management.call_command('update_feed', url)

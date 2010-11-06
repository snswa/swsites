from celery.decorators import task


@task
def report_ok():
    return 'OK'

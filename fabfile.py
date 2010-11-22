import django

from fabric.api import cd, env, local, require, run, sudo


env.repo = 'http://github.com/snswa/swsites.git'
env.srcdir = '~/src'
env.settings_module = 'snswa_deploy.localsettings'


def _admin():
    require('settings_module')
    return 'PYTHONPATH=$HOME DJANGO_SETTINGS_MODULE={0} ~/src/env/bin/django-admin.py'.format(env.settings_module)


def update_repo():
    require('repo', 'srcdir')
    with cd('~'):
        run(
            'if [ ! -d {srcdir:>s}/.git ]; then '
                'git clone {repo:>s} {srcdir:>s};'
                'cd {srcdir:>s} && git checkout --track origin/deploy; '
            'else '
                'echo already cloned; '
            'fi'
            .format(srcdir=env.srcdir, repo=env.repo)
        )


def pull_deploy():
    require('srcdir')
    with cd(env.srcdir):
        run('git checkout deploy')
        run('git pull')


def prepare_virtualenv():
    require('srcdir')
    with cd(env.srcdir):
        run('if [ ! -d env ]; then virtualenv -p python2.6 env; env/bin/pip install -U -e hg+http://bitbucket.org/gldnspud/pip-sw#egg=pip; fi')
        run('PATH=/usr/local/pgsql/bin:$PATH env/bin/pip install -r requirements.txt')
        run('env/bin/python2.6 setup.py develop')


def sync_and_migrate():
    require('srcdir')
    run('{0} syncdb --migrate --noinput'.format(_admin()))


def collectstatic():
    require('srcdir')
    if django.VERSION >= (1, 3):
        run('{0} collectstatic --noinput --link'.format(_admin()))
    else:
        run('{0} build_static --noinput --link'.format(_admin()))


def restart_app_server():
    require('srcdir')
    with cd(env.srcdir):
        run('production/supervisord.sh reload')


def rebuild_solr_schema():
    require('srcdir')
    with cd(env.srcdir):
        run('{0} build_solr_schema > ~/solr-schema.xml'.format(_admin()))
        run('sudo /etc/init.d/jetty stop')
        run('sudo /etc/init.d/jetty start')


def rebuild_search_index():
    require('srcdir')
    rebuild_solr_schema()
    with cd(env.srcdir):
        run('{0} rebuild_index --noinput'.format(_admin()))


def deploy():
    update_repo()
    pull_deploy()
    prepare_virtualenv()
    sync_and_migrate()
    collectstatic()
    restart_app_server()

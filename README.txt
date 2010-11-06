Base VM installation
====================

You don't need to worry about this if you received a prepared VM.

Install Ubuntu Server 10.04.1 32-bit

Network: bridged

Host name: swdev

User: user
Password: password

Install security updates automatically

Reboot

Login

$ sudo aptitude update
$ sudo aptitude -y dist-upgrade
$ sudo aptitude -y install build-essential
$ sudo reboot

Install parallels tools

$ sudo mount /dev/cdrom /cdrom
$ cd /cdrom
$ sudo ./install --install-unattended-with-deps
$ cd

Install packages

$ sudo aptitude install openssh-server avahi-daemon

Ssh to user@swdev.local

$ sudo aptitude install \
emacs-snapshot-nox \
python-mode \
vim-nox \
screen \
libjpeg62-dev \
mercurial \
bzr \
git-core \
apache2 \
apache2-mpm-prefork \
subversion \
libpq-dev \
build-essential \
python2.6-dev \
python-setuptools \
postgresql \
libpq5 \
postgresql-client-8.4 \
postgresql-common \
postgresql-client-common \
postgresql-contrib-8.4 \
avahi-daemon \
phppgadmin \
samba

edit /etc/samba/smb.conf

[homes]
   comment = Home Directories
   browseable = no
   read only = no
   create mask = 0640
   directory mask = 0750

$ sudo service smbd restart


Prepare postgres to allow 'user' as superuser
---------------------------------------------

$ sudo -u postgres createuser user
superuser? y


Install virtualenv and pip
--------------------------

$ sudo easy_install pip
$ sudo pip install virtualenv virtualenvwrapper
$ cat >> .bashrc <<EOF
source /usr/local/bin/virtualenvwrapper.sh
EOF
$ mkdir .virtualenvs
$ exec bash -login


Installation atop base VM
=========================


Install SSH key, change password
--------------------------------

$ ssh-copy-id user@swdev.local
$ ssh user@swdev.local
$ passwd
$ sudo smbpasswd user


Connect using Mac
-----------------

In Finder, Cmd+K or use menu: Go -> Connect to Server.

smb://swdev.local/user

This lets you access home directory using your favorite Mac editor.


Set up git
----------

$ git config --global user.name "Your Name"
$ git config --global user.email "your@email.com"
$ git config --global http.sslVerify 0


Clone repository, install dependencies
--------------------------------------

$ mkvirtualenv --no-site-packages sw
$ cat >> $VIRTUAL_ENV/bin/postactivate <<EOF
export DJANGO_SETTINGS_MODULE=swproject.localsettings
EOF
$ workon sw
$ pip install -U -e hg+http://bitbucket.org/gldnspud/pip-sw#egg=pip
$ git clone https://USER:PASS@git.sensiblewashington.org/swsites.git
$ cd swsites
$ pip install -r requirements.txt
$ python setup.py develop


Set up localsettings
--------------------

$ cd swproject
$ cat > localsettings.py <<EOF
from swproject.settings_dev import *
EOF


Create and initialize db and superuser
--------------------------------------

$ createdb -E utf8 -T template0 swdev
$ django-admin.py syncdb --migrate --noinput
$ django-admin.py createsuperuser
user: (your choice)
pass: (your choice)


Run server and browse against it
--------------------------------

$ django-admin.py runserver 0.0.0.0:8000

Browse to http://swdev.local:8000




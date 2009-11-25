#!/usr/bin/python

from fabric.api import *

# GLOBALS

env.project_name = 'votersdaily_web'

# ENVIRONMENTS
    
def testenv():
    """
    Configure for local test environment.
    """
    env.hosts = ['192.168.0.11']
    env.user = 'sk'
    env.path = '/home/%(user)s/%(project_name)s' % env

# COMMANDS

def setup():
    """
    Install Apache and other requirements, create a fresh virtualenv, and make
    required directories.
    """
    require('hosts', provided_by=[testenv])
    require('path', provided_by=[testenv])
    
    apt_install('python-setuptools')
    easy_install('pip')
    pip_install('virtualenv')
    apt_install('apache2')
    apt_install('libapache2-mod-wsgi')
    
    apt_install('couchdb')
    
    with cd('/etc/couchdb'):
        sudo('cp local.ini local.ini.bak')
        sudo("sed 's/;bind_address = 127.0.0.1/bind_address = 0.0.0.0/' <local.ini.bak > local.ini")
        sudo('/etc/init.d/couchdb restart')
    
    sudo('cd /etc/apache2/sites-available/; a2dissite default;', pty=True)
    sudo('mkdir -p %(path)s; chown %(user)s:%(user)s %(path)s;' % env, pty=True)
    
    with cd(env.path):
        run('virtualenv .;', pty=True)
        run('mkdir logs; chmod a+w logs;' % env, pty=True)

def deploy():
    """
    Deploy the project onto the target environment. Assumes setup() has already
    been run.
    """
    require('hosts', provided_by=[testenv])
    require('path', provided_by=[testenv])
    
    upload_tar_from_git()
    install_requirements()
    install_site()
    restart_webserver()
    
# UTILITIES

def apt_install(package):
    """
    Install a single package on the remote server with Apt.
    """
    sudo('aptitude install -y %s' % package)

def easy_install(package):
    """
    Install a single package on the remote server with easy_install.
    """
    sudo('easy_install %s' % package)

def pip_install(package):
    """
    Install a single package on the remote server with pip.
    """
    sudo('pip install %s' % package)

def upload_tar_from_git():
    """
    Create a tar archive from the current git master branch and upload it.
    """    
    local('git archive --format=tar master | gzip > upload.tar.gz')
    put('upload.tar.gz', '%(path)s' % env)
    
    with cd(env.path):
        run('tar zxf upload.tar.gz', pty=True)
        
    local('rm upload.tar.gz')
    
def install_requirements():
    """
    Install the required packages from the requirements file using pip.
    """    
    with cd(env.path):
        run('pip install -E . -r requirements.txt', pty=True)
    
def install_site():
    """
    Add the virtualhost configuration file to Apache."
    """    
    with cd(env.path):
        run("sed 's/{PROJECT_PATH}/%s/' <vhost.conf > vhost.local.conf" % env.path.replace('/', '\/'))
        sudo('cp vhost.local.conf /etc/apache2/sites-available/%(project_name)s' % env)
        
    with cd('/etc/apache2/sites-available/'):
        sudo('a2ensite %(project_name)s' % env, pty=True)
    
def restart_webserver():
    """
    Restart Apache.
    """    
    sudo('/etc/init.d/apache2 reload', pty=True)
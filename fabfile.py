#!/usr/bin/python

from fabric.api import *

# GLOBALS

env.project_name = 'votersdaily_web'

# ENVIRONMENTS
    
def testenv():
    env.hosts = ['192.168.0.11']
    env.user = 'sk'
    env.path = '/home/%(user)s/%(project_name)s' % env

# DEPLOYMENTS

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', provided_by=[testenv])
    require('path', provided_by=[testenv])
    
    sudo('aptitude install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    #sudo('aptitude install -y apache2-threaded')
    #sudo('aptitude install -y libapache2-mod-wsgi') # beware, outdated on hardy!
    # we want to get rid of the default apache config
    #sudo('cd /etc/apache2/sites-available/; a2dissite default;', pty=True)
    sudo('mkdir -p %(path)s; chown %(user)s:%(user)s %(path)s;' % env, pty=True)
    with cd(env.path):
        run('virtualenv .;', pty=True)
        run('mkdir logs; chmod a+w logs;' % env, pty=True)

def deploy():
    require('hosts', provided_by=[testenv])
    require('path', provided_by=[testenv])
    
    upload_tar()
    install_requirements()
    #install_site()
    restart_webserver()
    
# UTILITIES

def upload_tar():
    """
    Create an archive from the current Git master branch and upload it
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
    "Add the virtualhost file to apache"
    require('release', provided_by=[deploy, setup])
    
    sudo('cd %(path)s; cp vhost.conf /etc/apache2/sites-available/%(project_name)s' % env)
    sudo('cd /etc/apache2/sites-available/; a2ensite %(project_name)s' % env, pty=True)
    
def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 reload', pty=True)
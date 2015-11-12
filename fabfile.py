from __future__ import print_function
import os

from fabric import api
import cfg


api.env.hosts = [cfg.DEPLOY_HOST]


def buildenv():
    try:
        os.makedirs(cfg.ENV_DIR)
    except OSError:
        pass
    with api.settings(warn_only=True):
        api.local('pyvenv %s' % cfg.ENV_DIR, capture=False)
    api.local('%s/bin/easy_install pip' % cfg.ENV_DIR, capture=False)
    api.local('%s/bin/pip install -r cfg/pipreq.txt' % cfg.ENV_DIR,
              capture=False)


def pull():
    api.local('git pull ssh://%s/%s' % (cfg.DEPLOY_HOST, cfg.DEPLOY_PATH))


def deploy_fix():
    api.local("git ci -am'little fix'")
    api.local('fab deploy')


def deploy():
    push()
    build_webassets()
    restart()


def build_webassets():
    with api.cd(cfg.DEPLOY_PATH):
        api.run('./bin/build_webassets.py')


def restart():
    with api.cd(cfg.DEPLOY_PATH):
        api.run('sudo supervisorctl restart %s' % cfg.SUPERVISOR_NAME)


def push():
    api.local('git push')
    with api.cd(cfg.DEPLOY_PATH):
        api.run('git pull')


def log():
    with api.cd(cfg.DEPLOY_PATH):
        api.run('tail -n50 -f %s' % cfg.LOG_FILE_NAME)


def rm_log():
    with api.cd(cfg.DEPLOY_PATH):
        api.run('rm %s' % cfg.LOG_FILE_NAME)
    restart()


def uplib(name):
    for line in open('cfg/pipreq.txt'):
        if name in line:
            api.local('%s/bin/pip install --upgrade --force %s' % (
                cfg.ENV_DIR, line.strip()))


def s():
    api.local('nodemon ./server.py --exec "var/env/bin/python"'
              ' --ext "py html yaml" --ignore "static var"')


def freeze():
    api.local('./var/env/bin/pip freeze')

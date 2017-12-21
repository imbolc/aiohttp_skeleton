import os

from fabric import api
import cfg
from cfg import ENV_DIR, DEPLOY_USER, DEPLOY_HOST, DEPLOY_PATH


api.env.hosts = [f'{DEPLOY_USER}@{DEPLOY_HOST}']


def install():
    os.makedirs(ENV_DIR, exist_ok=True)
    os.makedirs('./var/log', exist_ok=True)
    os.makedirs('./var/webasset-cache', exist_ok=True)
    with api.settings(warn_only=True):
        api.local(f'python -m venv {ENV_DIR}', capture=False)
    api.local(f'{ENV_DIR}/bin/pip install -r cfg/requirements.txt',
              capture=False)
    api.local(f'cd static; npm i')


def pull():
    api.local(f'git pull {DEPLOY_USER}@{DEPLOY_HOST}:{DEPLOY_PATH}')


def fix():
    api.local("git ci -am'Fix'")
    api.local('fab deploy')


def deploy():
    push()
    push_assets()
    restart()


def push_assets():
    api.local('./bin/build_webassets.py')
    path = 'static'
    dst = f'{DEPLOY_USER}@{DEPLOY_HOST}:{DEPLOY_PATH}/{path}'
    api.local(f'rsync -rP {path}/dist {dst}')


def restart():
    with api.cd(DEPLOY_PATH):
        api.run(f'sudo supervisorctl restart {cfg.SUPERVISOR_NAME}')


def push():
    api.local('git push')
    with api.cd(DEPLOY_PATH):
        api.run('git pull')


def log():
    with api.cd(DEPLOY_PATH):
        api.run(f'tail -n50 -f {cfg.LOGGING_FILENAME}')


def uplib(name):
    for line in open('cfg/requirements.txt'):
        line = line.strip()
        if not line or line.startswith('#') or name not in line:
            continue
        api.local(f'{ENV_DIR}/bin/pip install --upgrade --force {line}')


def s():
    #  api.local(f'./var/env/bin/adev runserver -v -p{cfg.PORT}')
    api.local('./static/node_modules/nodemon/bin/nodemon.js '
              './app.py --exec "var/env/bin/python" '
              '--ext "py yaml sql" '
              '--ignore static/ --ignore var/')


def pulldb():
    fname = 'var/db.dump.gz'
    dbname = cfg.DATABASE.split('/')[-1]
    with api.cd(DEPLOY_PATH):
        api.run(f'pg_dump {dbname} -c -Z9 > {fname}')
    api.local(f'rsync -P {DEPLOY_HOST}:{DEPLOY_PATH}/{fname} ./var/')
    api.local(f'gunzip -c {fname} | psql {dbname}')

    path = 'static/media'
    api.local(f'rm -r {path}')
    api.local(f'rsync -rP {DEPLOY_HOST}:{DEPLOY_PATH}/{path}/ {path}/')

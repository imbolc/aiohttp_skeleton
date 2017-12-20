import os

from fabric import api
import cfg


api.env.hosts = [cfg.DEPLOY_HOST]


def install():
    os.makedirs(cfg.ENV_DIR, exist_ok=True)
    os.makedirs('./var/log', exist_ok=True)
    os.makedirs('./var/webasset-cache', exist_ok=True)
    with api.settings(warn_only=True):
        api.local(f'python -m venv {cfg.ENV_DIR}', capture=False)
    api.local(f'{cfg.ENV_DIR}/bin/pip install -r cfg/requirements.txt',
              capture=False)
    api.local(f'cd static; npm i')


def pull():
    api.local(f'git pull {cfg.DEPLOY_HOST}:{cfg.DEPLOY_PATH}')


def fix():
    api.local("git ci -am'Fix'")
    api.local('fab deploy')


def deploy():
    push()
    push_assets()
    restart()


def push_assets():
    api.local('./bin/build_webassets.py')
    path = 'static/assets'
    fname = path + '/build'
    api.local(f'rsync -rP {fname} {cfg.DEPLOY_HOST}:{cfg.DEPLOY_PATH}/{path}')


def restart():
    with api.cd(cfg.DEPLOY_PATH):
        api.run(f'sudo supervisorctl restart {cfg.SUPERVISOR_NAME}')


def push():
    api.local('git push')
    with api.cd(cfg.DEPLOY_PATH):
        api.run('git pull')


def log():
    with api.cd(cfg.DEPLOY_PATH):
        api.run(f'tail -n50 -f {cfg.LOGGING_FILENAME}')


def uplib(name):
    for line in open('cfg/requirements.txt'):
        line = line.strip()
        if not line or line.startswith('#') or name not in line:
            continue
        api.local(f'{cfg.ENV_DIR}/bin/pip install --upgrade --force {line}')


def s():
    #  api.local(f'./var/env/bin/adev runserver -v -p{cfg.PORT}')
    api.local('nodemon '
              './app.py --exec "var/env/bin/python" '
              '--ext "py yaml sql" '
              '--ignore static/ --ignore var/')


def pulldb():
    fname = 'var/db.dump.gz'
    dbname = cfg.DATABASE.split('/')[-1]
    with api.cd(cfg.DEPLOY_PATH):
        api.run(f'pg_dump {dbname} -c -Z9 > {fname}')
    api.local(f'rsync -P {cfg.DEPLOY_HOST}:{cfg.DEPLOY_PATH}/{fname} ./var/')
    api.local(f'gunzip -c {fname} | psql {dbname}')

    path = 'static/media'
    api.local(f'rm -r {path}')
    api.local(f'rsync -rP {cfg.DEPLOY_HOST}:{cfg.DEPLOY_PATH}/{path}/ {path}/')

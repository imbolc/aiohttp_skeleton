#!var/env/bin/python
from _setup import call
import sys

import cfg


COMMAND = '''
    ./var/env/bin/certbot {}
        --config-dir=./var/certbot/cfg
        --work-dir=./var/certbot/work
        --logs-dir=./var/log/certbot
        --renew-hook "sudo /etc/init.d/nginx reload"
'''
COMMAND = ' '.join(COMMAND.split())


def obtain():
    command = COMMAND.format(
        f'certonly --webroot -w ./static/root -d {cfg.HOST} -d www.{cfg.HOST}')
    call(command)
    print('Do not forget to add RENEW command to your CRONTAB:')
    print(f'15 4 * * *  cd {cfg.ROOT}; timeout 10m ./bin/certbot.py renew')


def renew():
    command = COMMAND.format('renew')
    call(command)


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['obtain', 'renew']:
        print(f'Usage: `{__file__} obtain` or `{__file__} renew`')
        sys.exit(1)
    globals()[sys.argv[1]]()

import os
import sys
from contextlib import contextmanager


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def echo(color, message):
    prefix = {'ok': '3;32;107', 'bug': '3;31;107', 'dim': '2;37;39'}[color]
    print(f'\033[{prefix}m{message}\033[0m')


@contextmanager
def sudo():
    try:
        yield
    except PermissionError:
        echo('bug', 'Permission error, try it with sudo')
        sys.exit(1)


def call(command):
    echo('dim', f'[call] {command}')
    code = os.system(command)
    if code:
        echo('bug', ' BUG ')
        sys.exit(code)
    echo('ok', ' O.K. ')

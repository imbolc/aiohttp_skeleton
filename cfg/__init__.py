DEBUG = False

TEMPLATE_AUTO_RELOAD = False
TEMPLATE_PATH = './templates'

HOST = 'site.com'
PORT = 8000

LOG_FILE_NAME = './var/log/site.log'
LOG_FILE_LEVEL = 'ERROR'
LOG_CONSOLE_LEVEL = 'ERROR'
LOG_LEVELS = {
    'asyncio': 'warn',
    'aiohttp': 'warn',
}

ENV_DIR = 'var/env'

DEPLOY_HOST = HOST
DEPLOY_PATH = HOST

SUPERVISOR_NAME = HOST
SUPERVISOR_USER = 'user'


try:
    from .local import *  # noqa
except ImportError:
    pass

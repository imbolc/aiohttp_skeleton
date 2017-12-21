from pathlib import Path


DEBUG = False

TEMPLATE_AUTO_RELOAD = False
TEMPLATE_PATH = './templates'

HOST = 'site.com'
PORT = 8000

ROOT = Path('__file__').resolve().parent
ENV_DIR = 'var/env'
DEPLOY_HOST = HOST
DEPLOY_PATH = HOST

SUPERVISOR_NAME = HOST
SUPERVISOR_USER = 'user'

LOGGING_FILENAME = './var/log/site.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOGGING_FILENAME,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 1,
        }
    },
    'loggers': {
        'asyncio': {
            'level': 'WARNING',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'aiohttp': {
            'level': 'WARNING',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}

try:
    from .local import *  # noqa
except ImportError:
    pass

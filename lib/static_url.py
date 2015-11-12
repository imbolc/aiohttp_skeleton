import os
import hashlib
import logging
import functools


log = logging.getLogger(__name__)


def static_url(filename, static_path='static'):
    filename = os.path.join(static_path, filename)
    return '/%s?v=%s' % (filename, get_version(filename))


@functools.lru_cache()
def get_version(filename):
    log.info('Calculate version hash for file: %s', filename)
    with open(filename, 'rb') as f:
        content = f.read()
    hasher = hashlib.md5()
    hasher.update(content)
    return hasher.hexdigest()[-5:]

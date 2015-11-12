import os
import json
import logging
import functools

import yaml


log = logging.getLogger(__name__)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def from_root(path):
    return os.path.join(ROOT, *path.split('/'))


def read_text(filename, *, encoding='utf-8'):
    with open(filename, encoding=encoding) as f:
        return f.read()


def read_json(filename):
    return json.loads(read_text(filename))


def read_yaml(filename):
    return yaml.load(read_text(filename))


def read(filename):
    ext = filename.split('.')[-1]
    reader = {
        'json': read_json,
        'yaml': read_yaml,
    }.get(ext, read_text)
    return reader(filename)


@functools.lru_cache(maxsize=None)
def read_cached(filename):
    log.debug('import file: ' + filename)
    return read(filename)


def write_text(filename, text, *, encoding='utf-8', makedirs=True):
    if makedirs:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    with open(filename, 'w', encoding=encoding) as f:
        return f.write(text)


def write_json(filename, data, **json_kwargs):
    write_text(filename, json.dumps(data, **json_kwargs))

import os
from zlib import adler32
import mimetypes
import hashlib
import logging
import functools

from aiohttp.web import Response


log = logging.getLogger(__name__)


async def middleware(app, handler):
    '''This middleware is not either safe nor fast enough for production'''
    async def static(request):
        url = request.path
        filename = url[1:]
        if filename:
            filename = secure_filename(filename)
            filename = os.path.join('./static', filename)
            if os.path.isfile(filename):
                return sendfile(filename)
        return await handler(request)
    return static


def secure_filename(path):
    return path.lstrip('/').replace('../', '')


def sendfile(location, mimetype=None, add_etags=True):
    headers = {}
    filename = os.path.split(location)[-1]

    with open(location, 'rb') as ins_file:
        out_stream = ins_file.read()

    if add_etags:
        headers['ETag'] = '{}-{}-{}'.format(
            int(os.path.getmtime(location)),
            hex(os.path.getsize(location)),
            adler32(location.encode('utf-8')) & 0xffffffff)

    mimetype = mimetype or mimetypes.guess_type(filename)[0] or 'text/plain'

    return Response(status=200,
                    headers=headers,
                    content_type=mimetype,
                    body=out_stream)


def static_url(url):
    filename = 'static' + url
    hash = file_version(filename)
    return f'{url}?v={hash}'


@functools.lru_cache()
def file_version(filename):
    log.debug('Calculate version hash for file: %s', filename)
    return file_hash(filename)[-5:]


def file_hash(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

'''
Helpers for aiohttp.web
'''
from functools import wraps

from aiohttp import web
import ujson as json

import cfg


APP = None
DEFAULT = object()


def setup(app):
    global APP
    APP = app


def url_for(urlname, **kwargs):
    return APP.router[urlname].url_for(**kwargs)


def get_argument(container, name, default=DEFAULT, *, cls=None):
    arg = container.get(name, default)
    if name not in container:
        if default is not DEFAULT:
            return default
        raise web.HTTPBadRequest(
            reason='Missing required argument: {}'.format(name))
    if cls:
        try:
            arg = cls(arg)
        except Exception:
            raise web.HTTPBadRequest(
                reason='Argument is incorrect: {}'.format(name))
    return arg


def json_dumps(data, **kwargs):
    params = {
        'indent': 4 if cfg.DEBUG else 0,
        'ensure_ascii': False,
    }
    params.update(kwargs)
    return json.dumps(data, **params)


def json_response(data, **kwargs):
    kwargs['content_type'] = kwargs.get('content_type', 'application/json')
    return web.Response(text=json_dumps(data), **kwargs)


def jsonify(handler, *args, **kwargs):
    @wraps(handler)
    async def wrapper(request):
        response = await handler(request)
        if isinstance(response, web.StreamResponse):
            return response
        return json_response(response, *args, **kwargs)
    return wrapper


async def trailing_slash_middleware(app, handler):
    async def middleware(request):
        try:
            response = await handler(request)
        except web.HTTPNotFound as e:
            if not request.path.endswith('/'):
                raise web.HTTPFound(request.path + '/')
            raise e
        return response
    return middleware


def get_client_ip(request):
    try:
        return request.headers['X-Forwarded-For']
    except KeyError:
        return request.transport.get_extra_info('peername')[0]

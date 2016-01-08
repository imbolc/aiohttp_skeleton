'''
Helpers for aiohttp.web
'''
from aiohttp import web

from object_by_name import object_by_name
import asjson

import cfg


APP = None
DEFAULT = object()


def setup(app):
    global APP
    APP = app


def url(method, path, handler, name=None):
    handler = object_by_name(handler)
    APP.router.add_route(method, path, handler, name=name)


def url_for(urlname, *, query_=None, **parts):
    url = APP.router[urlname].url
    return url(parts=parts, query=query_) if parts else url(query=query_)


def get_argument(container, name, default=DEFAULT, *, cls=None):
    arg = container.get(name, default)
    if arg is DEFAULT:
        raise web.HTTPBadRequest(
            reason='Missing required argument: {}'.format(name))
    if cls:
        try:
            arg = cls(arg)
        except Exception:
            raise web.HTTPBadRequest(
                reason='Argument is incorrect: {}'.format(name))
    return arg


def jsonify(handler_or_data, *args, **kwargs):
    f = jsonify_decortor if callable(handler_or_data) else jsonify_function
    return f(handler_or_data, *args, **kwargs)


def jsonify_function(data, debug=False, **kwargs):
    json_debug = debug or cfg.DEBUG
    text = asjson.dumps(data, debug=json_debug)
    kwargs['content_type'] = kwargs.get('content_type', 'application/json')
    return web.Response(text=text, **kwargs)


def jsonify_decortor(handler, *args, **kwargs):
    async def wrapper(request):
        response = await handler(request)
        if isinstance(response, web.StreamResponse):
            return response
        return jsonify_function(response, *args, **kwargs)
    return wrapper


async def remove_trailing_slash_middleware(app, handler):
    async def middleware(request):
        try:
            response = await handler(request)
        except web.HTTPNotFound as e:
            if request.path.endswith('/') and request.path != '/':
                raise web.HTTPFound(request.path[:-1])
            else:
                raise e
        return response
    return middleware


def get_client_ip(request):
    try:
        return request.headers['X-Forwarded-For']
    except KeyError:
        return request.transport.get_extra_info('peername')[0]

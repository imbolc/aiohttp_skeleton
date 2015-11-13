'''
Helpers for aiohttp.web
'''
import json
from aiohttp import web

import ujson
from object_by_name import object_by_name

from .serialize import datetime_to_iso


APP = None


def setup(app):
    global APP
    APP = app


def url(method, path, handler, name=None):
    handler = object_by_name(handler)
    APP.router.add_route(method, path, handler, name=name)


def url_for(urlname, *, query_=None, **parts):
    url = APP.router[urlname].url
    return url(parts=parts, query=query_) if parts else url(query=query_)


def get_qs_argument(request, *args, **kwargs):
    return _get_argument(request.GET, *args, **kwargs)


def get_url_argument(request, *args, **kwargs):
    return _get_argument(request.match_info, *args, **kwargs)


def _get_argument(container, name, default=None, *, cls=None):
    arg = container.get(name, default)
    if arg is None:
        raise web.HTTPBadRequest(
            reason='Missing required argument: {}'.format(name))
    if cls:
        try:
            arg = cls(arg)
        except Exception:
            raise web.HTTPBadRequest(
                reason='Argument is incorrect: {}'.format(name))
    return arg


def json_dumps(data, convert_datetime=True):
    if convert_datetime:
        data = datetime_to_iso(data)
    if APP['cfg'].DEBUG:
        text = json.dumps(data, ensure_ascii=False, indent=4)
    else:
        text = ujson.dumps(data, ensure_ascii=False)
    return text


def jsonify(data, convert_datetime=True, **kwargs):
    kwargs['content_type'] = kwargs.get('content_type', 'application/json')
    text = json_dumps(data, convert_datetime)
    return web.Response(text=text, **kwargs)

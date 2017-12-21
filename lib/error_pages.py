import asyncio
import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp_jinja2 import template

import cfg


log = logging.getLogger(__name__)
SUPPRESS_LOGGING_FOR_EXCEPTIONS = (
    HTTPMethodNotAllowed,
    asyncio.CancelledError,
)


async def middleware(app, handler):
    async def process(request):
        try:
            response = await handler(request)
        except (web.HTTPSuccessful, web.HTTPRedirection):
            raise
        except web.HTTPNotFound as e:
            response = await error404(request)
            response.set_status(e.status_code)
        except SUPPRESS_LOGGING_FOR_EXCEPTIONS as e:
            if cfg.DEBUG:
                raise e
            response = await error5xx(request)
            response.set_status(get_error_status_code(e))
        except Exception as e:
            if cfg.DEBUG:
                raise e
            code = get_error_status_code(e)
            log.error('Error [code={}, method={}, url={}]'.format(
                code, request.method, request.path), exc_info=e)
            response = await error5xx(request)
            response.set_status(code)
        return response
    return process


def get_error_status_code(e):
    return e.status_code if isinstance(e, web.HTTPError) else 500


@template('error_pages/404.html')
async def error404(request):
    return {}


@template('error_pages/5xx.html')
async def error5xx(request):
    return {}

#!var/env/bin/python
import os
import asyncio
import datetime
import logging.config

from aiohttp import web
import setproctitle
import jinja2
import aiohttp_jinja2
import webassets.loaders
from object_by_name import object_by_name
import misaka
import asjson

import cfg
import lib.web
import lib.jinja
from lib.static_url import static_url
import apps.errors


setproctitle.setproctitle(cfg.HOST)

os.makedirs(os.path.dirname(cfg.LOGGING_FILENAME), exist_ok=True)
logging.config.dictConfig(cfg.LOGGING)


async def create_app(loop):
    app = web.Application(loop=loop, middlewares=[
        apps.errors.middleware,
        lib.web.remove_trailing_slash_middleware,
    ])

    lib.web.setup(app)
    setup_routes(app)
    jinja_env = setup_jinja(app)
    setup_webassets(jinja_env)
    return app


def setup_routes(app):
    url = lib.web.url

    url('GET', '/', 'apps.home.home')
    url('GET', '/api/now', 'apps.api.now', name='api__now')

    app.router.add_static('/static', './static')


def setup_jinja(app):
    env = aiohttp_jinja2.setup(
        app,
        loader=lib.jinja.AppsLoader(cfg.TEMPLATE_PATH),
        auto_reload=cfg.TEMPLATE_AUTO_RELOAD,
        extensions=[
            'jinja2.ext.with_',
        ]
    )

    env.globals.update({
        'str': str,
        'enumerate': enumerate,
        'datetime': datetime,
        'len': len,

        'cfg': cfg,
        'static_url': static_url,
        'url_for': lib.web.url_for,
    })
    env.filters['json'] = lambda data: asjson.dumps(data, debug=cfg.DEBUG)
    env.filters['markdown'] = misaka.html

    return env


def setup_webassets(jinja_env):
    env = webassets.loaders.YAMLLoader(
        'cfg/webassets.yaml').load_environment()
    env.debug = cfg.DEBUG
    jinja_env.globals['webassets'] = env


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(loop))

    handler = app.make_handler(debug=cfg.DEBUG)
    srv = loop.run_until_complete(
        loop.create_server(handler, '127.0.0.1', cfg.PORT))
    print('Serving at http://{}:{}/'.format(*srv.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()

#!var/env/bin/python
import asyncio
import logging.config
from contextlib import suppress

import uvloop
import setproctitle
from aiohttp import web

import cfg
import lib

import routes
import lib.error_pages
import lib.static


setproctitle.setproctitle(cfg.HOST)
logging.config.dictConfig(cfg.LOGGING)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def create_app():
    app = web.Application(middlewares=[
        lib.error_pages.middleware,
        lib.web.trailing_slash_middleware,
        lib.static.middleware,
    ])

    lib.web.setup(app)
    lib.jinja.setup(app)
    routes.setup(app)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())

    handler = app.make_handler(debug=cfg.DEBUG)
    f = loop.create_server(handler, '0.0.0.0', cfg.PORT)
    srv = loop.run_until_complete(f)
    print('Serving at http://{}:{}/'.format(*srv.sockets[0].getsockname()))

    with suppress(KeyboardInterrupt):
        loop.run_forever()
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(handler.shutdown(60.0))
    loop.run_until_complete(app.cleanup())
    loop.close()

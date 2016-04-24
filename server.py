#!var/env/bin/python
import os
import asyncio
import logging.config

from aiohttp import web
import setproctitle

import cfg
import cfg.jinja

import routes
import middlewares.error_pages


setproctitle.setproctitle(cfg.HOST)

os.makedirs(os.path.dirname(cfg.LOGGING_FILENAME), exist_ok=True)
logging.config.dictConfig(cfg.LOGGING)


async def create_app(loop):
    app = web.Application(loop=loop, middlewares=[
        middlewares.error_pages.middleware,
        lib.web.remove_trailing_slash_middleware,
    ])

    lib.web.setup(app)
    cfg.jinja.setup(app)
    routes.setup(app)
    return app


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

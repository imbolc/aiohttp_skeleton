import handlers.home
import handlers.api


def setup(app):
    url = app.router.add_route

    url('GET',  '/', handlers.home.home, name='home')
    url('GET', '/api/now', handlers.api.now, name='api_now')

    app.router.add_static('/static', './static')

import handlers


def setup(app):
    url = app.router.add_route

    url('GET',  '/', handlers.home, name='home')

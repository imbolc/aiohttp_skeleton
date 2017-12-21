from aiohttp_jinja2 import template


@template('home.html')
async def home(request):
    return {}

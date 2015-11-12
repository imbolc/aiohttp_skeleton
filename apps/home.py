import logging

from aiohttp import web
from aiohttp_jinja2 import template


log = logging.getLogger(__name__)


@template('home.html')
async def home(request):
    return {}

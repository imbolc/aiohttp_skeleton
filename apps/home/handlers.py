import logging

from aiohttp_jinja2 import template

import lib.fs


log = logging.getLogger(__name__)


@template('home/home.html')
async def home(request):
    return {
        'readme': lib.fs.read_text('./README.md'),
    }

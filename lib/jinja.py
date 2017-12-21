import datetime

import jinja2
import aiohttp_jinja2
import webassets.loaders
import misaka

import cfg
from lib.static import static_url
import lib.web


def setup(app):
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(cfg.TEMPLATE_PATH),
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
    })
    env.policies['json.dumps_function'] = lib.web.json_dumps
    env.filters['markdown'] = misaka.html

    webassets_env = webassets.loaders.YAMLLoader(
        'cfg/webassets.yaml').load_environment()
    webassets_env.debug = cfg.DEBUG
    env.globals['webassets'] = webassets_env

    return env

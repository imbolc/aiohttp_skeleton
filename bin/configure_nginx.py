#!var/env/bin/python
from _setup import echo, sudo
import os
import sys

import cfg


template = open('cfg/nginx.txt').read()
content = template % {
    'root': cfg.ROOT,
    'host': cfg.HOST.encode('idna').decode('utf-8'),
    'port': cfg.PORT,
}
echo('dim', content)

filename = f'/etc/nginx/sites-enabled/{cfg.HOST}'
with sudo():
    open(filename, 'w').write(content)
print('Nginx config created:', filename)

code = os.system('nginx -t && /etc/init.d/nginx restart')
echo(*(('bug', ' BUG ') if code else ('ok', ' O.K. ')))
sys.exit(code)

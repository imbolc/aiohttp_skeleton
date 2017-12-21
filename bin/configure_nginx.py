#!var/env/bin/python
from _setup import echo, sudo, call

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

call('nginx -t && /etc/init.d/nginx restart')

#!var/env/bin/python
import _setup  # noqa
import os

import cfg
import lib.fs


template = lib.fs.read_text('cfg/nginx.txt')
content = template % {
    'root': lib.fs.ROOT,
    'host': cfg.HOST.encode('idna').decode('utf-8'),
    'port': cfg.PORT,
}
filename = '/etc/nginx/sites-enabled/{}'.format(cfg.HOST)
print(content)
#  lib.fs.write_text(filename, content)
#  print('Nginx config created:', filename)
#  os.system('/etc/init.d/nginx configtest && sudo /etc/init.d/nginx restart')

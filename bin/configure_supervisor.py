#!var/env/bin/python
import _setup  # noqa
import os

import cfg
import lib.fs


template = lib.fs.read_text('cfg/supervisord.conf')
content = template.format(root=lib.fs.ROOT, cfg=cfg)
filename = '/etc/supervisor/conf.d/{}.conf'.format(cfg.SUPERVISOR_NAME)
lib.fs.write_text(filename, content)
print('Nginx config created:', filename)
os.system('sudo /etc/init.d/supervisor restart')

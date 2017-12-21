#!var/env/bin/python
from _setup import echo, sudo, call

import cfg


template = open('cfg/supervisord.conf').read()
content = template.format(cfg=cfg)
echo('dim', content)

filename = f'/etc/supervisor/conf.d/{cfg.SUPERVISOR_NAME}.conf'
with sudo():
    open(filename, 'w').write(content)
print('Supervisor config created:', filename)

call('sudo supervisorctl reload')

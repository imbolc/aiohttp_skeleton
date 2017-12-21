Skeleton for aiohttp site
=========================
* logging
* webassets
* setproctitle
* jinja2
* json serialization with ujson
* custom error pages
* trailing slash middleware
* deployment with git and fabric
* nginx

    * version hashes for static files
    * and its agressive caching

* supervisor
* let's encrypt


Installation
------------
    sudo aptitude install nginx supervisor libyaml-dev libevent-dev g++ libffi-dev
    pip install fabric3
    fab install

    sudo ./bin/configure_nginx.py
    sudo ./bin/configure_supervisor.py
    ./bin/cerbot.py obtain

Add ssl-certificate renew command to your crontab:

    MAILTO=""
    PATH=/usr/local/bin/:/usr/bin

    15 4 * * *  cd ~/site-root/; timeout 10m ./bin/certbot.py renew


Starting of development server
-----------------------------
    echo 'DEBUG = TEMPLATE_AUTO_RELOAD = True' > ./cfg/local.py
    fab s

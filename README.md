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


Installation
------------
    sudo aptitude install nginx supervisor libyaml-dev libevent-dev g++ libffi-dev
    pip install fabric3
    fab install

    sudo ./bin/configure_nginx.py
    sudo ./bin/configure_supervisor.py


Starting of development server
-----------------------------
    echo 'DEBUG = TEMPLATE_AUTO_RELOAD = True' > ./cfg/local.py
    fab s

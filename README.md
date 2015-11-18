Skeleton for aiohttp site
=========================
* logging
* webassets
* setproctitle
* jinja2
* json serialization with support of `date`, `datetime` and `bson.ObjectId`
* agressive caching of static files 
* deployment with git and fabric 
* nginx and supervisor configuration


Installation
------------
    sudo aptitude install supervisor libyaml-dev libevent-dev g++ libffi-dev
    fab buildenv
    npm i

    sudo ./bin/configure_nginx.py
    sudo ./bin/configure_supervisor.py


Starting of development server
-----------------------------
    fab s

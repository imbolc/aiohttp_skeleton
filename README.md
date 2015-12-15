Skeleton for aiohttp site
=========================
* logging
* webassets
* setproctitle
* jinja2 with loading of templates from apps folders
* json serialization with support of `date`, `datetime` and `bson.ObjectId`
* 404 and 500 error pages
* auto removing of trailing slashes for unknown urls
* agressive caching of static files 
* deployment with git and fabric 
* nginx and supervisor configuration


Installation
------------
    sudo aptitude install supervisor libyaml-dev libevent-dev g++ libffi-dev
    fab buildenv
    cd ./static; npm i; cd ..

    sudo ./bin/configure_nginx.py
    sudo ./bin/configure_supervisor.py


Starting of development server
-----------------------------
    fab s

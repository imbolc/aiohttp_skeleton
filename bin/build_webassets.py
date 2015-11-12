#!var/env/bin/python
import _setup  # noqa
import logging

import webassets
from webassets.script import CommandLineEnvironment


log = logging.getLogger('webassets')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

env = webassets.loaders.YAMLLoader(
    'cfg/webassets.yaml').load_environment()
cmdenv = CommandLineEnvironment(env, log)
cmdenv.build()

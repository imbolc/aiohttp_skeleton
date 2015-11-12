import os
import logging
import logging.handlers


def to_console(logger_name, level,
               format='%(levelname)-8s [%(name)s] %(message)s'):
    handler = logging.StreamHandler()
    set_level(handler, level)
    handler.setFormatter(logging.Formatter(format))
    logging.getLogger(logger_name).addHandler(handler)


def to_file(logger_name, filename, level):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        filename=filename,
        mode='a+',
        maxBytes=1000000,
        backupCount=10,
    )
    set_level(handler, level)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s\t%(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'))
    logging.getLogger(logger_name).addHandler(handler)


def set_levels(levels):
    for name, level in levels.items():
        set_level(name, level)


def set_level(handler, level):
    level = getattr(logging, level.upper())
    if isinstance(handler, str):
        handler = logging.getLogger(handler)
    handler.setLevel(level)

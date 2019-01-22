from __future__ import absolute_import
import logging

#############################
# create root logger
root_log = logging.getLogger()
root_log.setLevel(logging.WARN)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# add formatter to handler
ch.setFormatter(formatter)

# add handler to logger
root_log.addHandler(ch)


# create named logger
def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.propagate = False
    log.addHandler(ch)
    return log
#############################

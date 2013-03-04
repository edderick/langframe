import logging
import sys
import inspect


class Logger():
    """
    Generic Logger class; contains joint functionality, could be used on
    its own though.
    """
    def __init__(self, subchannel):
        # lookup which function in which file created this logger
        caller_funcname = inspect.stack()[2][3]
        caller_filename = inspect.stack()[2][1]

        self.root_logger = logging.getLogger("langframe.root.%s" % subchannel)
        self.debug_logger = logging.getLogger("langframe.debug.%s" % subchannel)

        self.root_logger.info("%s Initialised from %s in %s" %
                              (subchannel, caller_funcname, caller_filename))

    def info(self, message):
        self.root_logger.info(message)


def display_log(*channels):
    for channel_name in channels:
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(0)

        log = logging.getLogger(channel_name)
        log.setLevel(logging.DEBUG)
        log.addHandler(log_handler)
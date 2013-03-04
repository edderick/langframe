import logging, sys, inspect

class NPLogger():
    def __init__(self):
        """
         Underlying channel name is given based on its classname (e.g. NPLogger)
         and an individual, unique instance name, assigned at runtime. This
         instamce channel is a subchannel of the class channel, so all messages
         are routed through both channels.
        """
        class_name = self.__class__.__name__
        instance_name = id(self)
        full_name = "%s.%s" % (class_name, instance_name)

        # lookup which function in which file created this logger
        caller_funcname = inspect.stack()[2][3]
        caller_filename = inspect.stack()[2][1]

        self.root_logger = logging.getLogger("langframe.root.%s" % full_name)
        self.debug_logger = logging.getLogger("langframe.debug.%s" % full_name)

        self.root_logger.info("%s Initialised from %s in %s" %
                              (full_name, caller_funcname, caller_filename))

    def info(self, message):
        self.root_logger.info(message)

    def rule_debug(self, debug_string, indent=0, symbol=""):
        if symbol:
            symbol = "[%s]" % str(symbol)
        tabs = "\t" * indent

        debug_string = str(debug_string)
        debug_string = debug_string.replace("\n", "\n%s" % tabs, 50)

        self.debug_logger.info("%s %s %s" % (tabs, symbol, debug_string) )


def display_log(full_channel_name):
    #TODO: use positional arguments to allow multiple channels to be specified

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(0)

    log = logging.getLogger(full_channel_name)
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)
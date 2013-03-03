import logging, sys

class NPLogger():
    def __init__(self):
        self.root_logger = logging.getLogger("langframe.root.nplogger")
        self.debug_logger = logging.getLogger("langframe.debug.nplogger")

        self.root_logger.info("NPSymbolLearner Initialised from %s" % "TODO")

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
import logging, sys

class NPLogger():
    def __init__(self):
        self.root_logger = logging.getLogger("langframe.root.nplogger")
        self.debug_logger = logging.getLogger("langframe.debug.nplogger")

        self.root_logger.info("NPSymbolLearner Initialised from %s" % "TODO")

    def info(self, message):
        self.root_logger.info(message)

    def rule_debug(self, indent_level, symbol, debug_string):
        if symbol is not "->" or "<-":
            symbol = "[%s]" % symbol

        self.logger.debug("%s %s %s", ("\t" * indent_level, symbol, debug_string) )


def display_log(full_channel_name):
    #TODO: use positional arguments to allow multiple channels to be specified

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(0)

    log = logging.getLogger(full_channel_name)
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)
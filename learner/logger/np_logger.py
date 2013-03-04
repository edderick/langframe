from utils.logger import Logger

class NPLogger(Logger):
    def __init__(self):
        """
         Underlying channel name is given based on its classname (e.g. NPLogger)
         and an individual, unique instance name, assigned at runtime. This
         instance channel is a subchannel of the class channel, so all messages
         are routed through both channels.
        """
        class_name = self.__class__.__name__
        instance_name = id(self)
        full_name = "%s.%s" % (class_name, instance_name)

        Logger.__init__(self, full_name)

    def rule_debug(self, debug_string, indent=0, symbol=""):
        """
        Format rule flow in a standardised way (symbol display, level of
        indentation).
        """
        if symbol:
            symbol = "[%s]" % str(symbol)
        tabs = "\t" * indent

        debug_string = str(debug_string)
        debug_string = debug_string.replace("\n", "\n%s" % tabs, 50)

        self.debug_logger.info("%s %s %s" % (tabs, symbol, debug_string) )
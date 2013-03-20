from utils.logger import Logger

class ColourLogger(Logger):
    def __init__(self, agent_name):
        Logger.__init__(self, "ColourLogger")
        self.agent_name = agent_name
        self.lang_name = "0"
        self.data_logger.info("lang.name,r,g,b,word,x,y,z")

    def set_langname(self, lang_name):
        """
        The full name of the language is "agent_name.lang_name". This can be used
        to differentiate between languages at different learning stages
        """
        self.lang_name = lang_name

    def new_point(self, word, p):
        full_name = ".".join((self.agent_name, self.lang_name))
        coordinates = ",".join(str(x) for x in p)

        self.data_logger.info("%s,%s,%s,%s" %
                              (full_name, coordinates, word, coordinates))

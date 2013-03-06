from utils.logger import Logger

class ColourLogger(Logger):
    def __init__(self):
        Logger.__init__(self, "ColourLogger")

    def new_point(self, word, p):
        self.data_logger.info("+ %d,%d,%d %s"
                              % (p[0], p[1], p[2], word))
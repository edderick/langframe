from utils.logger import Logger
from training.expression import Expression

class ColourLogger(Logger):
    def __init__(self, learner):
        Logger.__init__(self, "ColourLogger")

        self.learner = learner
        self.full_name = learner.agent_name
        
        # on new point
        self.data_logger.info("lang.name,r,g,b,word,x,y,z")

        # probe point & mean point
        self.probe_logger = Logger("colour.sample")
        self.mean_logger = Logger("colour.mean")

        # output header CSV
        self.probe_logger.info("lang.name,word")
        self.mean_logger.info("lang.name,word,r,g,b")

    def display_log(*channels):
        Logger.display_log(*channels)

    def new_point(self, word, p):
        coordinates = ",".join(str(x) for x in p)
        self.data_logger.info("%s,%s,%s,%s" %
                              (self.learner.agent_name, coordinates, word, coordinates))

    def log_points(self, lang_name, test_colours):
        for rgb in test_colours:
            expression = Expression(["COLOUR", "r_%d" % rgb[0],
                                 "g_%d" % rgb[1],
                                 "b_%d" % rgb[2] ])
            self.probe_logger.info("%s,%s" % (lang_name, self.learner.word_for(expression)))
    
    def mean(self, lang_name):
        core_words = ("black", "darkblue", "green", "red", "cyan", "yellow", 
                    "magenta", "white")
        for word in core_words:
            try:
                mean = self.learner.mean[word]
                self.mean_logger.info("%s,%s,%d,%d,%d" % 
                    (lang_name, word, mean[0], mean[1], mean[2]))
            except KeyError:
                self.mean_logger.info("%s,%s,0,0,0" % (lang_name, word))

        used_words = set(core_words)
        all_words = set(self.learner.n.keys())
        extra_words = list(all_words.difference(used_words))
        extra_words.sort()

        for extra_word in extra_words:
            mean = self.learner.mean[extra_word]
            self.mean_logger.info("%s,%s,%d,%d,%d" % 
                    (lang_name, extra_word, mean[0], mean[1], mean[2]))


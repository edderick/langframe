import knowledge.knn_colour
import utils.logger
import training.expression

utils.logger.display_log("langframe.data.ColourLogger")

def get_colour_expression(rgb):
   return training.expression.Expression(["COLOUR",
                                         "r_%d" % rgb[0],
                                         "g_%d" % rgb[1],
                                         "b_%d" % rgb[2] ])

colour = knowledge.knn_colour.KNNColourSemantics("agent", k=1)

data = (
    ("darkblue", (0, 0, 255)),
    ("cyan", (0, 255, 255)),
    ("purple", (255, 0, 255)),
    ("white", (255, 255, 255)),
)

for colour_word, rgb in data:
    colour.learn(colour_word, get_colour_expression(rgb))
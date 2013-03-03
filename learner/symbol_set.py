from training.pairs import VariableExpression, ConstantExpression

class SymbolSet(set):
    """
    Has slightly different interface for adding element to set (as we want to be able
    to add a string, which is an Iterable, and would otherwise add each character.
    """

    def is_universal(self):
        return False

    def __str__(self):
        return "{ %s }" % ", ".join(repr(symbol) for symbol in self)

    def variables(self):
        return {symbol for symbol in self
                if isinstance(symbol, VariableExpression) or symbol.islower()}

    def constants(self):
        return {symbol for symbol in self
                if isinstance(symbol, ConstantExpression) or symbol.isupper()}


class UniversalSymbolSet:
    """
    This is like a typical set, but is initialised as universal... which is
    just a "token" state, until it is intersected with a finite set, the result
    being that finite set.
    """

    def is_universal(self):
        return True

    def __contains__(self, element):
        # universal set trivially contains all elements
        return True

    def __str__(self):
        return "UNIVERSAL"

    def add(self, elements):
        return

    def intersection(self, other_set):
        finite_set = SymbolSet()
        return finite_set.union(other_set)
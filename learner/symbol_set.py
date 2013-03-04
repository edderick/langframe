from training.expression import VariableExpression, ConstantExpression


class SymbolSet(set):
    """
    Has slightly different interface for adding element to set (as we want to be able
    to add a string, which is an Iterable, and would otherwise add each character.
    """

    def is_universal(self):
        """Finite symbol set cannot be infinite in size"""
        return False

    def __str__(self):
        """String representation"""
        return "{ %s }" % ", ".join(repr(symbol) for symbol in self)

    def variables(self):
        """Return list of variables in this set"""
        return {symbol for symbol in self
                if isinstance(symbol, VariableExpression) or symbol.islower()}

    def constants(self):
        """Return list of constants in this set"""
        return {symbol for symbol in self
                if isinstance(symbol, ConstantExpression) or symbol.isupper()}


class UniversalSymbolSet:
    """
    This is like a typical set, but is initialised as universal... which is
    just a "token" state, until it is intersected with a finite set, returning
    that finite set.
    """

    def is_universal(self):
        return True

    # noinspection PyUnusedLocal
    def __contains__(self, element):
        # universal set trivially contains all elements
        return True

    def __str__(self):
        """String representation"""
        return "UNIVERSAL"

    def add(self, elements):
        """Adding to universal set changes nothing"""
        return

    def intersection(self, other_set):
        """Return other_set as finite SymbolSet"""
        finite_set = SymbolSet()
        return finite_set.union(other_set)
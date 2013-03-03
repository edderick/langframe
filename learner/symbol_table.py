from learner.symbol_set import SymbolSet, UniversalSymbolSet
from abc import ABCMeta, abstractmethod
from training.pairs import VariableExpression, ConstantExpression

class SymbolTable:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.mapping = dict()

    def __iter__(self):
        """iterate through all symbols, i.e. all keys in internal dict"""
        return self.mapping.keys().__iter__()

    def __setitem__(self, key, value):
        """override usage of [] operator for setting a set for a word"""
        self.mapping[key] = value

    @abstractmethod
    def __contains__(self, item):
        """overload 'in' operator. semantically: is a word in the lexicon?"""
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def add(self, word, symbols):
        pass

class FiniteSymbolTable(SymbolTable):
    def add(self, word, symbols):
        """add a word and symbol string/set of symbol strings to the table"""
        if isinstance(symbols, basestring):
            if symbols.isupper():
                symbols = ConstantExpression(symbols)   # add singleton set containing string
            else:
                symbols = VariableExpression(symbols)

        try:
            self.mapping[word] = self.mapping[word].union(symbols)
        except KeyError:  # no entry exists for word: create one
            self.mapping[word] = SymbolSet()
            self.mapping[word] = self.mapping[word].union(symbols)

    def __str__(self):
        return "\n".join(["%s || %s" % (word.rjust(10),
                                    str(self[word]).ljust(25))
                                        for word in self.mapping]  )

    def __contains__ (self, element):
        return element in self.mapping.keys()

    def __getitem__(self, key):
        """override usage of [] operator for getting a set for a word"""
        if key in self.mapping.keys():
            return self.mapping[key]
        else:
            self.mapping[key] = SymbolSet()
            return self.mapping[key]


class UniversalSymbolTable(SymbolTable):
    def add(self, word, symbols):
        # if given symbol is single string, add to singleton set otherwise
        # it would add each individual letter as a symbol

        try:
            self.mapping[word].add(symbols)
        except KeyError:
            self.mapping[word] = UniversalSymbolSet()

    def __repr__(self):
        return "UNIVERSAL"

    def __contains__(self, item):
        """Universal symbol table would trivially have any key"""
        return True

    def __getitem__(self, key):
        """override usage of [] operator for getting a set for a word"""
        if key in self.mapping.keys():
            return self.mapping[key]
        else:
            self.mapping[key] = UniversalSymbolSet()
            return self.mapping[key]
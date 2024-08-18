import json
import re
import functools


class Symbol:
    def __init__(self, type, word):
        self.type = type
        self.word = word

    def __len__(self):
        return len(self.word)

    @property
    def is_token(self):
        return self.type != 'spaces'


class SymbolBuilder:
    @staticmethod
    def operators(word):
        return Symbol('operators', word)

    @staticmethod
    def bounds(word):
        return Symbol('bounds', word)

    @staticmethod
    def spaces(word):
        return Symbol('spaces', word)


class Token:
    def __init__(self, line, index, type, word):
        self.line = line
        self.index = index
        self.type = type
        self.word = word

    def __str__(self):
        return f'<{self.line}, {self.index}, {self.type}, {self.word}>'


class TokenBuilder:
    @staticmethod
    def symbol(location, symbol):
        return Token(location[0], location[1], symbol.type, symbol.word)

    @staticmethod
    def default(location, type, word):
        return Token(location[0], location[1], type, word)


class Error:
    def __init__(self, line, index, message):
        self.line = line
        self.index = index
        self.message = message

    def __str__(self):
        return f'Error at line: {self.line} column: {self.index} {self.message}'


class ErrorBuilder:
    @staticmethod
    def unexpected(location):
        return Error(location[0], location[1], 'unexpected symbols')

    @staticmethod
    def invalid(location, type):
        return Error(location[0], location[1], f'invalid {type}')


class TransformEdge:
    def __init__(self, last, char, next):
        self.last = last
        self.char = char
        self.next = next


class AutomataGrammar:
    def __init__(self, formulas, alias, start, final):
        self.formulas = formulas
        self.alias = alias
        self.start = start
        self.final = final

    def parse_edges(self):
        for formula in self.formulas:
            if match := re.match(r'(.+?) -> `(.+?)` (.+)', formula):
                last = match.group(1)
                name = match.group(2)
                next = match.group(3)

                for char in self.alias[name]:
                    yield TransformEdge(last, char, next)

            elif match := re.match(r'(.+?) -> `(.+?)`', formula):
                last = match.group(1)
                name = match.group(2)

                for char in self.alias[name]:
                    yield TransformEdge(last, char, self.final)

            elif match := re.match(r'(.+?) -> (.) (.+)', formula):
                last = match.group(1)
                char = match.group(2)
                next = match.group(3)

                yield TransformEdge(last, char, next)

            elif match := re.match(r'(.+?) -> (.)', formula):
                last = match.group(1)
                char = match.group(2)

                yield TransformEdge(last, char, self.final)


class SymbolGrammar:
    def __init__(self, keywords, operators, bounds, spaces, constants_specials):
        self.keywords = keywords
        self.operators = operators
        self.bounds = bounds
        self.spaces = spaces
        self.constants_specials = constants_specials


class GrammarLoader:
    @staticmethod
    @functools.cache
    def config():
        with open('grammars/grammar.json', 'r', encoding='utf-8') as grammar_json:
            return json.load(grammar_json)

    @staticmethod
    def constants():
        config = GrammarLoader.config()

        return AutomataGrammar(
            config['constants']['formulas'],
            config['alias'],
            config['constants']['start'],
            config['constants']['final'],
        )

    @staticmethod
    def identifiers():
        config = GrammarLoader.config()

        return AutomataGrammar(
            config['identifiers']['formulas'],
            config['alias'],
            config['identifiers']['start'],
            config['identifiers']['final'],
        )

    @staticmethod
    def symbols():
        config = GrammarLoader.config()

        return SymbolGrammar(
            config['keywords'],
            config['operators'],
            config['bounds'],
            config['spaces'],
            config['constants']['specials'],
        )

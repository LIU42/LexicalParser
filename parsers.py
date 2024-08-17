from automaton import FiniteAutomaton

from language import GrammarLoader
from language import TokenBuilder
from language import ErrorBuilder
from language import SymbolBuilder


class Automatons:

    def __init__(self):
        self.identifiers = FiniteAutomaton('identifiers')
        self.identifiers.build(GrammarLoader.identifiers())
        self.identifiers.reset()

        self.constants = FiniteAutomaton('constants')
        self.constants.build(GrammarLoader.constants())
        self.constants.reset()

    def allocate(self, char):
        if self.constants.transform_exist(char):
            return self.constants
        if self.identifiers.transform_exist(char):
            return self.identifiers


class StatusManager:

    def __init__(self, line, code):
        self.line = line
        self.code = code
        self.index = 0
        self.token = ''
        self.token_list = []
        self.error_list = []
        self.automaton = None

    @property
    def reached_end(self):
        return self.index >= len(self.code)

    @property
    def location(self):
        return self.line, self.index - len(self.token)

    @property
    def pending_char(self):
        return self.code[self.index]

    @property
    def pending_code(self):
        return self.code[self.index:]

    def transform_success(self):
        transform_success = self.automaton.transform(self.pending_char)

        if transform_success:
            self.token += self.pending_char
            self.index += 1

        return transform_success

    def release_automaton(self):
        self.token = ''
        self.automaton.reset()
        self.automaton = None


class LexicalParser:

    def __init__(self):
        self.symbols = GrammarLoader.symbols()
        self.automatons = Automatons()

    def __call__(self, inputs):
        token_list = []
        error_list = []

        for manager in self.generate_managers(inputs):
            self.parse_process(manager)

            token_list.extend(manager.token_list)
            error_list.extend(manager.error_list)

        return token_list, error_list

    @staticmethod
    def generate_managers(inputs):
        for line, code in enumerate(inputs, start=1):
            yield StatusManager(line, code)

    @staticmethod
    def match(manager, symbols):
        for symbol in filter(manager.pending_code.startswith, symbols):
            return symbol

    def match_symbols(self, manager):
        if symbol := self.match(manager, self.symbols.bounds):
            return SymbolBuilder.bounds(symbol)

        if symbol := self.match(manager, self.symbols.spaces):
            return SymbolBuilder.spaces(symbol)

        if symbol := self.match(manager, self.symbols.operators):
            return SymbolBuilder.operators(symbol)

    def parse_symbols(self, manager):
        symbol = self.match_symbols(manager)

        if symbol is None:
            manager.error_list.append(ErrorBuilder.unexpected(manager.location))
            manager.index += 1
        else:
            if symbol.is_token:
                manager.token_list.append(TokenBuilder.symbol(manager.location, symbol))
            manager.index += len(symbol)

    def token_valid(self, manager):
        return manager.automaton.name != 'constants' or self.match_symbols(manager)

    def type_recheck(self, manager):
        if manager.automaton.name == 'identifiers':
            if manager.token in self.symbols.keywords:
                return 'keywords'
            if manager.token in self.symbols.constants_specials:
                return 'constants'
        return manager.automaton.name

    def parse_variables(self, manager):
        location = manager.location

        if manager.automaton.reached_final and self.token_valid(manager):
            manager.token_list.append(TokenBuilder.default(location, self.type_recheck(manager), manager.token))
        else:
            manager.error_list.append(ErrorBuilder.invalid(location, manager.automaton.name))

        manager.release_automaton()

    def parse_process(self, manager):
        while not manager.reached_end:
            if manager.automaton is None:
                manager.automaton = self.automatons.allocate(manager.pending_char)

            if manager.automaton is None:
                self.parse_symbols(manager)

            elif not manager.transform_success():
                self.parse_variables(manager)

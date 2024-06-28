import json
import re


class Token:

    def __init__(self, line_no, index, type, word):
        self.line_no = line_no
        self.index = index
        self.type = type
        self.word = word

    def __str__(self):
        return f'<{self.line_no}, {self.index}, {self.type}, {self.word}>'


class TokenBuilder:

    @staticmethod
    def build(location, type, word):
        return Token(location[0], location[1], type, word)


class Error:

    def __init__(self, line_no, index, message):
        self.line_no = line_no
        self.index = index
        self.message = message

    def __str__(self):
        return f'Error at line: {self.line_no} column: {self.index} {self.message}'


class ErrorBuilder:

    @staticmethod
    def unexpected(location):
        return Error(location[0], location[1], 'unexpected symbols')

    @staticmethod
    def invalid(location, type):
        return Error(location[0], location[1], f'invalid {type}')


class AutomataGrammar:

    def __init__(self, formulas, alias, start_symbol, final_symbol):
        self.formulas = formulas
        self.alias = alias
        self.start_symbol = start_symbol
        self.final_symbol = final_symbol


class SymbolGrammar:

    def __init__(self, keywords, operators, bounds, spaces, constants_specials):
        self.keywords = keywords
        self.operators = operators
        self.bounds = bounds
        self.spaces = spaces
        self.constants_specials = constants_specials


class GrammarLoader:

    def __init__(self):
        with open('grammars/grammar.json', mode='r', encoding='utf-8') as grammar_file:
            self.grammar_dict = json.load(grammar_file)

    def load_automata_grammar(self, token_type):
        automata_grammar = AutomataGrammar(
            self.grammar_dict[token_type]['formulas'],
            self.grammar_dict['alias'],
            self.grammar_dict[token_type]['start'],
            self.grammar_dict[token_type]['final'],
        )
        return automata_grammar

    def load_symbol_grammar(self):
        symbol_grammar = SymbolGrammar(
            self.grammar_dict['keywords'],
            self.grammar_dict['operators'],
            self.grammar_dict['bounds'],
            self.grammar_dict['spaces'],
            self.grammar_dict['constants']['specials'],
        )
        return symbol_grammar


class FormulaParser:

    @staticmethod
    def parse(formula, grammar, nfa_transforms):
        if match_result := re.match(r'(.+?) -> `(.+?)` (.+)', formula):
            last_status, alias_name, next_status = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(last_status, char, next_status)

        elif match_result := re.match(r'(.+?) -> `(.+?)`', formula):
            last_status, alias_name = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(last_status, char, nfa_transforms.final_status)

        elif match_result := re.match(r'(.+?) -> (.) (.+)', formula):
            last_status, char, next_status = match_result.groups()
            nfa_transforms.add_transform(last_status, char, next_status)

        elif match_result := re.match(r'(.+?) -> (.)', formula):
            last_status, char = match_result.groups()
            nfa_transforms.add_transform(last_status, char, nfa_transforms.final_status)

import re

from transforms import NFATransforms

class Token:
    
    def __init__(self, line_no: int, index: int, type: str, word: str) -> None:
        self.line_no = line_no
        self.index = index
        self.type = type
        self.word = word

    def __str__(self) -> str:
        return f"<{self.line_no}, {self.index}, {self.type}, {self.word}>"


class Error:

    def __init__(self, line_no: int, index: int, message: str) -> None:
        self.line_no = line_no
        self.index = index
        self.message = message

    def __str__(self) -> str:
        return f"Error at line: {self.line_no} column: {self.index} {self.message}"


class ErrorBuilder:

    @staticmethod
    def unexpected(line_no: int, index: int) -> Error:
        return Error(line_no, index, "unexpected symbols")
    
    @staticmethod
    def invalid(line_no: int, index: int, symbol_type: str) -> Error:
        return Error(line_no, index, f"invalid {symbol_type}")


class Grammar:

    def __init__(self, formulas: list[str], alias: dict[str, list[str]], start_symbol: str, end_symbol: str) -> None:
        self.formulas = formulas
        self.alias = alias
        self.start_symbol = start_symbol
        self.end_symbol = end_symbol


class FormulaParser:

    @staticmethod
    def parse(formula: str, grammar: Grammar, nfa_transforms: NFATransforms) -> None:
        if match_result := re.match(r"(.+?) -> `(.+?)` (.+)", formula):
            status_from, alias_name, status_to = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(status_from, char, status_to)
        
        elif match_result := re.match(r"(.+?) -> `(.+?)`", formula):
            status_from, alias_name = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(status_from, char, nfa_transforms.end_status)

        elif match_result := re.match(r"(.+?) -> (.) (.+)", formula):
            status_from, char, status_to = match_result.groups()
            nfa_transforms.add_transform(status_from, char, status_to)

        elif match_result := re.match(r"(.+?) -> (.)", formula):
            status_from, char = match_result.groups()
            nfa_transforms.add_transform(status_from, char, nfa_transforms.end_status)

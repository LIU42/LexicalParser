import json
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


class AutomataGrammar:

    def __init__(self, formulas: list[str], alias: dict[str, list[str]], start_symbol: str, end_symbol: str) -> None:
        self.formulas = formulas
        self.alias = alias
        self.start_symbol = start_symbol
        self.end_symbol = end_symbol


class SymbolGrammar:

    def __init__(self, **element_dict: list[str]) -> None:
        self.keywords = element_dict["keywords"]
        self.operators = element_dict["operators"]
        self.bounds = element_dict["bounds"]
        self.spaces = element_dict["spaces"]
        self.constants_specials = element_dict["constants_specials"]

    
class GrammarLoader:

    def __init__(self, grammar_path: str = "./grammars/grammar.json") -> None:
        with open(grammar_path, mode="r", encoding="utf-8") as grammar_file:
            self.grammar_dict = json.load(grammar_file)

    def load_automata_grammar(self, token_type: str = "constants") -> AutomataGrammar:
        return AutomataGrammar(
            self.grammar_dict[token_type]["formulas"],
            self.grammar_dict["alias"],
            self.grammar_dict[token_type]["start"],
            self.grammar_dict[token_type]["end"]
        )
    
    def load_symbol_grammar(self) -> SymbolGrammar:
        return SymbolGrammar(
            keywords = self.grammar_dict["keywords"],
            operators = self.grammar_dict["operators"],
            bounds = self.grammar_dict["bounds"],
            spaces = self.grammar_dict["spaces"],
            constants_specials = self.grammar_dict["constants"]["specials"]
        )


class FormulaParser:

    @staticmethod
    def parse(formula: str, grammar: AutomataGrammar, nfa_transforms: NFATransforms) -> None:
        if match_result := re.match(r"(.+?) -> `(.+?)` (.+)", formula):
            last_status, alias_name, next_status = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(last_status, char, next_status)
        
        elif match_result := re.match(r"(.+?) -> `(.+?)`", formula):
            last_status, alias_name = match_result.groups()
            for char in grammar.alias[alias_name]:
                nfa_transforms.add_transform(last_status, char, nfa_transforms.end_status)

        elif match_result := re.match(r"(.+?) -> (.) (.+)", formula):
            last_status, char, next_status = match_result.groups()
            nfa_transforms.add_transform(last_status, char, next_status)

        elif match_result := re.match(r"(.+?) -> (.)", formula):
            last_status, char = match_result.groups()
            nfa_transforms.add_transform(last_status, char, nfa_transforms.end_status)

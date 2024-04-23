from automata import FiniteAutomata
from language import Token
from language import Error
from language import ErrorBuilder
from language import Grammar

class AutomataWrapper:

    def __init__(self, automata: FiniteAutomata = None, type_name: str = None) -> None:
        self.automata = automata
        self.type_name = type_name
        self.last_type_name = type_name

    def setup(self, automata: FiniteAutomata, type_name: str) -> None:
        self.automata = automata
        self.type_name = type_name

    def reset(self) -> None:
        if self.automata is not None:
            self.automata.reset()
            self.automata = None
            self.last_type_name = self.type_name
            self.type_name = None

    def is_setup(self) -> bool:
        return self.automata is not None


class LexicalParser:

    def __init__(self, grammars: dict[str, list[str] | dict[str, list[str] | str]]) -> None:
        self.constants_automata = FiniteAutomata(
            Grammar(
                grammars["constants"]["formulas"],
                grammars["alias"],
                grammars["constants"]["start"],
                grammars["constants"]["end"]
            )
        )
        self.identifiers_automata = FiniteAutomata(
            Grammar(
                grammars["identifiers"]["formulas"],
                grammars["alias"],
                grammars["identifiers"]["start"],
                grammars["identifiers"]["end"]
            )
        )
        self.current_automata_wrapper = AutomataWrapper()
        self.keywords = grammars["keywords"]
        self.operators = grammars["operators"]
        self.bounds = grammars["bounds"]
        self.spaces = grammars["spaces"]
        self.constants_specials = grammars["constants"]["specials"]

    def __call__(self, input_codes: list[str]) -> tuple[list[Token], list[Error]]:
        return self.parse(input_codes)
    
    def allocate_automata(self, char: str) -> None:
        if self.identifiers_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.identifiers_automata, "identifiers")
        elif self.constants_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.constants_automata, "constants")
       
    def parse_operators(self, code: str, index: int) -> str:
        for operator in self.operators:
            if code[index:index + len(operator)] == operator:
                return operator
        return None
    
    def parse_bounds(self, code: str, index: int) -> str:
        for bound in self.bounds:
            if code[index:index + len(bound)] == bound:
                return bound
        return None
    
    def parse_spaces(self, code: str, index: int) -> str:
        for space in self.spaces:
            if code[index:index + len(space)] == space:
                return space
        return None
    
    def parse_enumerable_symbols(self, code: str, index: int) -> tuple[bool, str, str]:
        if space := self.parse_spaces(code, index):
            return True, "spaces", space
        if bound := self.parse_bounds(code, index):
            return True, "bounds", bound
        if operator := self.parse_operators(code, index):
            return True, "operators", operator
        return False, None, None
    
    def type_recheck(self, word: str) -> str:
        if self.current_automata_wrapper.type_name == "identifiers":
            if word in self.keywords:
                return "keywords"
            if word in self.constants_specials:
                return "constants"
        return self.current_automata_wrapper.type_name
    
    def constants_error_precheck(self, code: str, index: int) -> bool:
        return self.current_automata_wrapper.type_name == "constants" and not self.parse_enumerable_symbols(code, index)[0]

    def parse_line(self, line_no: int, code: str, token_list: list[Token], error_list: list[Error]) -> None:
        index = 0
        word = ""
        while index < len(code):
            if not self.current_automata_wrapper.is_setup():
                self.allocate_automata(code[index])
            if not self.current_automata_wrapper.is_setup():
                success, symbol_type, symbol = self.parse_enumerable_symbols(code, index)
                if success:
                    if symbol_type != "spaces":
                        token_list.append(Token(line_no, index, symbol_type, symbol))
                    index += len(symbol)
                else:
                    error_list.append(ErrorBuilder.unexpected(line_no, index))
                    index += 1
            elif self.current_automata_wrapper.automata.transform(code[index]):
                word += code[index]
                index += 1
            else:
                if self.current_automata_wrapper.automata.is_finished():
                    token_list.append(Token(line_no, index - len(word), self.type_recheck(word), word))
                    if self.constants_error_precheck(code, index):
                        error_list.append(ErrorBuilder.invalid(line_no, index - len(word), "constants"))
                else:
                    error_list.append(ErrorBuilder.invalid(line_no, index - len(word), self.current_automata_wrapper.type_name))
                word = ""
                self.current_automata_wrapper.reset()

    def parse(self, input_codes: list[str]) -> tuple[list[Token], list[Error]]:
        token_list = list[Token]()
        error_list = list[Error]()

        for line_no, code in enumerate(input_codes, start = 1):
            self.parse_line(line_no, code, token_list, error_list)
        return token_list, error_list

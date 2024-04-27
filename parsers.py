from automata import FiniteAutomata
from language import Token
from language import Error
from language import ErrorBuilder
from language import GrammarLoader

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
    

class ParseLineParams:

    def __init__(self, line_no: int, code: str, token_list: list[Token], error_list: list[Error]) -> None:
        self.line_no = line_no
        self.code = code
        self.token_list = token_list
        self.error_list = error_list


class LexicalParser:

    def __init__(self, grammar_loader: GrammarLoader = GrammarLoader()) -> None:
        self.constants_automata = FiniteAutomata(
            grammar_loader.load_automata_grammar("constants")
        )
        self.identifiers_automata = FiniteAutomata(
            grammar_loader.load_automata_grammar("identifiers")
        )
        self.symbols = grammar_loader.load_symbol_grammar()
        self.current_automata_wrapper = AutomataWrapper()

    def __call__(self, input_codes: list[str]) -> tuple[list[Token], list[Error]]:
        return self.parse(input_codes)
    
    def allocate_automata(self, char: str) -> None:
        if self.identifiers_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.identifiers_automata, "identifiers")
        elif self.constants_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.constants_automata, "constants")
       
    def parse_operators(self, code: str, index: int) -> str:
        for operator in self.symbols.operators:
            if code[index:index + len(operator)] == operator:
                return operator
        return None
    
    def parse_bounds(self, code: str, index: int) -> str:
        for bound in self.symbols.bounds:
            if code[index:index + len(bound)] == bound:
                return bound
        return None
    
    def parse_spaces(self, code: str, index: int) -> str:
        for space in self.symbols.spaces:
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
            if word in self.symbols.keywords:
                return "keywords"
            if word in self.symbols.constants_specials:
                return "constants"
        return self.current_automata_wrapper.type_name
    
    def constants_error_precheck(self, code: str, index: int) -> bool:
        return self.current_automata_wrapper.type_name == "constants" and not self.parse_enumerable_symbols(code, index)[0]
    
    def handle_enumerable_parse(self, params: ParseLineParams, current_index: int) -> int:
        token_list = params.token_list
        error_list = params.error_list
        success, symbol_type, symbol = self.parse_enumerable_symbols(params.code, current_index)

        if success:
            if symbol_type != "spaces":
                token_list.append(Token(params.line_no, current_index, symbol_type, symbol))
            current_index += len(symbol)
        else:
            error_list.append(ErrorBuilder.unexpected(params.line_no, current_index))
            current_index += 1

        return current_index
    
    def handle_transform_failure(self, params: ParseLineParams, current_index: int, current_word: str) -> None:
        token_list = params.token_list
        error_list = params.error_list
        word_index = current_index - len(current_word)

        if self.current_automata_wrapper.automata.is_finished():
            token_list.append(Token(params.line_no, word_index, self.type_recheck(current_word), current_word))

            if self.constants_error_precheck(params.code, current_index):
                error_list.append(ErrorBuilder.invalid(params.line_no, word_index, "constants"))
        else:
            error_list.append(ErrorBuilder.invalid(params.line_no, word_index, self.current_automata_wrapper.type_name))

    def parse_line(self, line_no: int, code: str, token_list: list[Token], error_list: list[Error]) -> None:
        current_index = 0
        current_word = ""

        while current_index < len(code):
            if not self.current_automata_wrapper.is_setup():
                self.allocate_automata(code[current_index])

            params = ParseLineParams(line_no, code, token_list, error_list)
            if not self.current_automata_wrapper.is_setup():
                current_index = self.handle_enumerable_parse(params, current_index)

            elif self.current_automata_wrapper.automata.transform(code[current_index]):
                current_word += code[current_index]
                current_index += 1
            else:
                self.handle_transform_failure(params, current_index, current_word)
                current_word = ""
                self.current_automata_wrapper.reset()

    def parse(self, input_codes: list[str]) -> tuple[list[Token], list[Error]]:
        token_list = list()
        error_list = list()
        for line_no, code in enumerate(input_codes, start = 1):
            self.parse_line(line_no, code, token_list, error_list)        
        return token_list, error_list

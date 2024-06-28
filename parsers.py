from automata import FiniteAutomata
from language import ErrorBuilder
from language import TokenBuilder


class AutomataWrapper:

    def __init__(self, automata=None, type_name=None):
        self.automata = automata
        self.type_name = type_name

    def setup(self, automata, type_name):
        self.automata = automata
        self.type_name = type_name

    def reset(self):
        if self.automata is not None:
            self.automata.reset()
            self.automata = None
            self.type_name = None

    @property
    def is_setup(self):
        return self.automata is not None

    @property
    def is_finished(self):
        return self.automata.is_finished

    def transform(self, char):
        return self.automata.transform(char)


class ParseLineArgs:

    def __init__(self, line_code, line_no, token_list, error_list):
        self.line_code = line_code
        self.line_no = line_no
        self.token_list = token_list
        self.error_list = error_list


class LexicalParser:

    def __init__(self, grammar_loader):
        self.constants_automata = FiniteAutomata(
            grammar_loader.load_automata_grammar('constants')
        )
        self.identifiers_automata = FiniteAutomata(
            grammar_loader.load_automata_grammar('identifiers')
        )
        self.symbols = grammar_loader.load_symbol_grammar()
        self.current_automata_wrapper = AutomataWrapper()

    def __call__(self, input_codes):
        return self.parse(input_codes)

    def allocate_automata(self, char):
        if self.identifiers_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.identifiers_automata, 'identifiers')
        elif self.constants_automata.try_transform(char):
            self.current_automata_wrapper.setup(self.constants_automata, 'constants')

    def parse_operators(self, line_code, index):
        for operator in self.symbols.operators:
            if line_code[index:index + len(operator)] == operator:
                return operator
        return None

    def parse_bounds(self, line_code, index):
        for bound in self.symbols.bounds:
            if line_code[index:index + len(bound)] == bound:
                return bound
        return None

    def parse_spaces(self, line_code, index):
        for space in self.symbols.spaces:
            if line_code[index:index + len(space)] == space:
                return space
        return None

    def parse_enumerable_symbols(self, line_code, index):
        if space := self.parse_spaces(line_code, index):
            return True, 'spaces', space
        if bound := self.parse_bounds(line_code, index):
            return True, 'bounds', bound
        if operator := self.parse_operators(line_code, index):
            return True, 'operators', operator
        return False, None, None

    def type_recheck(self, word):
        if self.current_automata_wrapper.type_name == 'identifiers':
            if word in self.symbols.keywords:
                return 'keywords'
            if word in self.symbols.constants_specials:
                return 'constants'
        return self.current_automata_wrapper.type_name

    def invalid_error_aftercheck(self, line_code, index):
        if self.current_automata_wrapper.type_name != 'constants':
            return False
        return not self.parse_enumerable_symbols(line_code, index)[0]

    def handle_enumerable_parse(self, current_index, parse_args):
        success, symbol_type, symbol_word = self.parse_enumerable_symbols(parse_args.line_code, current_index)

        if success:
            if symbol_type != 'spaces':
                token = TokenBuilder.build(
                    type=symbol_type,
                    word=symbol_word,
                    location=(parse_args.line_no, current_index),
                )
                parse_args.token_list.append(token)
            current_index += len(symbol_word)
        else:
            error = ErrorBuilder.unexpected(
                location=(parse_args.line_no, current_index),
            )
            parse_args.error_list.append(error)
            current_index += 1

        return current_index

    def is_valid_token_at_transform_failure(self, line_code, current_index):
        if not self.current_automata_wrapper.is_finished:
            return False
        return not self.invalid_error_aftercheck(line_code, current_index)

    def handle_transform_failure(self, current_index, current_word, parse_args):
        word_index = current_index - len(current_word)

        if self.is_valid_token_at_transform_failure(parse_args.line_code, current_index):
            token = TokenBuilder.build(
                type=self.type_recheck(current_word),
                word=current_word,
                location=(parse_args.line_no, word_index),
            )
            parse_args.token_list.append(token)
        else:
            error = ErrorBuilder.invalid(
                type=self.current_automata_wrapper.type_name,
                location=(parse_args.line_no, word_index),
            )
            parse_args.error_list.append(error)

    def parse_line(self, parse_args):
        current_index = 0
        current_word = ''

        while current_index < len(parse_args.line_code):
            if not self.current_automata_wrapper.is_setup:
                self.allocate_automata(parse_args.line_code[current_index])

            if not self.current_automata_wrapper.is_setup:
                current_index = self.handle_enumerable_parse(current_index, parse_args)

            elif self.current_automata_wrapper.transform(parse_args.line_code[current_index]):
                current_word += parse_args.line_code[current_index]
                current_index += 1
            else:
                self.handle_transform_failure(current_index, current_word, parse_args)
                current_word = ''
                self.current_automata_wrapper.reset()

    def parse(self, input_codes):
        token_list = list()
        error_list = list()

        for line_no, line_code in enumerate(input_codes, start=1):
            parse_args = ParseLineArgs(
                line_code=line_code,
                line_no=line_no,
                token_list=token_list,
                error_list=error_list,
            )
            self.parse_line(parse_args)

        return token_list, error_list

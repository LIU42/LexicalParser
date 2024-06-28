from language import FormulaParser
from transforms import DFATransforms
from transforms import NFATransforms


class StatusNumberDict:

    def __init__(self):
        self.number_dict = dict()
        self.status_count = 0

    def __getitem__(self, status_set):
        try:
            return self.number_dict[status_set]
        except KeyError:
            return None

    def try_add(self, status_set):
        if status_set in self.number_dict:
            return False
        else:
            self.number_dict[status_set] = self.status_count
            self.status_count += 1
            return True

    def clear(self):
        self.number_dict.clear()
        self.status_count = 0


class FiniteAutomata:

    def __init__(self, grammar):
        self.transforms = self.ensure(self.create(grammar))
        self.current_status = self.transforms.start_status

    @staticmethod
    def create_status_set(*status):
        return set(status)

    @staticmethod
    def create(grammar):
        nfa_transforms = NFATransforms(grammar.start_symbol, grammar.final_symbol)
        for formula in grammar.formulas:
            FormulaParser.parse(formula.strip(), grammar, nfa_transforms)
        return nfa_transforms

    def ensure(self, nfa_transforms):
        dfa_transforms = DFATransforms()
        nfa_transforms.get_characters()

        status_dict = StatusNumberDict()
        status_dict.try_add(nfa_transforms.get_epsilon_closure(self.create_status_set(nfa_transforms.start_status)))

        status_buffer = set(status_dict.number_dict.keys())

        while len(status_buffer) > 0:
            new_status_sets = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_sets:
                for char in nfa_transforms.all_characters:
                    next_status = nfa_transforms.get_next_status(status, char)
                    if len(next_status) == 0:
                        continue
                    if status_dict.try_add(next_status):
                        status_buffer.add(next_status)
                    dfa_transforms.add_transform(status_dict[status], char, status_dict[next_status])

        for status, number in status_dict.number_dict.items():
            if nfa_transforms.start_status in status:
                dfa_transforms.start_status = number
            elif nfa_transforms.final_status in status:
                dfa_transforms.final_status.add(number)

        return dfa_transforms

    def reset(self):
        self.current_status = self.transforms.start_status

    def transform(self, char):
        try:
            self.current_status = self.transforms[self.current_status, char]
            return True
        except KeyError:
            return False

    def try_transform(self, char):
        return self.transforms.is_transform_exist(self.current_status, char)

    @property
    def is_finished(self):
        return self.current_status in self.transforms.final_status

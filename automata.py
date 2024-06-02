from language import AutomataGrammar
from language import FormulaParser

from status import StatusNumberDict
from status import StatusSetUtils

from transforms import DFATransforms
from transforms import NFATransforms

class FiniteAutomata:

    def __init__(self, grammar: AutomataGrammar) -> None:
        self.transforms = self.ensure(self.create(grammar))
        self.current_status = self.transforms.start_status

    def create(self, grammar: AutomataGrammar) -> NFATransforms:
        nfa_transforms = NFATransforms(grammar.start_symbol, grammar.end_symbol)
        for formula in grammar.formulas:
            FormulaParser.parse(formula.strip(), grammar, nfa_transforms)
        return nfa_transforms
    
    def ensure(self, nfa_transforms: NFATransforms) -> DFATransforms:
        dfa_transforms = DFATransforms()
        nfa_transforms.get_characters()

        status_dict = StatusNumberDict()
        status_dict.try_add(nfa_transforms.get_epsilon_closure(StatusSetUtils.create_by_items(nfa_transforms.start_status)))

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
            elif nfa_transforms.end_status in status:
                dfa_transforms.end_status.add(number)

        return dfa_transforms
    
    def reset(self) -> None:
        self.current_status = self.transforms.start_status
    
    def transform(self, char: str) -> bool:
        try:
            self.current_status = self.transforms[self.current_status, char]
            return True
        except KeyError:
            return False
        
    def try_transform(self, char: str) -> bool:
        return self.transforms.is_transform_exist(self.current_status, char)
        
    def is_finished(self) -> bool:
        return self.current_status in self.transforms.end_status

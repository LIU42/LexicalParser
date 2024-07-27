import functools
from collections import defaultdict


class TransformTable:

    def __init__(self, start, final, default):
        self.start = start
        self.final = final
        self.elements = defaultdict(lambda: defaultdict(default))

    def __getitem__(self, location):
        last = location[0]
        char = location[1]
        return self.elements[last][char]


class NFATransforms(TransformTable):

    @functools.cached_property
    def all_characters(self):
        return {char for transform in self.elements.values() for char in transform.keys() if char != 'ε'}
    
    def closure(self, status_set):
        status_closure = status_set.copy()
        status_buffer = status_set.copy()

        while len(status_buffer) > 0:
            current_status = status_buffer.copy()
            status_buffer.clear()

            for status in current_status:
                status_buffer = status_buffer.union(self.elements[status]['ε'])

            status_closure = status_closure.union(status_buffer)

        return frozenset(status_closure)

    def move(self, status, char):
        return {next for last in status for next in self.elements[last][char]}

    def next_status(self, status_set, char):
        return self.closure(self.move(status_set, char))


class DFATransforms(TransformTable):

    def __setitem__(self, condition, destination):
        last = condition[0]
        char = condition[1]
        self.elements[last][char] = destination

    def exist(self, last, char):
        return char in self.elements[last]


class TransformsBuilder:

    @staticmethod
    def nfa(grammar):
        nfa_transforms = NFATransforms(grammar.start, grammar.final, set)

        for element in grammar.parse_formulas():
            nfa_transforms.elements[element.last][element.char].add(element.next)

        return nfa_transforms

    @staticmethod
    def dfa():
        return DFATransforms(None, None, None)

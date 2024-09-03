import collections
import functools


class StatusNumber:
    def __init__(self, init_status):
        self.status_number = {init_status: 0}
        self.status_count = 1

    def __getitem__(self, status):
        return self.status_number[status]

    def __contains__(self, status):
        return status in self.status_number

    def add(self, status):
        self.status_number[status] = self.status_count
        self.status_count += 1

    def find(self, find_status):
        return {number for status, number in self.status_number.items() if find_status in status}


class TransformGraph:
    def __init__(self, default):
        self.start = None
        self.final = None
        self.edges = collections.defaultdict(lambda: collections.defaultdict(default))

    def __getitem__(self, location):
        last = location[0]
        char = location[1]

        return self.edges[last][char]


class NFATransformGraph(TransformGraph):
    @functools.cached_property
    def all_characters(self):
        return {char for edge in self.edges.values() for char in edge.keys() if char != 'ε'}
    
    def closure(self, status_set):
        status_closure = status_set.copy()
        status_buffer = status_set.copy()

        while len(status_buffer) > 0:
            current_status = status_buffer.copy()
            status_buffer.clear()

            for status in current_status:
                status_buffer = status_buffer.union(self.edges[status]['ε'] - status_closure)

            status_closure = status_closure.union(status_buffer)

        return frozenset(status_closure)

    def move(self, status, char):
        return {next for last in status for next in self.edges[last][char]}

    def next_status(self, status, char):
        return self.closure(self.move(status, char))

    @staticmethod
    def build(grammar):
        nfa_transform_graph = NFATransformGraph(set)

        for edge in grammar.parse_edges():
            nfa_transform_graph.edges[edge.last][edge.char].add(edge.next)

        nfa_transform_graph.start = grammar.start
        nfa_transform_graph.final = grammar.final

        return nfa_transform_graph


class DFATransformGraph(TransformGraph):
    def __setitem__(self, condition, destination):
        last = condition[0]
        char = condition[1]

        self.edges[last][char] = destination

    def exist(self, last, char):
        return char in self.edges[last]

    @staticmethod
    def build():
        return DFATransformGraph(None)

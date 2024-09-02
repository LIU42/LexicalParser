import automatons.build as build


class FiniteAutomaton:
    def __init__(self, name, grammar):
        self.name = name
        self.status = None
        self.transform_graph = build.dfa_transforms(grammar)

    @property
    def reached_final(self):
        return self.status in self.transform_graph.final

    def reset(self):
        for status in self.transform_graph.start:
            self.status = status

    def transform(self, char):
        try:
            self.status = self.transform_graph[self.status, char]
            return True
        except KeyError:
            return False

    def transform_exist(self, char):
        return self.transform_graph.exist(self.status, char)

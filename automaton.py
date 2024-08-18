from graphs import TransformGraphsBuilder


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


class FiniteAutomaton:
    def __init__(self, name):
        self.name = name
        self.status = None
        self.transform_graph = None

    @property
    def reached_final(self):
        return self.status in self.transform_graph.final

    @staticmethod
    def ensure(nfa_transform_graph):
        init_status = nfa_transform_graph.closure({nfa_transform_graph.start})

        status_number = StatusNumber(init_status)
        status_buffer = {init_status}

        dfa_transform_graph = TransformGraphsBuilder.dfa()

        while len(status_buffer) > 0:
            current_status = status_buffer.copy()
            status_buffer.clear()

            for status in current_status:
                for char in nfa_transform_graph.all_characters:
                    next_status = nfa_transform_graph.next_status(status, char)

                    if len(next_status) == 0:
                        continue
                    if next_status not in status_number:
                        status_number.add(next_status)
                        status_buffer.add(next_status)

                    dfa_transform_graph[status_number[status], char] = status_number[next_status]

        dfa_transform_graph.start = status_number.find(nfa_transform_graph.start)
        dfa_transform_graph.final = status_number.find(nfa_transform_graph.final)

        return dfa_transform_graph

    def build(self, grammar):
        self.transform_graph = self.ensure(TransformGraphsBuilder.nfa(grammar))

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

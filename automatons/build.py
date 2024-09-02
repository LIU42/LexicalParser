from automatons.status import StatusNumber

from automatons.graphs import NFATransformGraph
from automatons.graphs import DFATransformGraph


def ensure(nfa_transform_graph):
    init_status = nfa_transform_graph.closure({nfa_transform_graph.start})

    status_number = StatusNumber(init_status)
    status_buffer = {init_status}

    dfa_transform_graph = DFATransformGraph.build_dfa()

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


def dfa_transforms(grammar):
    return ensure(NFATransformGraph.build_nfa(grammar))

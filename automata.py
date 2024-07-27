from transforms import TransformsBuilder


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


class FiniteAutomata:

    def __init__(self, name):
        self.name = name
        self.transforms = None
        self.status = None

    @property
    def reached_final(self):
        return self.status in self.transforms.final

    @staticmethod
    def ensure(nfa_transforms):
        init_status = nfa_transforms.closure({nfa_transforms.start})

        status_number = StatusNumber(init_status)
        status_buffer = {init_status}

        dfa_transforms = TransformsBuilder.dfa()

        while len(status_buffer) > 0:
            current_status = status_buffer.copy()
            status_buffer.clear()

            for status in current_status:
                for char in nfa_transforms.all_characters:
                    next_status = nfa_transforms.next_status(status, char)

                    if len(next_status) == 0:
                        continue
                    if next_status not in status_number:
                        status_number.add(next_status)
                        status_buffer.add(next_status)

                    dfa_transforms[status_number[status], char] = status_number[next_status]

        dfa_transforms.start = status_number.find(nfa_transforms.start)
        dfa_transforms.final = status_number.find(nfa_transforms.final)

        return dfa_transforms

    def build(self, grammar):
        self.transforms = self.ensure(TransformsBuilder.nfa(grammar))

    def reset(self):
        for status in self.transforms.start:
            self.status = status

    def transform(self, char):
        try:
            self.status = self.transforms[self.status, char]
            return True
        except KeyError:
            return False

    def transform_exist(self, char):
        return self.transforms.exist(self.status, char)

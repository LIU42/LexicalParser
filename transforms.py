class NFATransforms:

    def __init__(self, start_status, final_status):
        self.transforms = dict()
        self.all_characters = set()
        self.start_status = start_status
        self.final_status = final_status

    def __getitem__(self, indices):
        return self.transforms[indices[0]][indices[1]]

    def add_transform(self, last_status, char, next_status):
        self.transforms.setdefault(last_status, dict()).setdefault(char, set()).add(next_status)

    def get_characters(self):
        if len(self.all_characters) > 0:
            return self.all_characters

        for transforms in self.transforms.values():
            for char in transforms.keys():
                if char != 'ε':
                    self.all_characters.add(char)

        return self.all_characters

    def get_epsilon_closure(self, status_set):
        closure_status_set = status_set.copy()
        status_buffer = closure_status_set.copy()

        while True:
            new_status_set = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_set:
                if status not in self.transforms or 'ε' not in self.transforms[status]:
                    continue
                for next_status in self.transforms[status]['ε']:
                    if next_status not in closure_status_set:
                        status_buffer.add(next_status)

            if len(status_buffer) == 0:
                break
            closure_status_set = closure_status_set.union(status_buffer)

        return frozenset(closure_status_set)
    
    def get_move_status(self, status_set, search_char):
        move_status_set = set()

        for status in status_set:
            if status not in self.transforms or search_char not in self.transforms[status]:
                continue
            for next_status in self.transforms[status][search_char]:
                move_status_set.add(next_status)

        return move_status_set
    
    def get_next_status(self, status_set, search_char):
        return self.get_epsilon_closure(self.get_move_status(status_set, search_char))


class DFATransforms:

    def __init__(self):
        self.transforms = dict()
        self.start_status = 0
        self.final_status = set()

    def __getitem__(self, indices):
        return self.transforms[indices[0]][indices[1]]
    
    def add_transform(self, last_status, char, next_status):
        self.transforms.setdefault(last_status, dict()).setdefault(char, next_status)

    def is_transform_exist(self, last_status, char):
        return last_status in self.transforms and char in self.transforms[last_status]

class NFATransforms:

    def __init__(self, start_status: str, end_status: str) -> None:
        self.transforms = dict()
        self.all_characters = set()
        self.start_status = start_status
        self.end_status = end_status

    def __getitem__(self, transform_index: tuple[str, int]) -> set[str]:
        return self.get_transform(*transform_index)

    def add_transform(self, last_status: str, char: str, next_status: str) -> None:
        self.transforms.setdefault(last_status, dict()).setdefault(char, set()).add(next_status)

    def get_transform(self, last_status: str, char: str) -> set[str]:
        return self.transforms[last_status][char]

    def get_characters(self, epsilon: str = "ε") -> set[str]:
        for transforms in self.transforms.values():
            for char in transforms.keys():
                if char != epsilon:
                    self.all_characters.add(char)
        return self.all_characters

    def get_epsilon_closure(self, status_set: set[str], epsilon: str = "ε") -> frozenset[str]:
        closure_status_set = status_set.copy()
        status_buffer = closure_status_set.copy()

        while True:
            new_status_set = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_set:
                if status not in self.transforms or epsilon not in self.transforms[status]:
                    continue
                for next_status in self.transforms[status][epsilon]:
                    if next_status not in closure_status_set:
                        status_buffer.add(next_status)

            if len(status_buffer) == 0:
                break
            closure_status_set = closure_status_set.union(status_buffer)

        return frozenset(closure_status_set)
    
    def get_move_status(self, status_set: set[str], search_char: str) -> set[str]:
        move_status_set = set()
        for status in status_set:
            if status not in self.transforms or search_char not in self.transforms[status]:
                continue
            for next_status in self.transforms[status][search_char]:
                move_status_set.add(next_status)
        return move_status_set
    
    def get_next_status(self, status_set: set[str], search_char: str) -> frozenset[str]:
        return self.get_epsilon_closure(self.get_move_status(status_set, search_char))


class DFATransforms:

    def __init__(self) -> None:
        self.transforms = dict()
        self.start_status = 0
        self.end_status = set()

    def __getitem__(self, transform_index: tuple[int, str]) -> int:
        return self.get_transform(*transform_index)
    
    def add_transform(self, last_status: int, char: str, next_status: int) -> None:
        self.transforms.setdefault(last_status, dict()).setdefault(char, next_status)

    def get_transform(self, last_status: int, char: str) -> int:
        return self.transforms[last_status][char]

    def is_transform_exist(self, last_status: int, char: str) -> bool:
        return last_status in self.transforms and char in self.transforms[last_status]

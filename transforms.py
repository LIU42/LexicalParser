class NFATransforms:

    def __init__(self, start_status: str, end_status: str) -> None:
        self.transforms = dict()
        self.all_characters = set()
        self.start_status = start_status
        self.end_status = end_status

    def __getitem__(self, transform_index: tuple[str, int]) -> set[str]:
        return self.get_transform(*transform_index)

    def add_transform(self, status_from: str, char: str, status_to: str) -> None:
        self.transforms.setdefault(status_from, dict()).setdefault(char, set()).add(status_to)

    def get_transform(self, status_from: str, char: str) -> set[str]:
        return self.transforms[status_from][char]

    def get_characters(self) -> set[str]:
        for transforms in self.transforms.values():
            for char in transforms.keys():
                if char != "ε":
                    self.all_characters.add(char)
        return self.all_characters

    def get_epsilon_closure(self, status_set: set[str]) -> frozenset[str]:
        closure_status_set = status_set.copy()
        status_buffer = closure_status_set.copy()

        while True:
            new_status_set = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_set:
                if self.transforms.get(status) is None or self.transforms[status].get("ε") is None:
                    continue
                for status_to in self.transforms[status]["ε"]:
                    if status_to not in closure_status_set:
                        status_buffer.add(status_to)

            if len(status_buffer) == 0:
                break
            closure_status_set = closure_status_set.union(status_buffer)

        return frozenset(closure_status_set)
    
    def get_move_status(self, status_set: set[str], search_char: str) -> set[str]:
        move_status_set = set()
        for status in status_set:
            if self.transforms.get(status) is None or self.transforms[status].get(search_char) is None:
                continue
            for status_to in self.transforms[status][search_char]:
                move_status_set.add(status_to)
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
    
    def add_transform(self, status_from: int, char: str, status_to: int) -> None:
        self.transforms.setdefault(status_from, dict()).setdefault(char, status_to)

    def get_transform(self, status_from: int, char: str) -> int:
        return self.transforms[status_from][char]

    def is_transform_exist(self, status_from: int, char: str) -> bool:
        try:
            return self.transforms[status_from][char] is not None
        except KeyError:
            return False

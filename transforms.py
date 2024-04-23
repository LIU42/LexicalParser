class NFATransforms:

    def __init__(self, start_status: str, end_status: str, all_characters: set[str] = set[str]()) -> None:
        self.items = dict[str, dict[str, set[str]]]()
        self.start_status = start_status
        self.end_status = end_status
        self.all_characters = all_characters

    def __getitem__(self, item_index: tuple[str, int]) -> set[str]:
        return self.get_item(*item_index)

    def get_item(self, status_from: str, char: str) -> set[str]:
        return self.items[status_from][char]

    def add_transform(self, status_from: str, char: str, status_to: str) -> None:
        self.items.setdefault(status_from, dict[str, set[str]]()).setdefault(char, set[str]()).add(status_to)

    def get_characters(self) -> set[str]:
        for transforms in self.items.values():
            for char in transforms.keys():
                if char != "ε":
                    self.all_characters.add(char)
        return self.all_characters

    def get_epsilon_closure(self, status_set: set[str]) -> set[str]:
        closure_status_set = status_set.copy()
        status_buffer = closure_status_set.copy()

        while True:
            new_status_set = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_set:
                if self.items.get(status) is None or self.items[status].get("ε") is None:
                    continue
                for status_to in self.items[status]["ε"]:
                    if status_to not in closure_status_set:
                        status_buffer.add(status_to)

            if len(status_buffer) == 0:
                break
            closure_status_set = closure_status_set.union(status_buffer)

        return closure_status_set
    
    def get_move_status(self, status_set: set[str], search_char: str) -> set[str]:
        move_status_set = set[str]()
        for status in status_set:
            if self.items.get(status) is None or self.items[status].get(search_char) is None:
                continue
            for status_to in self.items[status][search_char]:
                move_status_set.add(status_to)
        return move_status_set
    
    def get_next_status(self, status_set: set[str], search_char: str) -> set[str]:
        return self.get_epsilon_closure(self.get_move_status(status_set, search_char))


class DFATransforms:

    def __init__(self, start_status: int = None, end_status: set[int] = set[int]()) -> None:
        self.items = dict[int, dict[str, int]]()
        self.start_status = start_status
        self.end_status = end_status

    def __getitem__(self, item_index: tuple[int, str]) -> int:
        return self.get_item(*item_index)

    def get_item(self, status_from: int, char: str) -> int:
        return self.items[status_from][char]

    def add_transform(self, status_from: int, char: str, status_to: int) -> None:
        self.items.setdefault(status_from, dict[str, int]())[char] = status_to

    def is_transform_exist(self, status_from: int, char: str) -> bool:
        if self.items.get(status_from) is None:
            return False
        return self.items[status_from].get(char) is not None

class NFATransforms:

    def __init__(self, start_status: str, end_status: str, all_characters: set[str] = set[str]()) -> None:
        self.start_status = start_status
        self.end_status = end_status
        self.all_characters = all_characters
        self.transform_items = dict[str, dict[str, set[str]]]()

    def __getitem__(self, item_index: tuple[str, int]) -> set[str]:
        return self.get_item(*item_index)

    def get_item(self, status_from: str, char: str) -> set[str]:
        return self.transform_items[status_from][char]

    def add_transform(self, status_from: str, char: str, status_to: str) -> None:
        self.transform_items.setdefault(status_from, dict[str, set[str]]()).setdefault(char, set[str]()).add(status_to)

    def get_characters(self) -> set[str]:
        for transforms in self.transform_items.values():
            for char in transforms.keys():
                if char != "ε":
                    self.all_characters.add(char)
        return self.all_characters

    def get_epsilon_closure(self, status_set: set[str]) -> frozenset[str]:
        closure_status_set = set[str](status_set)
        status_buffer = closure_status_set.copy()

        while True:
            new_status_set = status_buffer.copy()
            status_buffer.clear()

            for status in new_status_set:
                if self.transform_items.get(status) is None or self.transform_items[status].get("ε") is None:
                    continue
                for status_to in self.transform_items[status]["ε"]:
                    if status_to not in closure_status_set:
                        status_buffer.add(status_to)

            if len(status_buffer) == 0:
                break
            closure_status_set = closure_status_set.union(status_buffer)

        return frozenset[str](closure_status_set)
    
    def get_move_status(self, status_set: frozenset[str], search_char: str) -> frozenset[str]:
        move_status_set = set[str]()
        for status in status_set:
            if self.transform_items.get(status) is None or self.transform_items[status].get(search_char) is None:
                continue
            for status_to in self.transform_items[status][search_char]:
                move_status_set.add(status_to)
        return frozenset[str](move_status_set)
    
    def get_next_status(self, status_set: set[str], search_char: str) -> frozenset[str]:
        return self.get_epsilon_closure(self.get_move_status(status_set, search_char))


class DFATransforms:

    def __init__(self, start_status: int = None, end_status: set[int] = set[int]()) -> None:
        self.start_status = start_status
        self.end_status = end_status
        self.transform_items = dict[int, dict[str, int]]()

    def __getitem__(self, item_index: tuple[int, str]) -> int:
        return self.get_item(*item_index)

    def get_item(self, status_from: int, char: str) -> int:
        return self.transform_items[status_from][char]

    def add_transform(self, status_from: int, char: str, status_to: int) -> None:
        self.transform_items.setdefault(status_from, dict[str, int]())[char] = status_to

    def is_transform_exist(self, status_from: int, char: str) -> bool:
        if self.transform_items.get(status_from) is None:
            return False
        return self.transform_items[status_from].get(char) is not None

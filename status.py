class StatusSetMap:

    def __init__(self) -> None:
        self.number_map = dict[frozenset[str], int]()
        self.status_count = 0

    def __getitem__(self, status_set: set[str]) -> int:
        return self.get_number(status_set)

    def __contains__(self, status_set: set[str]) -> bool:
        return frozenset[str](status_set) in self.number_map
    
    def if_add(self, status_set: set[str]) -> bool:
        frozen_status_set = frozenset[str](status_set)
        if frozen_status_set in self.number_map:
            return False
        self.number_map[frozen_status_set] = self.status_count
        self.status_count += 1
        return True

    def get_number(self, status_set: set[str]) -> int:
        return self.number_map.get(frozenset[str](status_set))
    
    def clear(self) -> None:
        self.number_map.clear()
        self.status_count = 0


class StatusSetBuffer:

    def __init__(self, status_sets: set[frozenset[str]] = set[frozenset[str]]()) -> None:
        self.items = set[frozenset[str]](status_sets)

    def __contains__(self, status_set: set[str]) -> bool:
        return frozenset[str](status_set) in self.items
    
    def __len__(self) -> int:
        return len(self.items)
    
    def add_item(self, status_set: set[str]) -> None:
        return self.items.add(frozenset[str](status_set))
    
    def copy_items(self) -> set[frozenset[str]]:
        return self.items.copy()
    
    def clear(self) -> None:
        self.items.clear()


class StatusSetUtils:

    @staticmethod
    def create_by_items(*status: str) -> set[str]:
        return set[str](status)
    
class StatusSetUtils:

    @staticmethod
    def create_by_items(*status: str) -> set[str]:
        return set(status)
    

class StatusNumberDict:

    def __init__(self) -> None:
        self.number_dict = dict()
        self.status_count = 0

    def __getitem__(self, status_set: frozenset[str]) -> int:
        return self.get_number(status_set)
    
    def try_add(self, status_set: frozenset[str]) -> bool:
        if status_set in self.number_dict:
            return False
        else:
            self.number_dict[status_set] = self.status_count
            self.status_count += 1
            return True

    def get_number(self, status_set: frozenset[str]) -> int:
        try:
            return self.number_dict[status_set]
        except KeyError:
            return None
    
    def clear(self) -> None:
        self.number_dict.clear()
        self.status_count = 0

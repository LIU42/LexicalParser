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

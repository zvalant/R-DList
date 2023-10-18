import target_date as td


class Project:
    def __init__(self, machine):
        self.machine = machine
        self.target_dates = {}

    def add_date(self, target_date):
        self.target_dates[target_date] = td.TargetDate(target_date)

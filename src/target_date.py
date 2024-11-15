import part


class TargetDate:

    def __init__(self, date):
        self.date = date
        self.parts = {}

    def add_part(self, part_number, quantity, description, status, engineer,inventory = "Not Found", notes = "Not Found", pm="NOt Found"):
        self.parts[part_number] = part.Part(quantity, description, status, engineer, inventory, notes,pm)

    def remove_part(self, part_number):
        self.parts.pop(part_number)

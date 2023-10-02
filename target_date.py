import part
class TargetDate:
    def __init__(self,date):
        self.date = date
        self.parts = {}
    def add_part(self,part_number,quantity,description,status,engineer):
        self.parts[part_number] = part.Part(quantity,description,status,engineer)

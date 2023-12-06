class Part:
    def __init__(self,quantity,description,status,engineer,inventory="Not Found",notes = "Not Found"):
        self.quantity = quantity
        self.description = description
        self.status = status
        self.engineer = engineer
        self.inventory = inventory
        self.notes = notes


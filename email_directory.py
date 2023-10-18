class EmailDirectory:
    def __init__(self):
        self.engineers_email = {
            "Zac": "zac.valant@baader.com",
        }
    def get_email(self,engineer):
        if engineer not in self.engineers_email:
            return self.engineers_email["Zac"]
        else:
            return self.engineers_email[engineer]
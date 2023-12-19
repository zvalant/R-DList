import utility
class EmailDirectory:
    def __init__(self):
        self.engineers_email_file = "M:\\_R&D List Docs\\DependencyFiles\\EngineerEmails.txt"
        self.all_email_file = "M:\\_R&D List Docs\\DependencyFiles\\AllEmails.txt"

        self.engineers_email = utility.map_engineering_emails(self.engineers_email_file)
        self.all_email = utility.collect_recipients(self.all_email_file)
    def get_email(self,engineer):
        if engineer not in self.engineers_email:
            return self.engineers_email["Zac"]
        else:
            return self.engineers_email[engineer]


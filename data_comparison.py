from utility import part_assignment
import status
from email_directory import EmailDirectory
from email_manager import EmailManager
from email_messages import EmailMessages
class DataComparison:
    def __init__(self,current_sheet,past_sheet):
        self.current_projects = current_sheet.projects
        self.past_projects = past_sheet.projects
        self.current_cache = current_sheet.key_cache
        self.past_cache = past_sheet.key_cache
        self.new_demand = {}
        self.removed_demand = {}
        self.project_change = {}
        self.quantity_change = {}
        self.date_change = {}
        self.driving_change = {}
        self.picked_change = {}
        self.issued_change = {}
        self.driving_modified = {}
        self.driving = {}
        self.issued = {}
        self.issued_modified = {}
        self.activity = {
            "New Demand":self.new_demand,
            "Removed Demand": self.removed_demand,
            "Project Change": self.project_change,
            "Quantity Change": self.quantity_change,
            "Date Change": self.date_change,
            "Status Change: Driving":self.driving_change,
            "Status Change: Picked": self.picked_change,
            "Status Change: Issued": self.issued_change
        }
        self.modified = set()
        self.error_found = False

    def activity_search(self,current_sheet):
        error_email = EmailManager()
        engineer_email = EmailDirectory()
        for id in self.current_cache:
            current_machine = self.current_cache[id].machine
            current_part_number = self.current_cache[id].part_number
            current_quantity = self.current_cache[id].quantity
            current_description = self.current_cache[id].description
            current_due_date = self.current_cache[id].due_date
            current_status = self.current_cache[id].status
            current_engineer = self.current_cache[id].engineer
            if id in self.past_cache:
                past_machine = self.past_cache[id].machine
                past_part_number = self.past_cache[id].part_number
                past_quantity = self.past_cache[id].quantity
                past_due_date = self.past_cache[id].due_date
                past_status = self.past_cache[id].status

                if current_part_number != past_part_number:
                    row = current_sheet[current_sheet["UniqueID"] == id]
                    row_index = int(row.index.values) + 2
                    msg = EmailMessages(0,row_index)
                    message = msg.error_reused_id
                    error_email.error_email(message, engineer_email.get_email(current_engineer))
                    current_sheet = current_sheet.drop(row_index-2)
                    continue

                if current_machine != past_machine:
                    self.project_change = part_assignment(self.project_change,f"{current_machine} was {past_machine}", current_due_date,current_part_number,current_quantity,current_description,current_status,current_engineer)
                    self.modified.add(current_machine)
                    self.modified.add(past_machine)
                if current_quantity != past_quantity:
                    self.quantity_change = part_assignment(self.quantity_change,
                                                              current_machine, current_due_date,
                                                              current_part_number,f"{current_quantity}X was {past_quantity}",
                                                              current_description, current_status, current_engineer)
                    self.modified.add(current_machine)
                if current_due_date != past_due_date:
                    self.date_change = part_assignment(self.date_change,
                                                               current_machine, current_due_date,
                                                               current_part_number,current_quantity,
                                                               current_description, current_status, current_engineer)
                    self.modified.add(current_machine)

                if current_status != past_status:
                    if current_status == status.DRIVING:
                        self.driving_change= part_assignment(self.driving_change,
                                                               current_machine, current_due_date,
                                                               current_part_number,
                                                               current_quantity,
                                                               current_description, current_status, current_engineer)
                    elif current_status == status.PICKED:
                        self.picked_change = part_assignment(self.picked_change,
                                                                   current_machine, current_due_date,
                                                                   current_part_number,
                                                                   current_quantity,
                                                                   current_description, current_status,
                                                                   current_engineer)
                    elif current_status == status.ISSUED:
                        self.issued_change = part_assignment(self.issued_change,
                                                                   current_machine, current_due_date,
                                                                   current_part_number,current_quantity,
                                                                   current_description, current_status,
                                                                   current_engineer)

                    self.modified.add(current_machine)

            else:
                self.new_demand = part_assignment(self.new_demand,current_machine,current_due_date,current_part_number,current_quantity,current_description,current_status,current_engineer)
                self.modified.add(current_machine)


        for id in self.past_cache:
            if id not in self.current_cache:
                past_machine = self.past_cache[id].machine
                past_part_number = self.past_cache[id].part_number
                past_quantity = self.past_cache[id].quantity
                past_description = self.past_cache[id].description
                past_due_date = self.past_cache[id].due_date
                past_status = self.past_cache[id].status
                past_engineer = self.past_cache[id].engineer
                if self.past_cache[id].status == status.DRIVING:
                    self.removed_demand = part_assignment(self.removed_demand,past_machine,past_due_date,past_part_number,past_quantity,past_description,past_status,past_engineer)
                    self.modified.add(past_machine)

    def status_sorter(self):
        # checks to see if project needs to be modifed and passes it to correct map to update pdfs in PdfManager
        for project in self.current_projects:
            for due_date in self.current_projects[project].target_dates:
                for part in self.current_projects[project].target_dates[due_date].parts:
                    current_machine = project
                    current_part_number = part
                    current_quantity = self.current_projects[project].target_dates[due_date].parts[part].quantity
                    current_description = self.current_projects[project].target_dates[due_date].parts[part].description
                    current_due_date = due_date
                    current_status = self.current_projects[project].target_dates[due_date].parts[part].status
                    current_engineer = self.current_projects[project].target_dates[due_date].parts[part].engineer
                    current_inventory = self.current_projects[project].target_dates[due_date].parts[part].inventory
                    if current_status == status.DRIVING:
                        if project in self.modified:
                            self.driving_modified = part_assignment(self.driving_modified,current_machine,current_due_date,current_part_number,current_quantity,current_description,current_status,current_engineer, current_inventory)
                        self.driving = part_assignment(self.driving_modified,current_machine,current_due_date,current_part_number,current_quantity,current_description,current_status,current_engineer, current_inventory)
                    elif current_status == status.ISSUED:
                        if project in self.modified:
                            self.issued_modified = part_assignment(self.issued_modified, current_machine,
                                                                current_due_date, current_part_number,
                                                                current_quantity, current_description,
                                                                current_status, current_engineer, current_inventory)
                        self.issued = part_assignment(self.issued_modified, current_machine,
                                                                current_due_date, current_part_number,
                                                                current_quantity, current_description,
                                                                current_status, current_engineer, current_inventory)

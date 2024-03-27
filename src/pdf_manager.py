from fpdf import FPDF
import time
import os
import datetime
from email_manager import EmailManager
from email_directory import EmailDirectory
from email_messages import EmailMessages
from utility import is_number
class PdfManager:
    def __init__(self,delta=None):
        self.delta = delta
        self.TITLE = "R&D Sheet Update"
        self.driving_folder_path = "M:\\_R&D List Docs\\pdfs\\DRIVING"
        self.issued_folder_path = "M:\\_R&D List Docs\\pdfs\\ISSUED"
        self.email_file_path = f"M:\\_R&D List Docs\\DependencyFiles\\{self.TITLE}.pdf"
        self.send_attempts = 0


    def create_driving_pdfs(self,demand):
        font_style = "Helvetica"
        error_email = EmailManager()
        engineer_email = EmailDirectory()
        # generate pdf for all projects in hash
        current_demand = demand
        for project in current_demand:
            due_dates = list(current_demand[project].target_dates)
            sorted_dates = sorted(due_dates)
            pdf = FPDF(orientation="P", unit="pt", format="Letter")
            pdf.add_page()
            pdf.set_font(family=font_style , style="B", size=34)
            pdf.multi_cell(w=0, h=50, txt=str(project), align="C")  # create pdf header with title of project
            for due_date in sorted_dates:
                pdf.set_font(family=font_style , style="B", size=24)
                pdf.multi_cell(w=0, h=50, txt=due_date)  # create pdf header with title of project
                pdf.set_font(family=font_style, style="B", size=18)
                for part in current_demand[project].target_dates[due_date].parts:
                    current_part = current_demand[project].target_dates[due_date].parts[part]
                    if not is_number(current_part.quantity):
                        pdf.set_text_color(200, 0, 0)
                        pdf.multi_cell(w=0, h=50,txt=f"     {part}:  {current_part.description}  REQ: ({current_part.quantity}) \n   OH: {current_part.inventory} (QTY FAILED FLOAT CONVERSION)")
                        pdf.set_text_color(0, 0, 0)
                        continue
                    elif current_part.inventory != "Not Found" and float(current_part.quantity) <= float(current_part.inventory):
                        pdf.set_text_color(0,200,0)
                    else:
                        pdf.set_text_color(0,0,0)
                    pdf.multi_cell(w=0, h=50, txt=f"     {part}:  {current_part.description}  REQ: ({current_part.quantity}X) \n   OH: {current_part.inventory}")
                    pdf.set_text_color(0,0,0)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = project.replace("/", "-")
            filename = filename.replace("?", "")
            filename += f" {current_time}"
            filename = filename.replace(":", "-")
            print(filename)
            while True:
                if self.send_attempts == 30:
                    msg = EmailMessages(project)
                    message = msg.error_encoding_pdf
                    error_email.error_email(message, engineer_email.get_email(current_part.engineer))#
                try:
                    pdf.output(f"{self.driving_folder_path}//{filename}.pdf")
                    break
                except Exception as e:
                    print(f"{e} PDF cant encode")
                    time.sleep(10)
                    self.send_attempts +=1
    def create_issued_pdfs(self,demand):
        font_style = "Arial"
        for project in demand:
            for target_date in demand[project].target_dates:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                title = f"{project}"
                # generate pdf for all projects in hash
                pdf = FPDF(orientation="P", unit="pt", format="Letter")
                pdf.add_page()
                pdf.set_font(family=font_style , style="B", size=28)
                pdf.multi_cell(w=0, h=50, txt=f"{title} Issued: {current_time}")  # create pdf header with title of project
                for part in demand[project].target_dates[target_date].parts:
                    current_part = demand[project].target_dates[target_date].parts[part]
                    pdf.set_font(family=font_style , style="B", size=18)
                    pdf.multi_cell(w=0, h=50, txt=f"    {part}:  {current_part.description}  ({current_part.quantity}X)  REQ by: {current_part.engineer}\n    Notes: {current_part.notes}")
                while True:  # make sure this still works as intended
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    filename = f"{title} {current_time}"
                    filename = filename.replace("/", "-")
                    filename = filename.replace(":", "-")
                    filename = filename.replace("?", "")
                    try:
                        pdf.output(f"{self.issued_folder_path}//{filename}.pdf")
                        time.sleep(1)
                        break
                    except Exception as e:
                        print(f"{e} PDF Still Open")
                        time.sleep(10)

    def create_activity_pdf(self):
        font_size_title = 34
        font_size_project = 24
        font_size_action = 24
        font_size_date = 20
        font_size_part = 18
        font_style = "Arial"
        # generate pdf for all projects in hash
        pdf = FPDF(orientation="P", unit="pt", format="Letter")
        pdf.add_page()
        pdf.set_font(family=font_style , style="B", size=font_size_title)
        pdf.multi_cell(w=0, h=50, txt=self.TITLE, align="C")
        for action in self.delta.activity:
            if self.delta.activity[action] != {}:
                pdf.set_font(family= font_style, style="B", size=font_size_action)
                pdf.multi_cell(w=0, h=50, txt=str(action), align="C")
            else:
                continue
            for current_project in self.delta.activity[action]:
                pdf.set_font(family=font_style , style="B", size=font_size_project)
                pdf.multi_cell(w=0, h=50, txt=str(current_project))
                for target_date in self.delta.activity[action][current_project].target_dates:
                    pdf.set_font(family=font_style , style="B", size=font_size_date)
                    pdf.multi_cell(w=0, h=50, txt=str(target_date))
                    for part in self.delta.activity[action][current_project].target_dates[target_date].parts:
                        current_part = self.delta.activity[action][current_project].target_dates[target_date].parts[part]
                        pdf.set_font(family=font_style , style="B", size=font_size_part)
                        pdf.multi_cell(w=0, h=50, txt=f"     {part}:  {current_part.description}  ({current_part.quantity}X)")
        while True:  # make sure this still works as intended
            try:
                pdf.output(self.email_file_path)
                break
            except Exception as e:
                print(f"{e} PDF Still Open")
                time.sleep(10)
    def pdf_removed_demand(self,demand):
        timestamp_length = -20
        for filename in os.listdir(self.driving_folder_path):
            project = filename.removesuffix(".pdf")[:timestamp_length]
            if project not in demand:
                file_path = os.path.join(self.driving_folder_path,filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")
    def pdf_project_cleanup(self):
        for filename in os.listdir(self.driving_folder_path):
            file_path = os.path.join(self.driving_folder_path, filename)
            if file_path[-3:]== "pdf":
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

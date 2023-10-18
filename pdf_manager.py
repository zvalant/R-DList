from fpdf import FPDF
import time
import os

class PdfManager:
    def __init__(self,delta=None):
        self.delta = delta
        self.TITLE = "R&D Sheet Update"
        self.driving_folder_path = "G:\\SW\\_Administration\\R&D Items Test\\pdfs\\DRIVING_2"
        self.issued_folder_path = "G:\\SW\\_Administration\\R&D Items Test\\pdfs\\ISSUED_2"
        self.email_file_path = f"G:\\SW\\_Administration\\R&D Items Test\\pdfs\\EMAIL_PDFS\\{self.TITLE}.pdf"


    def create_driving_pdfs(self,demand):
        # generate pdf for all projects in hash
        current_demand = demand
        for project in current_demand:
            due_dates = list(current_demand[project].target_dates)
            sorted_dates = sorted(due_dates)
            pdf = FPDF(orientation="P", unit="pt", format="Letter")
            pdf.add_page()
            pdf.set_font(family="Times", style="B", size=34)
            pdf.multi_cell(w=0, h=50, txt=str(project), align="C")  # create pdf header with title of project
            for due_date in sorted_dates:
                pdf.set_font(family="Times", style="B", size=24)
                pdf.multi_cell(w=0, h=50, txt=due_date)  # create pdf header with title of project
                pdf.set_font(family="Times", style="B", size=18)
                for part in current_demand[project].target_dates[due_date].parts:
                    current_part = current_demand[project].target_dates[due_date].parts[part]
                    if current_part.inventory != "Not Found" and float(current_part.quantity) <= float(current_part.inventory):
                        pdf.set_text_color(0,200,0)
                    else:
                        pdf.set_text_color(0,0,0)
                    pdf.set_font(family="Times", style="B", size=18)
                    pdf.multi_cell(w=0, h=50, txt=f"     {part}:  {current_part.description}  REQ: ({current_part.quantity}X)    OH: {current_part.inventory}")
                    pdf.set_text_color(0,0,0)
            filename = project.replace("/", "-")
            filename = filename.replace("?", "")
            while True:  # make sure this still works as intended
                try:
                    pdf.output(f"{self.driving_folder_path}//{filename}.pdf")
                    break
                except Exception as e:
                    print(f"{e} PDF Still Open")
                    time.sleep(10)
    def create_issued_pdfs(self,demand):
        for project in demand:
            for target_date in demand[project].target_dates:
                title = f"{project} {target_date}"
                # generate pdf for all projects in hash
                pdf = FPDF(orientation="P", unit="pt", format="Letter")
                pdf.add_page()
                pdf.set_font(family="Times", style="B", size=24)
                pdf.multi_cell(w=0, h=50, txt=title)  # create pdf header with title of project
                for part in demand[project].target_dates[target_date].parts:
                    current_part = demand[project].target_dates[target_date].parts[part]
                    pdf.set_font(family="Times", style="B", size=18)
                    pdf.multi_cell(w=0, h=50, txt=f"     {part}:  {current_part.description}  ({current_part.quantity}X)  REQ by: {current_part.engineer}")
                    filename = title.replace("/", "-")
                    filename = filename.replace("?", "")
                while True:  # make sure this still works as intended
                    try:
                        pdf.output(f"{self.issued_folder_path}//{filename}.pdf")
                        break
                    except Exception as e:
                        print(f"{e} PDF Still Open")
                        time.sleep(10)

    def create_activity_pdf(self):
        # generate pdf for all projects in hash
        pdf = FPDF(orientation="P", unit="pt", format="Letter")
        pdf.add_page()
        pdf.set_font(family="Times", style="B", size=34)
        pdf.multi_cell(w=0, h=50, txt=self.TITLE, align="C")
        for action in self.delta.activity:
            if self.delta.activity[action] != {}:
                pdf.set_font(family="Times", style="B", size=24)
                pdf.multi_cell(w=0, h=50, txt=str(action), align="C")
            else:
                continue
            for current_project in self.delta.activity[action]:
                pdf.set_font(family="Times", style="B", size=18)
                pdf.multi_cell(w=0, h=50, txt=str(current_project))
                for target_date in self.delta.activity[action][current_project].target_dates:
                    pdf.multi_cell(w=0, h=50, txt=str(target_date))
                    for part in self.delta.activity[action][current_project].target_dates[target_date].parts:
                        current_part = self.delta.activity[action][current_project].target_dates[target_date].parts[part]
                        pdf.set_font(family="Times", style="B", size=18)
                        pdf.multi_cell(w=0, h=50, txt=f"     {part}:  {current_part.description}  ({current_part.quantity}X)")
        while True:  # make sure this still works as intended
            try:
                pdf.output(self.email_file_path)
                break
            except Exception as e:
                print(f"{e} PDF Still Open")
                time.sleep(10)
    def pdf_cleanup(self,demand):
        for filename in os.listdir(self.driving_folder_path):
            project = filename.removesuffix(".pdf")
            if project not in demand:
                file_path = os.path.join(self.driving_folder_path,filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")


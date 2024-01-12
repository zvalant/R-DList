import time
from demand_sheet import DemandSheet
from data_comparison import DataComparison
from pdf_manager import PdfManager
import utility
from email_manager import EmailManager
TESTMODE = False
CURRENT_FILE = "R&D Items Due.xlsx"
PAST_FILE = "R&D Items Due_p.csv"
ISSUED_FILE = "R&D Items Due_Issued.xlsx"
DEMAND_PAST_FILE = f"M:\\_R&D List Docs\\DependencyFiles\\{PAST_FILE}"
DEMAND_CURRENT_FILE = f"G:\\SW\\_Administration\\R&D Items Due\\{CURRENT_FILE}"
ISSUED_EXCEL_FILE = f"M:\\_R&D List Docs\\{ISSUED_FILE}"
demand_sheet_past = DemandSheet(DEMAND_PAST_FILE)
demand_sheet_current = DemandSheet(DEMAND_CURRENT_FILE)


formatted_date = utility.current_mrp_date()
MRP_FILEPATH = f"S:\\IT\\Reports\\MRP\\MRP-{formatted_date}.txt"

if TESTMODE:
    while True:
        demand_sheet_past.create_dataframe() #create dataframes for current and past files
        demand_sheet_current.create_dataframe()
        demand_sheet_past.demand_generator(demand_sheet_past.dataframe,PAST_FILE)
        demand_sheet_current.demand_generator(demand_sheet_current.dataframe,CURRENT_FILE) # generate projects for current sheet
        sheet_delta = DataComparison(demand_sheet_current, demand_sheet_past) # pass data to compare both dataframes
        demand_sheet_current.dataframe = sheet_delta.activity_search(demand_sheet_current.dataframe, demand_sheet_past.dataframe)
        sheet_delta.status_sorter() # create issued and driving maps and pass info to make pdfs
        pdf_actions = PdfManager(sheet_delta)
        sheet_delta.driving = utility.inventory_update(sheet_delta.driving, MRP_FILEPATH)
        pdf_actions.pdf_project_cleanup()
        pdf_actions.create_driving_pdfs(sheet_delta.driving)
        if sheet_delta.modified:
            pdf_actions.create_issued_pdfs(sheet_delta.issued_change)
            utility.excel_export(sheet_delta.issued_change, ISSUED_EXCEL_FILE)
            pdf_actions.create_activity_pdf()
            send_email = EmailManager(pdf_actions.email_file_path)
            send_email.send_activity_pdf()
            send_email.close_smtp_connection()
        while True:
            try:
                demand_sheet_current.dataframe.to_csv(DEMAND_PAST_FILE)
                break
            except Exception as e:
                print(f"Excel sheet currently being modified or cannot be found {e}")
                time.sleep(30)
        time.sleep(30)
else:
    while True:
        utility.target_sleep("5:00:00")
        demand_sheet_past.create_dataframe() #create dataframes for current and past files
        demand_sheet_current.create_dataframe()
        demand_sheet_past.demand_generator(demand_sheet_past.dataframe,PAST_FILE)
        demand_sheet_current.demand_generator(demand_sheet_current.dataframe,CURRENT_FILE) # generate projects for current sheet
        sheet_delta = DataComparison(demand_sheet_current, demand_sheet_past) # pass data to compare both dataframes
        demand_sheet_current.dataframe = sheet_delta.activity_search(demand_sheet_current.dataframe,demand_sheet_past.dataframe)
        sheet_delta.status_sorter() # create issued and driving maps and pass info to make pdfs
        pdf_actions = PdfManager(sheet_delta)
        sheet_delta.driving = utility.inventory_update(sheet_delta.driving, MRP_FILEPATH)
        pdf_actions.pdf_project_cleanup()
        pdf_actions.create_driving_pdfs(sheet_delta.driving)
        if sheet_delta.modified:
            pdf_actions.create_issued_pdfs(sheet_delta.issued_change)
            utility.excel_export(sheet_delta.issued_change, ISSUED_EXCEL_FILE)
            pdf_actions.create_activity_pdf()
            utility.target_sleep("7:00:00")
            send_email = EmailManager(pdf_actions.email_file_path)
            send_email.send_activity_pdf()
            send_email.close_smtp_connection()
        while True:
            try:
                demand_sheet_current.dataframe.to_csv(DEMAND_PAST_FILE)
                break
            except Exception as e:
                print(f"Excel sheet currently being modified or cannot be found {e}")
                time.sleep(30)

        utility.target_sleep("00:00:00")



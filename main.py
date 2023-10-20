import pandas as pd
import time
import datetime
from demand_sheet import DemandSheet
from data_comparison import DataComparison
from pdf_manager import PdfManager
import utility
from email_manager import EmailManager
CURRENT_FILE = "R&D Items Due_test.xlsx"
PAST_FILE = "R&D Items Due_test_p.csv"
DEMAND_PAST_FILE = f"C:\\Users\\ZacV\\PycharmProjects\\R&DRepo\\{PAST_FILE}"
DEMAND_CURRENT_FILE = f"C:\\Users\\ZacV\\PycharmProjects\\R&DRepo\\{CURRENT_FILE}"
demand_sheet_past = DemandSheet(DEMAND_PAST_FILE)
demand_sheet_current = DemandSheet(DEMAND_CURRENT_FILE)

formatted_date = utility.current_mrp_date()
MRP_FILEPATH = f"S:\\IT\\Reports\\MRP\\MRP-{formatted_date}.txt"
demand_sheet_past.create_dataframe() #create dataframes for current and past files
demand_sheet_current.create_dataframe()
demand_sheet_past.demand_generator(demand_sheet_past.dataframe,PAST_FILE)
demand_sheet_past.projects = utility.inventory_update(demand_sheet_past.projects,MRP_FILEPATH)
startup_pdfs = PdfManager()
startup_pdfs.create_driving_pdfs(demand_sheet_past.projects) # create pdfs for past projects
demand_sheet_current.demand_generator(demand_sheet_current.dataframe,CURRENT_FILE) # generate projects for current sheet
sheet_delta = DataComparison(demand_sheet_current, demand_sheet_past) # pass data to compare both dataframes
sheet_delta.activity_search(demand_sheet_current.dataframe)
sheet_delta.status_sorter() # create issued and driving maps and pass info to make pdfs
pdf_actions = PdfManager(sheet_delta)
sheet_delta.driving = utility.inventory_update(sheet_delta.driving,MRP_FILEPATH)
pdf_actions.create_driving_pdfs(sheet_delta.driving_modified)
pdf_actions.create_issued_pdfs(sheet_delta.issued_modified)
pdf_actions.create_activity_pdf()
pdf_actions.pdf_cleanup(sheet_delta.driving)
send_email = EmailManager()
send_email.send_activity_pdf()
demand_sheet_current.dataframe.to_csv(DEMAND_PAST_FILE)


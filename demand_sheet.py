import pandas as pd
import time
from email_manager import EmailManager
from email_messages import EmailMessages
import dataframe_column_titles as dct
import utility
from id_values import IDValues
from email_directory import EmailDirectory

class DemandSheet:
    def __init__(self, file):
        self.filepath = file
        self.projects = {}
        self.key_cache = {}
        self.all_parts = {}
        self.dataframe = None

    def create_dataframe(self):
        time_delay = 10
        if self.filepath[-5:] == ".xlsx":
            while True:
                try:
                    # converters allows leading zeros
                    self.dataframe = pd.read_excel(self.filepath, converters={dct.PART_NUMBER: str})
                    break
                except Exception as e:
                    print(f"Excel sheet currently being modified or cannot be found {e}")
                    time.sleep(time_delay)
        elif self.filepath[-4:] == ".csv":
            while True:
                try:
                    self.dataframe = pd.read_csv(self.filepath, converters={dct.PART_NUMBER: str})
                    break
                except Exception as e:
                    print(f"csv sheet currently being modified or cannot be found {e}")
                    time.sleep(time_delay)
        self.dataframe = self.dataframe_setup()
        pd.options.display.width = None  # options to display df correctly for print options
        pd.options.display.max_columns = None
        pd.set_option("display.max_rows", 3000)
        pd.set_option("display.max_columns", 3000)
        return self.dataframe

    def dataframe_setup(self):
        self.dataframe.dropna(how="all", inplace=True)
        updated_dates = []
        for i in range(len(self.dataframe)):
            try:
                date_val = self.dataframe.at[i,dct.DUE_DATE]
                # set date format to mmddyy
                formatted_date = pd.to_datetime(date_val)
                formatted_date = formatted_date.strftime("%m-%d-%Y")
                updated_dates.append(formatted_date)

            except Exception as e:
                updated_dates.append(date_val)
        self.dataframe[dct.DUE_DATE] = updated_dates



        dataframe = self.dataframe.astype(str).fillna('')  # remove any empty cells with an empty string
        return dataframe

    def demand_generator(self, demand_sheet,file_name):
        self.projects = {}
        self.key_cache = {}
        machine_val = "Not Found" #initalize starting attributes to find comparisons
        date_val = "Not Found"
        status_val = "Not Found"
        engr_val = "Not Found"
        error_email = EmailManager()
        engineer_email = EmailDirectory()

        for row in range(len(demand_sheet)):
            machine_val, date_val, status_val, engr_val, key = utility.part_attribute_finder(row, demand_sheet, machine_val,
                                                                                         date_val, status_val, engr_val)
            msg = EmailMessages(file_name, row)

            if key in self.key_cache:
                message = msg.error_key_collision
                error_email.error_email(message,engineer_email.get_email(engr_val))
                self.dataframe = self.dataframe.drop(row)
                print("Collision Email Sent!")
                continue
            elif key == "nan":
                message = msg.error_key_not_assigned
                error_email.error_email(message, engineer_email.get_email(engr_val))
                self.dataframe = self.dataframe.drop(row)
                # make error messge later
                continue
            current_part = demand_sheet[dct.PART_NUMBER][row]  # setup current part and project
            current_project = f"{machine_val}"
            quantity = demand_sheet[dct.QUANTITY][row]
            description = demand_sheet[dct.DESCRIPTION][row]
            #check to see if part exists in project already and generate error if it exists.
            if current_project not in self.projects or date_val not in self.projects[current_project].target_dates or current_part not in self.projects[current_project].target_dates[date_val].parts:
                self.projects = utility.part_assignment(self.projects,current_project,date_val,current_part,quantity,description,status_val,engr_val)
            else:
                message = msg.error_duplicate_part
                error_email.error_email(message,engineer_email.get_email(engr_val))
                self.dataframe = self.dataframe.drop(row)
                continue

            self.all_parts[current_part] = "Not Found"
            self.key_cache[key] = IDValues(machine_val, current_part, demand_sheet[dct.QUANTITY][row],
                                   demand_sheet[dct.DESCRIPTION][row],
                                   date_val, status_val, engr_val)  # update cache if valid entry
        return self.projects




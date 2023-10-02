import pandas as pd
import time

import dataframe_column_titles as dct
import project_creation as pc

class DemandSheet:
    def __init__(self,file):
        self.filepath = f"G:\\SW\\_Administration\\R&D Items Test\\{file}"
        self.projects = {}
        self.key_cache = {}
        self.dataframe = None
    def create_dataframe(self):
        time_delay = 10
        if self.filepath[-5:] == ".xlsx":
            while True:
                try:
                    demand_sheet = pd.read_excel(self.filepath)
                    break
                except Exception as e:
                    print(f"Excel sheet currently being modified or cannot be found {e}")
                    time.sleep(time_delay)
        elif self.filepath[-4:] == ".csv":
            while True:
                try:
                    demand_sheet = pd.read_csv(self.filepath)
                    break
                except Exception as e:
                    print(f"csv sheet currently being modified or cannot be found {e}")
                    time.sleep(time_delay)
        demand_sheet = self.dataframe_setup(demand_sheet)
        pd.options.display.width = None  # options to display df correctly for print options
        pd.options.display.max_columns = None
        pd.set_option("display.max_rows", 3000)
        pd.set_option("display.max_columns", 3000)
        self.dataframe = demand_sheet
        return self.dataframe

    def dataframe_setup(self,dataframe):
        integer_conversion = [dct.PART_NUMBER,dct.QUANTITY]
        dataframe.dropna(how="all", inplace=True)  # make helper function for df modification
        dataframe[dct.DUE_DATE] = pd.to_datetime(dataframe[dct.DUE_DATE])
        dataframe[dct.DUE_DATE] = dataframe[dct.DUE_DATE].dt.strftime('%m-%d-%y')  # set date to specific format
        for i in integer_conversion:
            dataframe[i] = dataframe[i].apply(int)  # change pn and qty to be integers
        dataframe = dataframe.astype(str).fillna('')  # remove any empty cells with an empty string
        return dataframe



    def demand_generator(self,demand_sheet):
        machine_val = demand_sheet[dct.MACHINE][0]
        date_val = demand_sheet[dct.DUE_DATE][0]
        status_val = demand_sheet[dct.STATUS][0]
        engr_val = demand_sheet[dct.ENGINEER][0]
        for i in range(len(demand_sheet)):
            machine_val, date_val, status_val, engr_val, key = pnattributefinder(i, demand_sheet, machine_val,
                                                                                 date_val, status_val, engr_val)
            if key in self.key_cache:
                print("Key Collision")  # create collision error and send in email
                #generate error message/email later
                return True
            elif key == "nan":
                self.error_found = True  # send notification that ID is needed on the corresponding row
                self.error_msg = f"Error found in past CSV File. Please provide a unique ID in row {i + 2}"
                return True
            current_part = demand_sheet[dct.PART_NUMBER][i]  # setup current part and project
            current_project = f"{machine_val}"
            if current_project not in self.projects:
                self.projects[current_project] = pc.Project(machine_val)
            if date_val not in self.projects[current_project].target_dates:
                self.projects[current_project].add_date(date_val)
            if current_part not in self.projects[current_project].target_dates[date_val].parts:
                self.projects[current_project].target_dates[date_val].add_part(current_part,demand_sheet[dct.QUANTITY][i],demand_sheet[dct.DESCRIPTION][i],status_val,engr_val)

        return self.projects
        """
              projects[current_project] = project(machine_val, date_val)  # add project if it doesnt exist
            if current_part not in projects[current_project].parts:  # add part number to project if it doesnt exist
                projects[current_project].addpart(current_part, dataframe_past[qty][i], dataframe_past[desc][i], status_val,
                                                  engr_val)
            else:
                self.error_msg = f"Error found in past CSV File. {current_part} on row {i + 2} needs to be modified due to part already driving on {current_project}"
                self.error_found = True
                return True
            self.key_cache[key] = [machine_val, dataframe_past[pn][i], dataframe_past[qty][i], dataframe_past[desc][i],
                                   date_val, status_val, engr_val]
        """

def pnattributefinder(i, df, machine_val, date_val, status_val, engr_val):
    date_tgt = 'Due Date'  # constants used for project and part setup
    machine = "Machine"
    status = "Status"
    engr = "Engineer"
    unique_id = "UniqueID"
    if machine_val != df[machine][i] and df[machine][i] != "nan":  # maintian correct machine
        machine_val = df[machine][i]
    if date_val != df[date_tgt][i] and df[date_tgt][i] != "nan":  # maintain correct date
        date_val = df[date_tgt][i]
    if status_val != df[status][i] and df[status][i] != "nan":  # maintain correct status
        status_val = df[status][i]
    if engr_val != df[engr][i] and df[engr][i] != "nan":  # maintain correct engineer
        engr_val = df[engr][i]
    key = df[unique_id][i]
    return machine_val, date_val, status_val, engr_val, key




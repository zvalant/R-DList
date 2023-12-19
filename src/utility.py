import project_creation as pc
import time
from datetime import datetime, timedelta
import dataframe_column_titles as dct
import pandas as pd

def part_attribute_finder(i, df, machine_val, date_val, status_val, engr_val,notes_val):
    if machine_val != df[dct.MACHINE][i] and df[dct.MACHINE][i] != "nan":  # maintian correct machine
        machine_val = df[dct.MACHINE][i]
    if date_val != df[dct.DUE_DATE][i] and df[dct.DUE_DATE][i] != "nan" and df[dct.DUE_DATE][i] !="NaT":  # maintain correct date
        date_val = df[dct.DUE_DATE][i]
    if status_val != df[dct.STATUS][i] and df[dct.STATUS][i] != "nan":  # maintain correct status
        status_val = df[dct.STATUS][i]
    if engr_val != df[dct.ENGINEER][i] and df[dct.ENGINEER][i] != "nan":  # maintain correct engineer
        engr_val = df[dct.ENGINEER][i]
    if df[dct.NOTES][i]!= "nan":
        notes_val = df[dct.NOTES][i]
    else:
        notes_val = "None"

    key = df[dct.UNIQUE_ID][i]
    return machine_val, date_val, status_val, engr_val, notes_val, key
def part_assignment(activity,project,due_date,part,qty,description,status,engineer,inventory="Not Found",notes="Not Found"):
    if project not in activity:
        activity[project] = pc.Project(project)
    if due_date not in activity[project].target_dates:
        activity[project].add_date(due_date)
    activity[project].target_dates[due_date].add_part(part,qty,description,status,engineer,inventory,notes)
    return activity
def current_mrp_date():
    current_date = datetime.today()
    current_time = datetime.now()
    current_time = current_time.hour
    if current_time < 4:
        current_date = current_date - timedelta(days=1)
    current_date = current_date.strftime("%d-%m-%Y")
    return current_date

def inventory_update(demand,file):
    attempts = 0
    all_parts = {}
    for project in demand:
        for date in demand[project].target_dates:
            for part in demand[project].target_dates[date].parts:
                all_parts[part] = "Not Found"

    while attempts < 3:
        try:
            with open(file,"r") as file:
                previous_line = None
                for line in file:
                    if previous_line != None:
                        previous_line_list =previous_line.split(" ") #matches sequence in text file to pull quantity on hand from MRP report
                        if len(previous_line_list) > 6 and previous_line_list[2] == "Item" and previous_line_list[3] == "Number:":
                            part_number = previous_line_list[4]
                            if part_number in all_parts:
                                qty_list = line.split(" ")
                                if len(qty_list) > 6 and qty_list[4] == "Hand:":
                                    all_parts[part_number] = qty_list[5]
                    previous_line = line
            for project in demand:
                for date in demand[project].target_dates:
                    for part in demand[project].target_dates[date].parts:
                        if part in all_parts:
                            demand[project].target_dates[date].parts[part].inventory = all_parts[part]
            break
        except Exception as e:
            print(e)
            time.sleep(10)
            attempts +=1
    return demand

def target_sleep(end_time):
    current_time = datetime.now().time()
    current_datetime = datetime.combine(datetime.today(), current_time)
    end_time_formatted = datetime.strptime(end_time, "%H:%M:%S").time()
    end_datetime = datetime.combine(datetime.today(), end_time_formatted)
    if end_time == "00:00:00":
        end_datetime = end_datetime + timedelta(days=1)
    while end_datetime > current_datetime:
        print("Too early")
        sleep_time = runtime_differential(current_datetime, end_datetime)
        time.sleep(sleep_time)
        current_datetime = datetime.combine(datetime.today(), datetime.now().time())


def excel_export(issued,file_path):
    while True:
        try:
            # converters allows leading zeros
            dataframe = pd.read_excel(file_path, converters={dct.PART_NUMBER: str})
            break
        except Exception as e:
            print(f"Excel sheet currently being modified or cannot be found {e}")
            time.sleep(5)
    for project in issued:
        for due_date in issued[project].target_dates:
            for part in issued[project].target_dates[due_date].parts:
                part_description = issued[project].target_dates[due_date].parts[part].description
                part_notes = issued[project].target_dates[due_date].parts[part].notes
                part_quantity= issued[project].target_dates[due_date].parts[part].quantity
                part_engineer = issued[project].target_dates[due_date].parts[part].engineer
                issued_date = datetime.today()
                issued_date = issued_date.strftime("%m-%d-%Y")
                dataframe.loc[len(dataframe.index)] = [project,part,part_quantity,part_description,part_notes,part_engineer, issued_date]

    while True:
        try:
            dataframe.to_excel(file_path, index=False)
            print("excel modified")
            break
        except Exception as e:
            print(f"Excel sheet currently being modified or cannot be found {e}")
            time.sleep(10)

def runtime_differential(start_datetime,end_datetime):
    diff = end_datetime-start_datetime
    diff_seconds = diff.total_seconds()+1
    return diff_seconds

def map_engineering_emails(file):
    engineer_map = {}
    try:
        with open(file,"r") as file:
            for line in file:
                if len(line) > 1:
                    name = line.split(".")[0].capitalize()
                    engineer_map[name] = line[:-1]
    except Exception as e:
        print(e)
    return engineer_map

def collect_recipients(file):
    recipients = []
    try:
        with open(file,"r") as file:
            for line in file:
                if len(line) >1:
                    recipients.append(line[:-1])
    except Exception as e:
        print(e)
    return recipients

def email_credentials(file):
    line_count = 1
    try:
        with open(file, "r") as file:
            for line in file:
                if line_count==1:
                    sender = line[:-1]
                elif line_count==2:
                    port = int(line[:-1])
                elif line_count==3:
                    server = line[:-1]
                line_count +=1
    except Exception as e:
        print(e)
    return sender,port,server

def date_refactor(dataframe):
    column_title = "Due Date"
    for index in range(len(dataframe[column_title])):
        current_date = dataframe.loc[index,column_title]
        if isinstance(current_date,float) and index>0:
            dataframe.loc[index, column_title] = dataframe.loc[index-1, column_title]
        elif isinstance(current_date,datetime):
            dataframe.loc[index,column_title] = dataframe.loc[index,column_title].strftime("%Y-%m-%d")
    return dataframe


import project_creation as pc
import time
import datetime
import dataframe_column_titles as dct

def part_attribute_finder(i, df, machine_val, date_val, status_val, engr_val):
    if machine_val != df[dct.MACHINE][i] and df[dct.MACHINE][i] != "nan":  # maintian correct machine
        machine_val = df[dct.MACHINE][i]
    if date_val != df[dct.DUE_DATE][i] and df[dct.DUE_DATE][i] != "NaT":  # maintain correct date
        date_val = df[dct.DUE_DATE][i]
    if status_val != df[dct.STATUS][i] and df[dct.STATUS][i] != "nan":  # maintain correct status
        status_val = df[dct.STATUS][i]
    if engr_val != df[dct.ENGINEER][i] and df[dct.ENGINEER][i] != "nan":  # maintain correct engineer
        engr_val = df[dct.ENGINEER][i]
    key = df[dct.UNIQUE_ID][i]
    return machine_val, date_val, status_val, engr_val, key
def part_assignment(activity,project,due_date,part,qty,description,status,engineer,inventory="Not Found"):
    if project not in activity:
        activity[project] = pc.Project(project)
    if due_date not in activity[project].target_dates:
        activity[project].add_date(due_date)
    activity[project].target_dates[due_date].add_part(part,qty,description,status,engineer,inventory)
    return activity
def current_mrp_date():
    current_date = datetime.datetime.today()
    current_time = datetime.datetime.now()
    current_time = current_time.hour
    if current_time < 4:
        current_date = current_date - datetime.timedelta(days=1)
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

from prettytable.colortable import ColorTable,Themes#A simple Python library for easily displaying tabular data in a visually appealing ASCII table format

from colorama import  Fore
import os

def handleCSVSql(logs):
    """
    Handles csv output for the logs in the sql file
    """
    fields =["Id","MachineName", "Username","Date", "Level", "Logger", "Callsite", "Message","Exception",]
    table=ColorTable(theme=Themes.OCEAN)
    table.field_names=fields
    for log in logs:
        try:
            values = list(log.values())#get the values of the dictionary
            table.add_row(values)
        except:
            pass
    csv= table.get_csv_string()
    print(Fore.BLUE,csv)
    try:
        with open("results.csv","w",encoding="UTF-8") as file:
            file.write(csv)
    except Exception as e:
        print(e)


def handleCSVText(logs):
    """
    Handles csv output for the logs in the text file
    """
    if(os.path.exists("results.csv")):
        os.remove("results.csv")
    for log in logs:
        log= log[1]
        if "method" in log  and len(log)==6:
            table=ColorTable(theme=Themes.OCEAN)
            method =["TaskId",
            "start-date-task",
            "start-task-time",
            "System",
            "method",
            "message-start"]
            table.field_names=method#for app 4,5
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)
        elif "resultCode" in log and len(log)==6:
            table=ColorTable(theme=Themes.OCEAN)
            resultCode =["TaskId",
            "finish-date-task",
            "finish-task-time",
            "System",
            "resultCode",
            "message-end"]
            table.field_names=resultCode#for app 4,5
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)
        elif len(log)==4 and "start-date-task" in log:
            table=ColorTable(theme=Themes.OCEAN)
            field=["start-date-task",
            "start-task-time",
            "System",
            "message-start"] 
            table.field_names=field#for app 4,5
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)
        elif len(log)==10:
            table=ColorTable(theme=Themes.OCEAN)
            field=["TaskId",
            "start-date-task",
            "start-task-time",
            "System",
            "method",
            "message-start",
            "finished-date-task",
            "finish-task-time",
            "resultCode",
            "message-end"]
            table.field_names=field#for app 4,5
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)
        elif "date" in log and "message" in log and "level" in log and len(log)==4:
            table=ColorTable(theme=Themes.OCEAN)
            field= ["date", "time", "level","message"]
            table.field_names=field
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)
        elif "date" in log and "message" in log and "time" in log and "id" in log:
            field =["date","time","id","message"]
            table=ColorTable(theme=Themes.OCEAN)
            table.field_names=field
            values =  list(log.values())
            table.add_row(values)
            csv= table.get_csv_string()
            writeCsvFile(csv+"\n")
            print(Fore.BLUE,csv)

def writeCsvFile(data):
    """
    append information to csv file
    """
    print(Fore.CYAN,"WRITING TO FILE...")
    try:
        with open("results.csv","a",encoding="UTF-8") as file:
            file.write(data)

    except Exception as e:
        print(Fore.RED,"ERROR WRITING TO FILE")
    print(Fore.CYAN,"DONE...")

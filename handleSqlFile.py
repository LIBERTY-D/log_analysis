import time#Module which handles time related tasks
import datetime#Module which deals with data and time 
from colorama import Fore#Module which allows to change color of the text on terminal
import re #Module which provides regular expression support



from myXML import handleSqlXml,readXmlData#write logs to xml file and read xml written
from myJSON import handleSqlJson,writeJsonFile#returns json log for sql file and writes logs to file
from myHTML import handleHtmlSql #handles html output for logs in sql file
from myCSV import handleCSVSql# Handles csv output for the logs in the sql file

def handleSqlFile(args,logs):
    """
    handles sql file
    """
    myLogs=[]
    print("====SEARCHING FOR DATA====")
    start=  datetime.datetime.now()
    print(Fore.GREEN+"started at@ ",start)
    time.sleep(2.4)#app sleep for 2.4 seconds
    data =  logs.strip()
    # print(data)
    pattern =r"INSERT \[dbo\]\.\[Logger\] \(\[Id\], \[MachineName\], \[UserName\], \[Date\], \[Level\], \[Logger\], \[Callsite\], \[Message\], \[Exception\]\)\s+VALUES\s+(\(.*\))"
    found =  re.finditer(pattern,data,re.DOTALL)
    if found:#checks if something is found or atleast is not None
        for _,item in enumerate(found):
            information = item.group().split("INSERT [dbo].[Logger] ([Id], [MachineName], [UserName], [Date], [Level], [Logger], [Callsite], [Message], [Exception])")#return an array so that i extract values
            for _,info in enumerate(information):
                
                if info=="":#if infor is an empty string
                    pass#do nothing
                else:
                    content = info.replace("VALUES","").replace("(","").replace("N","").replace("CAST","").replace(" AS DateTime)","").replace(")","").replace("'","").strip()#chaining to replace unwanted characters with empty space then strip to remove white space
                    content =  tuple(content.split(","))#returns  a list with content needed in mylogs
                    # print("printed",content)
                    sqlDb=(
                    "Id",
                    "MachineName",
                     "Username",
                    "Date",
                    "Level",
                    "Logger",
                    "Callsite",
                    "Message",
                    "Exception",
                        )
                    mydata =  list((zip(sqlDb,content)))
                    init ={

                    }
                    for myd in mydata:
                        key =myd[0]#key for the tuple
                        value=myd[1].strip()#value for the tuple
                        init[key]=value
                    myLogs.append(init)#put the dictionary in a list
                    init ={}
    if args.type=="json":
        jsonlogs =handleSqlJson(myLogs)
        print(Fore.BLUE,jsonlogs)
        time.sleep(2.4)
        print("WRITING TO FILE.........")
        print("DONE....")
        writeJsonFile("results.json",jsonlogs)
    elif args.type=="xml":
        handleSqlXml(myLogs)
        readXmlData("results.xml") 
    elif args.type=="html":
        print(Fore.BLUE,"WRITING TO HTML FILE(results.html)...")
        handleHtmlSql(myLogs)
        print(Fore.BLUE,"DONE..(CHECK results.html)")
    elif args.type =="csv":
        print(Fore.BLUE,"WRITING TO CSV FILE(results.csv)...")
        handleCSVSql(myLogs)
        print(Fore.BLUE,"DONE..(CHECK results.csv)")
    end =  datetime.datetime.now()-start
    print(Fore.GREEN+"Time taken is :",end)
    print(Fore.WHITE)
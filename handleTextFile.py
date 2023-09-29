import re#Module which provides regular expression support
import datetime#Module which deals with data and time 
from colorama import Fore #Module which allows to change color of the text on terminal
import time#Module which handles time related tasks

from errors import handleErrors#handles errors
from myXML import handlesTxtXml,readXmlData# xml read and write functionality
from myJSON import handleTxtJson,writeJsonFile#returns json log for text file and writes logs to file
from myHTML import handleHtmlText# Handles html output for the logs in the text file
from myCSV  import handleCSVText # Handles csv output for the logs in the text file

duplicateList =[] 
def handleTextFile(logs,args):
     """
     Searches through the text file for occurences of this information
     """
     # regex for app 4,5 text files
     app45reg =r'^\[{1}[0-9]*-[0-9]*-[0-9]*\s*[0-9]*[:][0-9]*:[0-9]*\.[0-9]*\]{1}\s+.{38}\s+\[[ERP XL|Executor|CORE]+\]*(.)*'
     dates = " "
     Id =  " "
     method = " "
     resultCode = ""
     resultCode = " " 
     messageInfo =" " 
     time_=""     
     taskId =[]  #stores unique ids
     
     main=[] #   contains logs of fetched data
     global duplicateList 
     print("====SEARCHING FOR DATA====")
     start=  datetime.datetime.now()
     print(Fore.GREEN+"started at@ ",start)
     time.sleep(2.4)#app sleep for 2.4 seconds

     data = regex(app45reg,logs)#loop through the regex pattern
     if data:#check for app4 and app5
          taskId = re.findall(r'TaskId\s*=\s*\d*',data)
          taskId= list(set(taskId))#unique id
         
          for i, id in enumerate(taskId):
                    id= id.replace("TaskId = "," ").strip()
                    taskId[i] = id
          result = data.split("\n")
          for resindex  in  range(len(result)):
               groups =  result[resindex]
               Id= re.findall(r'TaskId\s*=\s*\d*',groups)# if theres an id it means we dealing with task which has ids
               if   Id:
                    Id =  " ".join(Id).split("=")[1].strip()
                    dates =  re.findall(r'[0-9]*-[0-9]*-[0-9]*\s*[0-9]*[:][0-9]*:[0-9]*\.[0-9]*',groups)
                    if dates:
                         dateTime = " ".join(dates).strip().split(" ")
                         dates =dateTime[0]
                         time_ =dateTime[1]
                    method = re.findall(r'Method\s*=\s*\w*',groups)
                    if method:
                         method = " ".join(method).split("=")[1].strip()
                    resultCode = re.findall(r'ResultCode\s*=\s*\w*',groups)
                    if resultCode:
                         resultCode = " ".join(resultCode).split("=")[1].strip()
                    system = re.findall(r'ERP XL|Executor|CORE]+',groups)
                    if system:
                         system =  " ".join(system)
                    messageInfo  =  re.search(r"\[[ERP XL|Executor|CORE]+\]\s*",groups)
                    if messageInfo:
                         messageInfo =  groups[messageInfo.end():].split("[")[0]
                         
                    if resultCode == "FinishedOk":#append a dictionary with success resultcode
                         main.append({
                              "TaskId":Id,
                                        "finished-date-task":dates,
                                          "finish-task-time":time_,
                                             "System":system,
                                        "resultCode":resultCode,
                                        "message-end":messageInfo
                                        })
                    m= re.search(r"Method = ",groups)
                    if m:
                         #append  to a dictionary 
                         main.append({
                                   "TaskId":Id,
                                             "start-date-task":dates,
                                             "start-task-time":time_,
                                             "System":system,
                                             "method":method,
                                             "message-start":messageInfo,
                                             })
               
               else:#when no tasklist id
                    dates =  re.findall(r'[0-9]*-[0-9]*-[0-9]*\s*[0-9]*[:][0-9]*:[0-9]*\.[0-9]',groups)
                    if dates:
                         dateTime= " ".join(dates).strip().split(" ")
                         dates= dateTime[0]
                         time_= dateTime[1]
                    system = re.findall(r'ERP XL|Executor|CORE]+',groups)
               
                    if system:
                         system =  " ".join(system).strip("]")
                    messageInfo  =  re.search(r"\[[ERP XL|Executor|CORE]+\]\s*",groups)
                    if messageInfo:
                         messageInfo = groups[messageInfo.end():]
                    
                         main.append({"start-date-task":dates,
                                 "start-task-time":time_,
                                 "System":system,
                                 "message-start":messageInfo,
                                        })
                    
     else:#matches app12367
          if data != None:
               sentencePat =r"([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3,4}[\|Error\||\|Info\||\|Warn\|]+.*)"#search pattern
               matcher =  re.findall(sentencePat,logs)
               if matcher:#app 134567 text files
                    matcher  =  re.split(sentencePat,logs)
                    matcher =  list(filter(removeEmptyLine,matcher))
                    for match in matcher:
                         splittedMatch =   re.split(r"(\|Error\||\|Info\||\|Warn\|)",match,re.DOTALL)
                         if len(splittedMatch)==1 and (splittedMatch[0]=="\n" or splittedMatch[0]=="\n ") :#do nothing if list contains this
                              pass
                         else:
                              date =""
                              level=""
                              message=""
                              if len(splittedMatch)==3:
                                   dateTime = splittedMatch[0].split(" ")
                                   date = dateTime[0]
                                   time_= dateTime[1]
                                   level = splittedMatch[1].strip("|")
                                   message =  splittedMatch[2].strip("|")
                                   main.append({
                                        "date":date,
                                         "time":time_,
                                        "level":level,
                                        "message":message
                                   })
                              elif len(splittedMatch)==1:
                                   lastItemAdded = main[len(main)-1]
                                   lastItemAdded.update({
                                        "message":lastItemAdded["message"]+splittedMatch[0].strip("\n")
                                   })
               else:
                    sentencePat = r"([0-9]*.[0-9]*.[0-9]*\s*[0-9]*:[0-9]*:[0-9]*)\s+(\[.*\])\s(.*)"#search pattern which matches text files in app2
                    matcher = logs.split("\n")
                    for match in matcher:
                         matched = re.finditer(sentencePat,match)
                         for i, m in  enumerate(matched):
                              dateTime=m.group(1).split(" ")
                              date =dateTime[0]
                              time_= dateTime[1]
                              id = m.group(2)
                              message=m.group(3)
                              main.append({
                                        "date":date.strip(),
                                         "time":time_,
                                        "id":id.strip("]").strip("["),
                                        "message":message,
                                        
                              })
                                   
     for logIndex in range(len(main)):#loop through main list
          getLog = main[logIndex]#get items
          for index  in range(logIndex+1,len(main)):#loop which is one step ahead for comparison
               anLog = main[index]
               if "TaskId" in getLog and "TaskId" in anLog:#check if the item contains a TaskId
                    
                    if getLog["TaskId"]==anLog["TaskId"]:#if id are the same then merge

                         getLog.update(anLog)#update  getLog 
                         duplicateList.append(index)# add unwanted index for removal with the filter function
     try:
          workable = list(filter(remove,enumerate(main))) 
          # workable.pop(len(workable)-1)#remove last item which always appesrs to be empty
          if args.output == "json":
               jsonObject = handleTxtJson(workable)#function which return  json data
               print(Fore.BLUE+jsonObject)
               time.sleep(2.4)
               print("WRITING TO FILE.........")
               writeJsonFile("results.json",jsonObject)
               print("DONE....")
          elif args.output=="xml":
               handlesTxtXml(workable)#write logs to xml file function
               if len(workable)>0:
                    readXmlData("results.xml")#read xml data produced
          elif args.output=="html":
               handleHtmlText(workable)
          elif args.output=="csv":
               handleCSVText(workable)
     except Exception  as e:
          handleErrors(e)

     duplicateList =[]
     taskId=[] 
     main=[]           
     end =  datetime.datetime.now()-start
     print(Fore.GREEN+"Time taken is :",end)
     print(Fore.WHITE)
    
def regex(regp,logs):
     """
     regex function which returns matched data 
     """
     data =""
     if logs:
          matcher =  re.compile(regp,re.DOTALL)
          matched = matcher.finditer(logs)
          if matched:
               for index, item in enumerate(matched):
                    start = item.span()[0]
                    end =  item.span()[1]
                    data =logs[start:end]
               return data
         
def remove(index_item):
     """
     return item not in duplicate list
     """
     index,item = index_item
     if index not in  duplicateList:
          return index_item
def removeEmptyLine(log):
     """
     Return Items which are not a new line
     """
     if log !='\n ' or log !='\n':
          return log
     


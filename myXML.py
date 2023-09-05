
import os as OS#Module which provides functionality for OS systems
import xml.etree.ElementTree as ET #Module  which Allows manupulation of xml related function
import lxml.etree as lxml#Module  which Allows manupulation of xml related function
from colorama import Fore#Module which allows to change color of the text on terminal
from errors import handleErrors #my own module which handles errors


def handlesTxtXml(logs):
     """
     handles text logs  output format and writes them to a file called results.xml
     """
     root =  ET.Element("Logs")#create root element for Logs
     tree =  ET.ElementTree(root)#put root to tree structure
     data =[]
     for logIndex in range(len(logs)):
          index,log =  logs[logIndex]
          data.append(log)
     try:
          for item in data:
               Log =  ET.SubElement(root,"Log")
               if "TaskId" in item:
                    taskId = ET.SubElement(Log,"TaskId")
                    taskId.text =  item["TaskId"]

          
               if "start-date-task" in item:
                    dateStart =  ET.SubElement(Log,"StartDate")
                    dateStart.text=item["start-date-task"]
               if "finished-date-task" in item:
                    dateFinish = ET.SubElement(Log,"FinishDate")
                    dateFinish.text = item["finished-date-task"]
               if "System " in item:
                    System  = ET.SubElement(Log,"System")
                    System.text =item["System"]
          
               if "message-start" in item:
                    messageStart = ET.SubElement(Log,"MessageStart")
                    messageStart.text=item["message-start"]

               if "message-end" in item:
                    messageFinish = ET.SubElement(Log,"MessageFinish")
                    messageFinish.text = item["message-end"]
               if "resultCode" in item:
                    resusltCode =  ET.SubElement(Log,"ResultCode")
                    resusltCode.text = item["resultCode"]
               if "method" in item:
                    method =  ET.SubElement(Log,"Method")
                    method.text = item["method"]
               if "date" in item:
                    date = ET.SubElement(Log,"Date")
                    date.text =  item["date"]
               if "level" in item:
                    level =  ET.SubElement(Log,"Level")
                    level.text = item["level"]
               if "message" in item :
                    message = ET.SubElement(Log,"Message")
                    message.text = item["message"]

               tree.write("results.xml",encoding="UTF-8")#write to a file with this encoding
          logs=[]
     except Exception as err:
          handleErrors(err)   
    

def readXmlData(path):
     """
     Reading xml result file produced
     """
     if path:
          if OS.path.exists(path):
               temp = lxml.parse(path)# reading the xml  file
               new_xml = lxml.tostring(temp,pretty_print=True,encoding="unicode")
               print(Fore.BLUE+new_xml)
          else:
               print("Does not exist")
def handleSqlXml(logs):
     """
     Handles sql logs xml output
     """
     root =  ET.Element("Logs")#create root element for Logs
     tree =  ET.ElementTree(root)#put root to tree structure
     fields=["Id","MachineName","Username","Date", "Level", "Logger","Callsite","Message","Exception"]
     for log in logs:#iterate through the logs
          Log =  ET.SubElement(root,"Log")
          for key,value in log.items():#iterate through key value pairs in a dictionary
               if key in fields:
                    element = ET.SubElement(Log,key)
                    element.text=value
     tree.write("results.xml",encoding="UTF-8")
     logs=[]


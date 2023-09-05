import json#Python module which handles json serialization and deserialization
import time #Module which handles time related tasks
def writeJsonFile(fileName, jsondata):
     """
     Writes logs to file called results.json
     """
     try:
          with open(fileName,"w",errors="ignore") as file:
               file.write(jsondata)
     except Exception as e:
          print("Something went wrong while attempting to write to file")

def  handleTxtJson(logs):
     """
     Handles text file json output  and writes the logs to a file

     """
     data =[]
     for logIndex in range(len(logs)):
          _,log =  logs[logIndex]
          data.append(log)
     finalData = {
          "results":str(len(data)),
          "data":data,
     }
     jsonObject =  json.dumps(finalData,indent=4,ensure_ascii=False)
     return jsonObject


def handleSqlJson(logs):
     """
     handles sql json output for the logs and writes the logs to a file

     """
     myjsonData ={
           "results":str(len(logs)),
           "data":logs,
          
     }
     jsonObject =  json.dumps(myjsonData,indent=4,ensure_ascii=False)
     return jsonObject



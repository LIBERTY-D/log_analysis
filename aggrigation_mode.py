import time#Module which handles time related tasks
import sys#The sys module in Python provides various functions and variables that are used to manipulate different parts of the Python runtime environment. It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter. Let’s consider the below example.
import os#Module which provides functionality for OS systems
import json#Python module which handles json serialization and deserialization
import re #Module which provides regular expression support
from colorama import Fore#Module which allows to change color of the text on terminal


from errors import handleErrors,InvalidField,Mode#custom errors 
user_field =""
user_query = ""
def aggrigationMode(args):
    """
    Deals with aggrigation retated function for sql and txt json output logs
    """
    time.sleep(2.4)
    if(args.aggrigation_mode and args.input_type=="txt" and args.output=="json"):
        try:
             print("""The appropriate field to search is the one produced in results.json file.
                   Usage:
                   Field value

                   if theres space between values then enter quotation marks like below:
                   
                   Field "value1 example"
                   """)
             promptTxt()
        except KeyboardInterrupt as e:
            handleErrors(e)
            sys.exit(0)
            
        except Exception as e:
            print("unknown error")
            print(e.args)
            sys.exit(0)
    elif(args.aggrigation_mode and args.input_type=="sql" and args.output=="json"):
        try:
             print("""The appropriate field to search is the one produced in results.json file.
                   Usage:
                   Field value

                   if theres space between values then enter quotation marks like below:
                   
                   Field "value1 example"
                   """)
             promptSql()
        except KeyboardInterrupt as e:
            handleErrors(e)
            sys.exit(0)
            
        except Exception as e:
            print("unknown errorrr")
            print(e)
            sys.exit(0)
    elif(args.aggrigation_mode and args.output=="xml"):
         try:
              raise Mode("xml")
         except Mode as e:
              handleErrors(e)

def promptTxt():
     """
     Prompt input which allows user to enter field and value
     """
     global user_query
     global user_field
     exitText=""
     while exitText!="exit()":
              user = input(Fore.WHITE+"Enter field  and value fot filter: ")
              filename= "results.json"
              if os.path.exists(filename):
                   content = readFiles(filename=filename)
                   content =  json.loads(content)
                   results = content["results"]#number of results
                   data =  content["data"]#getting the lists containing the data
                   if re.search(r"\s",user) and not re.search(r".*\".*\"",user):
                        user_field = user.split(" ")[0].strip()#contains the field user wanna filter
                        user_query = user.split(" ")[1]#contains the information to filter
                        try:
                             if user_field and user_query:
                                  filtered = list(filter(textFilter,data))
                                  length = len(filtered)
                                  if length> 0:
                                       data = {
                                            "results":length,
                                            "data":filtered
                                       }
                                       print(Fore.BLUE+json.dumps(data,indent=4,ensure_ascii=False))
                                  else:  print(Fore.RED+"No such Filters")  
                        except InvalidField as e:
                            handleErrors(e)
                                  
                   elif re.search(r".*\".*\"",user):
                         user_field = user.split(" ")[0].strip()#contains the field user wanna filter
                         user_query = user.find("\"")
                         if user_query!=-1:
                            user_query = user[user_query:].strip("\"")#contains the information to filter
                            try:
                                if user_field and user_query:
                                    filtered = list(filter(textFilter,data))
                                    length = len(filtered)
                                    if length> 0:
                                        data = {
                                                "results":length,
                                                "data":filtered
                                        }
                                        print(Fore.BLUE+json.dumps(data,indent=4,ensure_ascii=False))
                                    else:
                                        print(Fore.RED,"NO SUCH FIELD EXIST")
                            except InvalidField as e:
                                handleErrors(e)        
              else:
                   print(Fore.RED+"File does not exist")
                   
              exitText=user#if user types exit() then program will terminate
     sys.exit(0)


def  promptSql():
     """
     prompt input for sql data which allows user to enter field and value
     """
     global user_query#stores query value
     global user_field #stores queried field
     exitText="" 
     filename= "results.json"
     fields=["Id","MachineName","Username","Date", "Level", "Logger","Callsite","Message","Exception"]
     content = readFiles(filename=filename)
     data=[]
     try:    
          content =  json.loads(content)
          data = content["data"]
     except:
          pass
     if len(data)>0:
          while exitText!="exit()":
               
               user = input(Fore.WHITE+"Enter Field and value for filter: ")
               exitText=user
               inputs =  user.split(" ")#seperate input by space
               if (len(inputs)==2):
                    user_field=inputs[0]
                    user_query =inputs[1]
                    if  user_field in fields:
                         myFilter = list(filter(sqlFilter,data))
                         print(Fore.CYAN,"YOUR FILTERED RESULTS")
                         filteredData = {"results":len(myFilter),
                              "data":myFilter
                         }
                         print(Fore.BLUE+json.dumps(filteredData,indent=4,ensure_ascii=False))
                    else:
                         print(Fore.RED,"NO SUCH FIELD EXIST")
     else:
          print(Fore.RED,"Exiting Aggrimode for results length 0.....")
          time.sleep(2.4)
          print(Fore.WHITE)
          sys.exit(0)
          

                   
def sqlFilter(logs):
     """
     Filters  sql logs for field and value
     """
     if user_field in logs:
          if logs[user_field].lower()==user_query.lower():
               return logs
     
          


def textFilter(data):
        """
        Allows user to Filter json txt file output according to field and value 
        """
        if user_field in data and  isinstance(data[user_field],list)==False and data[user_field] !=None:
            if ((user_query.lower()==data[user_field].strip().lower())):
                return data
            else:
                return []
    

def readFiles(filename):
     """
     Reads files
     """
     with open(filename,"r") as file:
          if(file.readable()):
            data =  file.read()
            return data
                    
               
            
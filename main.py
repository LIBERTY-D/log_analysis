import argparse#Module which  Allows to enter command line arhuments
import xml.etree.ElementTree as ET #Module  which Allows manupulation of xml related function
import lxml.etree as lxml #Module  which Allows manupulation of xml related function
from colorama import Fore#Module which allows to change color of the text on terminal


from errors import handleErrors#import my own module
from readFiles import readFile#reads files
from readApi import readFromApi#return api data
from handleTextFile import handleTextFile#main logic for text files
from banner import Banner#my banner
from aggrigation_mode import aggrigationMode#deals with aggrigation related functions
from handleSqlFile import handleSqlFile#handles sql file

def localizations(path,args,encode):
     """
     Reads logs from different environments
     """
     if (path.startswith("http") or path.startswith("https")):
          return readFromApi(path,args)
     else:
          return readFile(path,args,encode)

 
def main(args):
        """
        Main function to execute  everything
        """
        banner =  Banner("Log Analysis,The Next Generation")
        print(Fore.MAGENTA+banner)
        supportedExt = ["txt","sql"]#support extensions log file  for the application
        file =  args.file.split(".")
        ext =  file[len(file)-1]#get user ext for the file
        if ext in supportedExt:
          logs = localizations(args.file,args,"UTF-8")
          if args.input_type=="sql":
               handleSqlFile(args,logs)#handles the sql file
               
          elif args.input_type=="txt":
               handleTextFile(logs,args)
          aggrigationMode(args)
        else:
             print(Fore.RED,"PLEASE ENTER TXT or SQL extension")
             print(Fore.WHITE,"")
          
     

#command line arguments
argParser =  argparse.ArgumentParser(prog="LogApp",description="Logs Analysis Tool")
argParser.add_argument("-f","--file",help="add relative or absolute path or takes a url for requests ",required=True,type=str)
argParser.add_argument("-sl","--startline",help="line to start reading file",type=int)
argParser.add_argument("-el","--endline",help="Up to which line you want to read",type=int)
argParser.add_argument("-nl","--numberline",help="number of lines you want to read starting from -sl",type=int)
argParser.add_argument("-a","--all",help="""reads the whole file
                       (**NOTE**),make sure -sl and -nl are not specified otherwise it wont work!"""
                       ,action="store_true")
argParser.add_argument("-it","--input_type",help="Input Type File",default="txt",nargs="?",choices=["txt","sql"])
argParser.add_argument("-t","--type",help="output type formate for logs",default="json" ,nargs="?",choices=["xml","json","csv","html"])
argParser.add_argument("-am","--aggrigation_mode",help="Enters aggrigation mode for the genneration data for the lines your choose, so that you anaylis the data in mode detail",type=bool,default=False)
args =  argParser.parse_args()
try:
     main(args)#main function which calls all other functions
except KeyboardInterrupt as e:#ctrl-c handled
     handleErrors(e)

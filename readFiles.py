import sys#The sys module in Python provides various functions and variables that are used to manipulate different parts of the Python runtime environment. It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter. Let’s consider the below example.
import lxml.etree as lxml#Module  which Allows manupulation of xml related function
from errors import handleErrors #my own module which handles errors




def readFile(path,args,encode):
     """
     Read file with logs
     """
     logs =[]
     if(args.startline is not None  and args.numberline is not None and args.all==False and args.input_type=="txt"):
     
          try:#handle errors using try catch
               with open(path,"r",encoding=encode,errors='ignore') as file:     # open file
                    content = file.readlines()#   read file lines
                    start =  args.startline#gets line where user want to start reading
                    end =  args.numberline#gets the number of lines user want to read
                    total  =  start+end#logic to get the calculated lines
                    if start ==0:
                         logs = content[start:total]
                    else:
                         logs = content[start-1:total]
                    logs = " ".join(logs)   #join array into string
          except FileNotFoundError as e:
               handleErrors(e)
               sys.exit(0)
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
       
     elif args.all and args.input_type=="txt":
          try:#handle errors using try catch
               with open(path,"r",encoding=encode,errors='ignore') as file: #    open file
                    content = file.readlines()#read lines
                    logs =  " ".join(content)  
          except FileNotFoundError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
        
     elif (args.startline is not None and args.endline is not None and args.all==False and args.input_type=="txt"):
          try:
               with open(path,"r",encoding=encode,errors='ignore') as file:
                    content = file.readlines()
                    start =  args.startline
                    end =  args.endline
                    if start==0:
                         logs = content[start:end+1]
                    else :
                         logs = content[start-1:end]
                    logs = " ".join(logs)
          except FileNotFoundError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
        
     elif(args.startline is not  None and args.endline is  not  None and args.numberline is None and  args.all==False and args.input_type=="sql"):
          try:
               with open(path,"r",encoding="UTF-16LE") as file:
                    content = file.readlines()
                    start =  args.startline
                    end =  args.endline
                    if start==0:
                         logs = content[start:end+1]
                    else :
                         logs = content[start-1:end]
                    logs =  "".join(logs)
          except FileNotFoundError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
     elif(args.startline is not None  and args.numberline is not None and args.all==False and args.input_type=="sql"):
          try:#handle errors using try catch
               with open(path,"r",encoding="UTF-16LE") as file:     # open file
                    content = file.readlines()#   read file lines
                    start =  args.startline#gets line where user want to start reading
                    end =  args.numberline#gets the number of lines user want to read
                    total  =  start+end#logic to get the calculated lines
                    if start ==0:
                         logs = content[start:total]
                    else:
                         logs = content[start-1:total]
                    logs = " ".join(logs)   #join logs list into string
          except FileNotFoundError as e:
               handleErrors(e)
               sys.exit(0)
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
       

       
     elif args.all and args.input_type=="sql":
          try:#handle errors using try catch
               with open(path,"r",encoding="UTF-16LE") as file: #    open file
                    content = file.readlines()#read lines
                    logs =  "".join(content)  
          except FileNotFoundError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
          except OSError as e:
               handleErrors(e)#global function to handle errors
               sys.exit(0)#exit code if theres an error
     
     return logs

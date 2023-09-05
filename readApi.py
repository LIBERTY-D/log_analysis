import  requests#Module which allows  you to send HTTP requests using Python.
import sys#The sys module in Python provides various functions and variables that are used to manipulate different parts of the Python runtime environment. It allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter. Let’s consider the below example.
from errors import handleErrors#handles my errors

def readFromApi(path,args):
     """
     Makes an http get request to the server serving the file
     """
     logs =[]
     try:
          session =  requests.session()
          with session.get(path,stream=True) as res:
               status_code= res.status_code
               if status_code==200:#success code 200
                    if(args.startline is not None and args.endline is not None and args.all==False):
                         content = res.content.decode()
                         content = content.split("\r")
                         start =  args.startline
                         end =  args.endline
                         if start==0:
                              logs = content[start:end+1]
                         else :
                              logs = content[start-1:end]
                         logs = " ".join(logs)
                    elif(args.startline is not None  and args.numberline is not None and args.all==False):
                    
                         content = res.content.decode()#   read res
                         data =  content.split("\n")
                         
                         start =  args.startline#gets line where user want to start reading
                         end =  args.numberline#gets the number of lines user want to read
                         total  =  start+end#logic to get the calculated lines
                         if start ==0:
                              logs = data[start:total]
                         else:
                              logs = data[start-1:total]
                         
                         m =  list(map(lambda st:st.replace("\r","\n"),logs))#replace carriage character \r with \n 
                         logs="".join(m)
     
                    elif args.all:
                              content =  res.content.decode()
                              logs =  "".join(content)  
                    
                    
     except requests.exceptions.ConnectionError as e:#catch connection error eg when server is down
          handleErrors(e)
          sys.exit(9)

     except requests.exceptions.MissingSchema as e:#incorrect schema of the url 
          handleErrors(e)
          sys.exit(0)
     return logs

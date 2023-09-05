
import requests
from colorama import Fore

class InvalidField(Exception):
     """
     My custom exception
     """
     def __init__(self,message) -> None:
          self.message = message
     def myErrror(self):
          return self.message
class Mode(Exception):
     def __init__(self,message) -> None:
          self.message=message
     def mode(self):
          return self.message
          
     
errors ={
     UnicodeDecodeError:"Error Decoding File",
     FileNotFoundError:"File Not Found",
     UserWarning:"Output format not supported",
     KeyboardInterrupt:"Program interupted",
     requests.exceptions.ConnectionError:"connection err",
     requests.exceptions.MissingSchema:"invalid url",
     OSError:"Something went wrong..as a precaution check your path or url",
     InvalidField:"Invalid field",
     Mode:"Mode does not support the type of out put you want"
    
     

}
def handleErrors(error):
     """
     Handles application errors
     """
  
     if(type(error) in errors):#check if error is in the dictionary
          print(Fore.RED+errors[type(error)])#get error message
          print(Fore.WHITE)
     else:
          print("errrrr",error)

import pyfiglet# module which allows a few lines of the code, which creates fancy text in large size with the help of the screen characters

def Banner(text:str):
    """
    My App Banner
    """
    banner =  pyfiglet.figlet_format(text)
    return banner

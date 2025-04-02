from googleapiclient.discovery import build
from authenticate import authenticate
from googleapiclient.errors import HttpError

def connect_to_sheets():
    creds = authenticate(); 
    service = None
    try:
        service = build("sheets", "v4", credentials=creds)
    except HttpError as err:
        print(err)
    
    return service

   
   

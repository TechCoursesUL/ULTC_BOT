import firebase_admin
import json
import os
from firebase_admin import db

bannedUserExample = json.dumps(
    {
        192937297382: 
        {
            "displayname": "John Doe", #username when banned
            "endtime": 345345353434534, #unix time when ban ends
            "reason": "touched brown thomas", #banreason
        }       
    }
)

class ULTCDB:
    def __init__(self) -> None:
        self.cred_obj = firebase_admin.credentials.Certificate(os.getenv('DBAUTH'))
        self.app = firebase_admin.initialize_app(self.cred_obj, {'databaseURL' :'https://ultcdb-default-rtdb.europe-west1.firebasedatabase.app/'})
        
    def GetBannedUsers(self) -> json:
        print(f"getting banned users from db...")
        
        ref = db.reference("server/users/bannedusers")
        return ref.get()
    
    def SetBannedUsers(self, bannedUsers: json):
        ref = db.reference("server/users/bannedusers")
        ref.set(bannedUsers)




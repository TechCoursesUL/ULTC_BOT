import firebase_admin
import json
import os
import dotenv
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
dotenv.load_dotenv()

class ULTCDB:
    def __init__(self) -> None:
        self.app = firebase_admin.initialize_app( credential=firebase_admin.credentials.Certificate(json.loads(os.getenv("DBAUTH"))), options={'databaseURL' :'https://ultcdb-default-rtdb.europe-west1.firebasedatabase.app/'} )
        
    async def GetBannedUsers(self) -> json:
        print(f"getting banned users from db...")
        
        ref = db.reference("server/users/bannedusers")
        return await ref.get()
    
    async def SetBannedUsers(self, bannedUsers: json):
        ref = db.reference("server/users/bannedusers")
        ref.set(bannedUsers)
        






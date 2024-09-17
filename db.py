import firebase_admin
import json
import os
import dotenv
import discord
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
        
    def GetAllBannedUsers(self):
        print(f"getting banned users from db...")
        
        ref = db.reference("server/users/bannedusers")
        return ref.get()
    
    async def AddBannedUser(self, userid : str, username : str, unixendtime : int, reason : str):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{int(userid)}")
        
        child.set({"displayname": username,
            "endtime": unixendtime,
            "reason": reason,})
        
    async def RemoveBannedUser(self, userid : str):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{int(userid)}")
        child.delete()
        
    async def GetBannedUser(self, userid : str):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{int(userid)}")
        return child.get()
        
        






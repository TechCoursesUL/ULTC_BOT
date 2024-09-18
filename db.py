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
        self.app = firebase_admin.initialize_app( credential=firebase_admin.credentials.Certificate("creds.json"), options={'databaseURL' :'https://ultcdb-default-rtdb.europe-west1.firebasedatabase.app/'} )

        
    def GetAllBannedUsers(self):
        print("getting banned users from db...")

        ref = db.reference("server/users/bannedusers")
        return ref.get()
    
    async def AddBannedUser(self, userid : str, username : str, unixendtime : int, reason : str, staffmember: discord.Member):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{userid}")
        
        child.set({"displayName": username,
            "endTime": unixendtime,
            "reason": reason,
            "byStaffMember": staffmember.global_name})
        
    async def RemoveBannedUser(self, userid : str):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{userid}")
        
        
        child.delete()
        
    async def GetBannedUser(self, userid : str):
        ref = db.reference("server/users/bannedusers")
        child = ref.child(f"{userid}")
        return child.get()
        
        






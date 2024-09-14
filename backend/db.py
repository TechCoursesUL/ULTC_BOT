import firebase_admin
import json
from firebase_admin import db

class ULTCDB:
    def __init__(self) -> None:
        self.cred_obj = firebase_admin.credentials.Certificate("./DBAUTH.json")
        self.app = firebase_admin.initialize_app(self.cred_obj, {'databaseURL' :'https://ultcdb-default-rtdb.europe-west1.firebasedatabase.app/'})
        
    def GetBannedUsers(self) -> json:
        print(f"getting banned users from db...")
        
        ref = db.reference("server/users/bannedusers")
        return ref.get()
    
    def SetBannedUsers(self, bannedUsers: json) -> bool:
        ref = db.reference("server/users/bannedusers")
        
        ref.set(bannedUsers)

print(ULTCDB().GetBannedUsers())
userExample = json.dumps(
    {
        -1: #DiscordUserID
            10000000000000, #unix time which indicates when ban ends
        -2: 100000000005488,
        
    }
)




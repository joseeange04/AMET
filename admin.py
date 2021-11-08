import messenger
from conf import ACCESS_TOKEN
import requete

botAdmin= messenger.Messenger(ACCESS_TOKEN)
reqAdmin = requete.Requete()

class Admin:
    def __init__(self):
        pass

    def sendMessage(self,sender_id): 
        botAdmin.send_message(sender_id,"bonjour Angela")
        return True


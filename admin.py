import messenger
from conf import ACCESS_TOKEN
import requete

botAdmin= messenger.Messenger(ACCESS_TOKEN)
reqAdmin = requete.Requete()

class Admin:
    def __init__(self):
        pass

    def salutationAdmin(self,sender_id_admin):
        botAdmin.send_message(sender_id_admin,"Bonjour Admin,Ravi de vous voir 😊😊😊")
        botAdmin.send_quick_reply(sender_id_admin,"tachesAdmin")
        return True
    
    def traitementCmdAdmin(self,sender_id_admin,commande):
        if commande == "__create":
            botAdmin.send_message(sender_id_admin,"Create")

            return True
        elif commande == "__read":
            botAdmin.send_message(sender_id_admin,"Read")
            return True
        elif commande == "__update":
            botAdmin.send_message(sender_id_admin,"Update")
            return True
        elif commande == "__delete":
            botAdmin.send_message(sender_id_admin,"Delete")
            return True

    def executionAdmin(self,sender_id_admin,commade):
        
        #Mettre en vue d'abord notre cher(e) Admin
        botAdmin.send_action(sender_id_admin, 'mark_seen')

        print(commande)
        if self.traitementCmdAdmin(sender_id_admin,commade):
            return
        
        if self.salutationAdmin(sender_id_admin):
            return
        

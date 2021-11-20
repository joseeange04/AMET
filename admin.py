import messenger
from conf import ACCESS_TOKEN
from utils import download_file
import requete

botAdmin= messenger.Messenger(ACCESS_TOKEN)
reqAdmin = requete.Requete()

class Admin:
    def __init__(self):
        pass

    #---------------------------------------------OPTIONS----------------------------------------------------------------#
    def getProductModifier(self):
        """
            Afficher tout les produit existant dans la BDD
        """
        self.data = reqAdmin.get_product()
        produits = []
        i = 0
        while i < len(self.data):
            produits.append({
                "title":str(self.data[i][0]) + " - " + self.data[i][1],
                "image_url":"https://amet.iteam-s.xyz/" + self.data[i][4],
                "subtitle":"Prix : " + str(self.data[i][3]) + " Ar /heures",
                "buttons":[ 
                    {
                        "type":"postback",
                        "title":"MODIFIER",
                        "payload": "__MODIFIER" + " " + str(self.data[i][0])  
                    }, 
                ]           
            })
            i = i + 1
        return produits

    #--------------------------------------------FIN OPTIONS------------------------------------------------------------#


    def salutationAdmin(self,sender_id_admin):
        botAdmin.send_message(sender_id_admin,"Bonjour Admin,Ravi de vous acceuillir 😊😊😊")
        botAdmin.send_quick_reply(sender_id_admin,"tachesAdmin")
        return True
    
    def traitementPstPayloadAdmin(self,sender_id_admin,commande):
        self.payload = commande.split(" ")
        if self.payload[0]== "__MODIFIER":
            botAdmin.send_quick_reply(sender_id_admin,"proposeModifierAdmin")
            return True

    def traitementActionAdmin(self,sender_id_admin,commande,statut):
        if statut == "MODIFIER_NOM":
            botAdmin.send_message(sender_id_admin,"Tongasoa ato @nom")
            return True

        elif statut == "MODIFIER_DETAILS":
            botAdmin.send_message(sender_id_admin,"Tongasoa ato @details")
            return True

        elif statut == "MODIFIER_PRIX":
            botAdmin.send_message(sender_id_admin,"Tongasoa ato @prix")
            return True

        elif statut == "MODIFIER_COUVERTURE":
            botAdmin.send_message(sender_id_admin,"Tongasoa ato @couverture")
            return True

        #-------------------------INSERT NEW PRODUCT----------------------------#   
        # self.elementProductInsert = []
        elif statut == "ATTENTE_NOM":
            self.elementProductInsert.append(commande)
            botAdmin.send_message(sender_id_admin,"Details")
            reqAdmin.set_action(sender_id_admin,"ATTENTE_DETAILS")
            return True

        elif statut == "ATTENTE_DETAILS":
            botAdmin.send_message(sender_id_admin,"creer details")
            return True


    
    def traitementCmdAdmin(self,sender_id_admin,commande):
        #-----------Premier QuickReply-----------------------#
        if commande == "__create":
            botAdmin.send_message(sender_id_admin,"Create")
            botAdmin.send_message(sender_id_admin,"Entrer le nom du produit à créer")
            req.set_action(sender_id_admin,"ATTENTE_NOM")
            return True

        elif commande == "__read":
            botAdmin.send_message(sender_id_admin,"Listes de données")
            botAdmin.send_template(sender_id_admin,self.getProductModifier())
            return True

        elif commande == "__update":
            botAdmin.send_message(sender_id_admin,"Update")
            return True

        elif commande == "__delete":
            botAdmin.send_message(sender_id_admin,"Delete")
            return True
        #elif verif commande

        #--------------------second QuickReply--------------------#
        elif commande == "__NOM":
            botAdmin.send_message(sender_id_admin,"Entrer le nouveau nom:")
            reqAdmin.set_action(sender_id_admin,"MODIFIER_NOM")
            return True

        elif commande == "__DETAILS":
            botAdmin.send_message(sender_id_admin,"Entrer le nouveau details:")
            reqAdmin.set_action(sender_id_admin,"MODIFIER_DETAILS")
            return True
        
        elif commande == "__PRIX":
            botAdmin.send_message(sender_id_admin,"Entrer le nouveau Prix:")
            reqAdmin.set_action(sender_id_admin,"MODIFIER_PRIX")
            return True
        
        elif commande == "__COUVERTURE":
            botAdmin.send_message(sender_id_admin,"Entrer la nouvelle photo de couverture :")
            reqAdmin.set_action(sender_id_admin,"MODIFIER_COUVERTURE")
            return True

    # def getUrlInsertOrUpdate(self,sender_id_admin,url):
        

    def executionAdmin(self,sender_id_admin,commande):
        
        reqAdmin.verifAdmin(sender_id_admin)
        #Mettre en vue d'abord notre cher(e) Admin
        botAdmin.send_action(sender_id_admin, 'mark_seen')

        statut = reqAdmin.get_action(sender_id_admin)

        if self.traitementCmdAdmin(sender_id_admin,commande):
            return
        
        if self.traitementActionAdmin(sender_id_admin,commande,statut):
            return True

        if self.traitementPstPayloadAdmin(sender_id_admin,commande):
            return

        if self.salutationAdmin(sender_id_admin):
            return
        

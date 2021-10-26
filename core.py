import messenger
from conf import ACCESS_TOKEN
import requete

bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()

class Traitement: 
    def __init__(self):
        pass 
#---------------------------------------------OPTIONS--------------------------------------------------------------------#   
    def elements_produits(self):  
        '''
            Fonction qui fetch des données de chaques 
            produits dans la base de données
        '''
        self.photos = req.get_produits()
        produits = []
        i = 0
        while i < len(self.photos):
            produits.append({
                "title":str(self.photos[i][0]) + " - " + self.photos[i][1],
                "image_url":"https://amet.iteam-s.xyz/" + self.photos[i][3],
                "subtitle":"Prix : " + str(self.photos[i][2]) + " Ar /heures",
                "buttons":[ 
                    {
                        "type":"postback",
                        "title":"Voir Gallery",
                        "payload": "__GALERY" + " " + str(self.photos[i][0])  
                    },{
                        "type":"postback",
                        "title":"Details",
                        "payload":"__DETAILS" + " " + str(self.photos[i][0])
                    },
                    {
                        "type":"postback",
                        "title":"Disponibilité",
                        "payload":"__DISPONIBILITÉ"
                    }  
                ]           
            })
            i = i + 1

        return produits


    def gallery(self,id_prod):
        self.all_gallerry = req.get_gallerry(id_prod)

        listeGallery = []
        j = 0
        while j < len(self.all_gallerry):
            listeGallery.append({
                "title":"image 😊😊😊",
                "image_url":"https://amet.iteam-s.xyz/" + self.all_gallerry[j][0],
                "buttons":[ 
                    {
                        "type":"postback",
                        "title":"voir image",
                        "payload": "__voirimage" + " " +  "https://amet.iteam-s.xyz/" + self.all_gallerry[j][0]
                    } 
                ]           
            })
            j = j + 1

        return listeGallery
    
    def details(self,id_prod):
        self.photoDetails = req.get_detail(id_prod)
        urlDetails = "https://amet.iteam-s.xyz/" + self.photoDetails[0][0]
        return urlDetails   



#--------------------------------------------FIN OPTIONS------------------------------------------------------------------#

    def _analyse(self, data):           
        '''
            Fonction analysant les données reçu de Facebook
            Donnée de type Dictionnaire attendu (JSON parsé)
        '''
        for event in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # recuperation de l'id de l'utilisateur
                    sender_id = message['sender']['id']

                    if message['message'].get('quick_reply'):
                        # cas d'une reponse de type QUICK_REPLY
                        self.__execution(
                            sender_id,
                            message['message']['quick_reply'].get('payload')
                        )
                          
                    elif message['message'].get('text'):
                        # cas d'une reponse par text simple.
                        #envoi au traitement
                        self.__execution(
                            sender_id,
                            message['message'].get('text')
                        )
                        
                        information = "Bonjour, Nous sommes une petite entreprise qui fait une location des terrains scientitiques ici Antananarivo"
                        bot.send_message(sender_id,information)
                        bot.send_quick_reply(sender_id) 

                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    pst_payload = message['postback']['payload']
                    # envoie au traitement
                    self.__execution(recipient_id, pst_payload) 

    def traitement_cmd(self,sender_id,commande):
        """
            Methode qui permet d'envoyer les options 
            aux utilisateurs afin qu'ils puissent continuer
            ses actions 

        """

        if commande == "__louer_terrain": 
            produitDispo = "Voici donc les differents terrains disponibles"
            bot.send_message(sender_id,produitDispo)
            bot.send_template(sender_id,self.elements_produits())

        elif commande == "__information":
            pageInfo = "Les informations concernants notre page arrivent bientôt ici"
            bot.send_message(sender_id,pageInfo) 

    def traitement_pstPayload(self,sender_id,pst_payload):
        listeElementPayload = pst_payload.split()

        #----------------------PREMIER TEMPLATE GENERIC AVEC TROIS PALYLOAD------------------------------------#

        if listeElementPayload[0] == "__GALERY":
            données = self.gallery(int(listeElementPayload[1]))
            bot.send_template(sender_id,données)
        elif listeElementPayload[0] == "__DETAILS":
            url = self.details(int(listeElementPayload[1]))
            bot.send_file_url(sender_id,url,"image")

        #----------------------DEUXIEME TEMPLATE GENERIC AVEC TROIS PALYLOAD------------------------------------#

        elif listeElementPayload[0] == "__voirimage":
            bot.send_file_url(sender_id,listeElementPayload[1],"image")


    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu   
        """
        #Mettre en vue les messages reçus
        bot.send_action(user_id, 'mark_seen')

        # #traiter les commandes obtenus
        if self.traitement_cmd(user_id,commande):
            return

        if self.traitement_pstPayload(user_id,commande):
            return
    

        




    
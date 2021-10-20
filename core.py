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
                        "payload":"__GALlERY"
                    },{
                        "type":"postback",
                        "title":"Details",
                        "payload":"__DETAILS"
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
            

   


#--------------------------------------------FIN OPTIONS------------------------------------------------------------------#

    def _analyse(self, data):           
        '''
            Fonction analysant les données reçu de Facebook
            Donnée de type Dictionnaire attendu (JSON parsé)
        '''
        # print(data)
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
                        
                        information = "Bonjour, Nous sommes une petite entreprise qui fait une location des"
                        information2 = "terrains scientitiques ici Antananarivo"
                        info = information + " " + information2
                        bot.send_message(sender_id,info)
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

    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu   
        """
        #Mettre en vue les messages reçus
        bot.send_action(user_id, 'mark_seen')

        #traiter les commandes obtenus
        self.traitement_cmd(user_id,commande)

    

        




    
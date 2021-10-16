import messenger
from conf import ACCESS_TOKEN
import requete

bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()

class Traitement: 
    def __init__(self):
        pass 
   
    def elements_produits(self):  
        '''
            Fonction qui fetch des données de chaques 
            produits dans la base de données
        '''
        self.photos = req.get_produits()
        
        elements =[
                    {
                    "title":list(self.photos[0])[0],
                    "image_url":list(self.photos[0])[2],
                    "subtitle":str(list(self.photos[0])[1]) + "Ar",
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://www.iteam-s.mg",
                            "title":"View Website"
                        },
                        {
                            "type":"postback",
                            "title":"commander",
                            "payload":"__commande"
                        }  
                    ]      
                }
            ] 

        return elements

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

                        reponse_quick_reply = message['message']['quick_reply'].get('payload')
                        if reponse_quick_reply == "__louer_terrain": 
                            produitDispo = "Voici donc les differents terrains disponibles"
                            bot.send_message(sender_id,produitDispo)
                            bot.send_template(sender_id)
                            
                        elif reponse_quick_reply == "__information":
                            pageInfo = "Les informations concernants notre page arrivent bientôt ici"
                            bot.send_message(sender_id,pageInfo)
                            

                    elif message['message'].get('text'):
                        # cas d'une reponse par text simple.
                        self.__execution(
                            sender_id,
                            message['message'].get('text')
                        )
                        
                        information = "Bonjour, Nous sommes une petite entreprise qui fait une location des"
                        information2 = "terrains scientitiques ici Antananarivo"
                        info = information + " " + information2
                        bot.send_message(sender_id,info)
                        bot.send_quick_reply(sender_id) 


    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu   
        """
        #Mettre en vue les messages reçus
        bot.send_action(user_id, 'mark_seen')

    

        




    
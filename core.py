import messenger
from conf import ACCESS_TOKEN

bot = messenger.Messenger(ACCESS_TOKEN)


class Traitement: 
    def __init__(self):
        pass 


    def message(self,text):
        a = text.lower()
        if a == "salut":
            b = "Hello word!"
        else:
            b = "BOt message"
        return b
    
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
                        self.__execution(
                            sender_id,
                            message['message'].get('text')
                        )
                        
                        texte = message['message'].get('text')
                        print(texte)
                        reponse = self.message(texte)   
                        print(reponse)
                        bot.send_message(sender_id,reponse)
                        
        


    def __execution(self, user_id, commande):
        '''
            Fonction privée qui traite les differentes commandes réçu
        '''
        # Mettre en VUE le message qui est en cours de traitement
        bot.send_action(user_id, 'mark_seen')

        # # recuperer l'action de l'utilisateur.
        # statut = req.get_action(user_id)

        # # recuperation des infos de l'utilisateur
        # user_info = req.get_user_info(user_id)

        '''
            Pour ces différents traitement, si un condition est
            remplit, ne plus continuer les autres.
            les differentes fonction retourne 'True' si un
            option a été traité d'où l'arret des autres trts.
        '''
        # # traitement par action courrant
        # if self.trt_statut(statut, user_id, user_info, commande):
        #     return

        # # traitement par commande
        # if self.trt_commande(commande, user_id, user_info):
        #     return

        # # autre traitement
        # if self.trt_divers(user_id, user_info):
        #     return

        # # Pour plus de securité si aucun option sa été selectionner
        # # on nettoye les valeurs de temp et action
        # req.set_action(user_id, None)
        # req.set_temp(user_id, None)

        # # Envoie du choix de l'options Menu
        # bot.send_quick_reply(user_id, user_info['lang'], SHOW_MENU=True)



    
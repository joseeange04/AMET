import messenger
from conf import ACCESS_TOKEN
from datetime import date , datetime
import requete
import admin

admin = admin.Admin()
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
                        "payload":"__DISPONIBILITÉ" + " " + str(self.photos[i][0])
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



#--------------------------------------------FIN OPTIONS----------------------------------------------------------------#


#-------------------------------------ANALYSES DES MESSAGES POSTÉS PAR LES UTILISATEURS--------------------------------#
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

                    if sender_id == "4435320363255529" :
                        admin.sendMessage(sender_id)
                        return True
                    else:
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
      
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    pst_payload = message['postback']['payload']
                    # envoie au traitement
                    self.__execution(recipient_id, pst_payload) 
    
    #-------------------------------FIN ANALYSES DES MESSAGES POSTÉS PAR LES UTILISATEURS--------------------------------#


    #--------------------------------------LES TRAITEMENTS---------------------------------------------------------------#
    def salutation(self,sender_id):
        information = "Bonjour, Nous sommes une petite entreprise qui fait une location des terrains scientitiques ici Antananarivo"
        bot.send_message(sender_id,information)
        bot.send_quick_reply(sender_id,"proposerAction")
        return True
   
    def traitement_action(self,sender_id,commande,action):
        if action[0] == "DATE":
            req.set_action(sender_id,None)
            self.daty = commande 
            verifTypeDate = self.daty.split("-")
            dateNow = str(date.today().strftime("%d-%m-%Y")).split("-")
            
            #Conditions qui verifient les types de la date entrée par l'utilisateur
            if (not verifTypeDate[0].isdigit() or (int(verifTypeDate[0]) not in range(0,32))) \
            or (not verifTypeDate[1].isdigit() or (int(verifTypeDate[1]) not in range(1,13))) \
            or (not verifTypeDate[2].isdigit() or (int(verifTypeDate[2]) not in range(2021,2023))):
                bot.send_message(sender_id,"Votre date est invalide\n\nVeuillez saisir à nouveau et suivez le bon format😊😊😊:")
                req.set_action(sender_id,"DATE")
                return True

            elif (int(verifTypeDate[0])<int(dateNow[0]) and (int(verifTypeDate[1])==int(dateNow[1])) and (int(verifTypeDate[2])==int(dateNow[2]))) \
            or ((int(verifTypeDate[1])<int(dateNow[1])) and (int(verifTypeDate[2])==int(dateNow[2]))):
                bot.send_message(sender_id,"Votre date est invalide\n\nPeut être cette date est déjà passée\n\n"
                +"Alors veuillez-vous saisir à nouveau et faire le bon choix pour la future date et pourqoui pas maintenant?"
                +"😊😊😊")
                req.set_action(sender_id,"DATE")
                return True

            else:
                _dateAlaTerrain = datetime.strptime(self.daty, "%d-%m-%Y")
                __dateAlaTerrain = _dateAlaTerrain.strftime("%Y-%m-%d")
                exist = req.date_dispo(__dateAlaTerrain,self.listeElementPayload[1])
                if exist:
                    heureDejaReserve = req.heureReserve(__dateAlaTerrain,self.listeElementPayload[1])
                    k=0
                    self.listeHeureDebut = []
                    self.listeHeureFin = []
                    while k<len(heureDejaReserve):
                        self.listeHeureDebut.append(str(heureDejaReserve[k][0]))
                        self.listeHeureFin.append(str(heureDejaReserve[k][1]))
                        k = k + 1
                    
                    self.listeHeureDebutTraiter = []
                    self.listeHeureFinTraiter = []
                    x  = 0
                    y = 0
                    while x<len(self.listeHeureDebut):
                        self.listeHeureDebutTraiter.append(
                            str(self.listeHeureDebut[x]).split(":")[0] + "h" + str(self.listeHeureDebut[x]).split(":")[1]
                        )
                        x = x + 1

                    while y<len(self.listeHeureFin):
                        self.listeHeureFinTraiter.append(
                            str(self.listeHeureFin[y]).split(":")[0] + "h" + str(self.listeHeureFin[y]).split(":")[1]
                        )
                        y = y + 1

                    w = 0
                    listeMessage = []
                    while w<len(self.listeHeureDebutTraiter):
                        message = self.listeHeureDebutTraiter[w]+" à "+self.listeHeureFinTraiter[w]
                        w = w + 1
                        listeMessage.append(message)

                    bot.send_message(sender_id,"Pour cette Date; les heures déjà resérvés sont:\n\n"
                    +"\n".join(listeMessage)+"\n\nDonc vous pouvez choisir vos heures à part cela")
                    bot.send_quick_reply(sender_id,"proposerCmd")
                    req.set_action(sender_id,None)
                    return True
                    
                else:
                    bot.send_message(sender_id,
                    "Pour cette date, il n'y a pas encore des reservations,"
                    +"donc vous êtes libre de choisir vos heures entre 6h00 à 20h00"
                    )
                    bot.send_message(sender_id,"Saisir alors votre heure de debut en format HHhMM\n"+
                    "Exemple: 12h00")
                    req.set_action(sender_id,"HEURE_DEBUT")
                    return True

        elif action[0] == "HEURE_DEBUT":
            self.heure_debut = commande
            self.verifHeureDeDebut = self.heure_debut.split("h")

            if(not self.verifHeureDeDebut[0].isdigit() or int(self.verifHeureDeDebut[0])<6 or int(self.verifHeureDeDebut[0])>20) \
                or (not self.verifHeureDeDebut[1].isdigit() or int(self.verifHeureDeDebut[1])>59):
                bot.send_message(sender_id,
                "Votre heure est invalide\nVeuillez saisir à nouveau et suivez le bon format\nMerci😊😊😊"
                )
                return True
            else:

                if (int(self.verifHeureDeDebut[1]) == 0) or (int(self.verifHeureDeDebut[1]) == 30):
                    a=0
                    b=0
                    self.verifIntervalleDebut = []
                    self.verifIntervalleFin = []
                    print(self.verifIntervalleDebut)
                    while a<len(self.listeHeureDebutTraiter):
                        self.verifIntervalleDebut.append(self.listeHeureDebutTraiter[a].split("h")[0])
                        a = a + 1

                    while b<len(self.listeHeureFinTraiter):
                        self.verifIntervalleFin.append(self.listeHeureFinTraiter[b].split("h")[0])
                        b = b + 1

                    c=0
                    while c<len(self.verifIntervalleDebut):
                        if int(self.verifIntervalleDebut[c])<=int(self.verifHeureDeDebut[0])<int(self.verifIntervalleFin[c]):
                            bot.send_message(sender_id," Votre heure de DEBUT est tombé dans l'intervalle de temps des heures déjà"
                            +"réservés\n\nDonc, Veuillez-vous saisir à nouveau et bien verifier votre heure\n\n"
                            +"Merci 😊😊😊")
                            return True
                        elif int(self.verifHeureDeDebut[0])==int(self.verifIntervalleFin[c]):
                            if int(self.verifHeureDeDebut[1])>=int(self.listeHeureFinTraiter[c].split("h")[1]):
                                bot.send_message(sender_id,"Saisir votre heure de fin en format HHhMM\n"+
                                "Exemple 12h00")
                                req.set_action(sender_id,"HEURE_FIN")
                                return True
                            else:
                                bot.send_message(sender_id," Votre heure de DEBUT est tombé dans l'intervalle de temps des heures déjà"
                                +"réservés\n\nDonc, Veuillez-vous saisir à nouveau et bien verifier votre heure\n\n"
                                +"Merci 😊😊😊")
                                return True
                        else:
                            pass 
                        c = c + 1

                    print(self.verifIntervalleDebut)
                    bot.send_message(sender_id,"Saisir votre Heure de fin en format HHhMM\n"+
                    "Exemple 12h00")
                    req.set_action(sender_id,"HEURE_FIN")
                    return True
                
                else:
                    print(int(self.verifHeureDeDebut[1]))
                    bot.send_message(sender_id,"Votre Heure de DEBUT est invalide car il ne respecte pas le marge de"
                    +"la tranche\n\nVeuillez saisir à nouveau en respectant la marge de trance\n\nMerci😊😊😊")
                    return True

        elif action[0] == "HEURE_FIN":
            self.heure_fin = commande
            self.verifHeureDeFin = self.heure_fin.split("h")

            if(not self.verifHeureDeFin[0].isdigit() or int(self.verifHeureDeFin[0])<6 or int(self.verifHeureDeFin[0])>19) \
                or (not self.verifHeureDeFin[1].isdigit() or int(self.verifHeureDeFin[1])>59):
                bot.send_message(sender_id,
                "Votre heure est invalide\nVeuillez saisir à nouveau et suivez le bon format\nMerci😊😊😊"
                )
                return True

            else:

                if int(self.verifHeureDeFin[1]) == 0 or int(self.verifHeureDeFin[1]) == 30:
                    d=0
                    while d<len(self.verifIntervalleDebut):
                        if int(self.verifIntervalleDebut[d])<=int(self.verifHeureDeFin[0])<int(self.verifIntervalleFin[d]):
                            bot.send_message(sender_id," Votre heure de FIN est tombé dans l'intervalle de temps des heures déjà"
                            +"réservés\n\nDonc, Veuillez-vous saisir à nouveau et bien verifier votre heure\n\n"
                            +"Merci 😊😊😊")
                            return True
                        elif int(self.verifHeureDeFin[0])==int(self.verifIntervalleDebut[d]):
                            if int(self.verifHeureDeFin[1])<=int(self.listeHeureDebutTraiter[d].split("h")[1]):
                                if self.verifHeureDeFin[0]<=self.verifHeureDeDebut[0]:
                                    bot.send_message(sender_id,"Votre heure de Fin est ivalide car selon la marge du commande"
                                    +", il est forcement plus d'une heure le commande\n\n"+
                                    "Alors veuillez-vous saisir à nouveau en respectant cette marge\n\nMerci😊😊😊")
                                    return True
                                else:   
                                    bot.send_message(sender_id,"bien recu")
                                    req.set_action(sender_id,None)
                                    return True
                        else:
                            pass 
                        d = d + 1

                    if self.verifHeureDeFin[0]<=self.verifHeureDeDebut[0]:
                        bot.send_message(sender_id,"Votre heure de Fin est ivalide car selon la marge du commande"
                        +", il est forcement plus de une heure le commande\n\n"+
                        "Alors veuillez-vous saisir à nouveau en respectant cette marge\n\nMerci😊😊😊")
                        return True
                    else:

                        self.listeHeureDebutEtFin = self.verifIntervalleDebut + self.verifIntervalleFin
                        print(self.listeHeureDebutEtFin)
                        for e in range(int(self.verifHeureDeDebut[0]),int(self.verifHeureDeFin[0])+1):
                            for f in range (len(self.listeHeureDebutEtFin)):
                                if e == int(self.listeHeureDebutEtFin[f]):
                                    print(int(self.listeHeureDebutEtFin[f]))
                                    print(e)
                                    bot.send_message(sender_id,"Erreur:Votre heure de FIN est tombé dans l'intervalle de temps des heures déjà"
                                    +"réservés\n\nDonc, Veuillez-vous saisir à nouveau et bien verifier votre heure\n\n"
                                    +"Merci 😊😊😊")
                                    req.set_action(sender_id,"HEURE_FIN")
                                    return True
                                else:
                                    pass
                        
                        bot.send_message(sender_id,"bien recu")
                        req.set_action(sender_id,None)
                        return True

                else:
                    bot.send_message(sender_id,"Votre Heure de FIN est invalide car il ne respecte pas le marge de"
                    +"la tranche\n\nVeuillez saisir à nouveau en respectant la marge de trance\n\nMerci😊😊😊")
                    return True

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
            req.set_action(sender_id,None)
            return True

        elif commande == "__information":
            pageInfo = "Les informations concernants notre page arrivent bientôt ici"
            bot.send_message(sender_id,pageInfo) 
            req.set_action(sender_id,None)
            return True

        elif commande == "__cmdDateActu":
            bot.send_message(sender_id,"Saisir alors votre heure de Debut en format HHhMM\n"+
            "Exemple: 12h00")
            req.set_action(sender_id,"HEURE_DEBUT")
            return True

        elif commande == "__cmdAutreDate":
            bot.send_message(sender_id,"Entrer alors la date en respctant toujours le bon format😊😊😊")
            req.set_action(sender_id,"DATE")
            return True

        elif commande == "__curieux":
            bot.send_message(sender_id,"Merci beaucoup pour votre curiosité et la visite de notre page😊😊😊\n\n"
            +"Vous pouvez encore  faire un commade maintenant même ou à une autre jour si vous voulez en envoyant"
            +" encore de message 😉😉😉\n\nSinon A Bientôt ✋✋✋✋✋✋✋")
            req.set_action(sender_id,None)
            return True



    def traitement_pstPayload(self,sender_id,pst_payload):
        self.listeElementPayload = pst_payload.split()

        #PREMIER TEMPLATE GENERIC AVEC TROIS PALYLOAD
        if self.listeElementPayload[0] == "__GALERY":
            données = self.gallery(int(self.listeElementPayload[1]))
            bot.send_template(sender_id,données)
            req.set_action(sender_id,None)
            return True

        elif self.listeElementPayload[0] == "__DETAILS":
            url = self.details(int(self.listeElementPayload[1]))
            bot.send_file_url(sender_id,url,"image")
            req.set_action(sender_id,None)
            return True

        elif self.listeElementPayload[0] == "__DISPONIBILITÉ":
            bot.send_message(sender_id,
            " De quelle date?\n\nSaisir la date sous forme JJ-MM-AAAA\n\nExemple: " + str(date.today().strftime("%d-%m-%Y")))  
            req.set_action(sender_id,"DATE")
            return True

        #DEUXIEME TEMPLATE GENERIC AVEC TROIS PALYLOAD
        elif self.listeElementPayload[0] == "__voirimage":
            bot.send_file_url(sender_id,self.listeElementPayload[1],"image")
            return True




    #-------------------------------------LE COEUR DES TRAITEMENTS---------------------------------------------#

    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu   
        """
        # Verification du sender dans la base
        # Insertion si non présent
        req.verif_utilisateur(user_id)
        
        #Mettre en vue les messages reçus
        bot.send_action(user_id, 'mark_seen')

        # recuperer l'action de l'utilisateur.
        statut = req.get_action(user_id)

        # traitement par action courrant
        if self.traitement_action(user_id,commande,statut):
            return
        # #traiter les commandes obtenus
        if self.traitement_cmd(user_id,commande):
            return

        if self.traitement_pstPayload(user_id,commande):
            return 

        if self.salutation(user_id):
            return 
    
        
        




    
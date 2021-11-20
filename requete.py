import mysql.connector
from conf import DATABASE


class Requete:
    def __init__(self):
        '''
            Initialisation: Connexion à la base de données
        '''
        self.__connect()

    def __connect(self):
        self.db = mysql.connector.connect(**DATABASE)
        self.cursor = self.db.cursor()


    def verif_db(fonction):
        '''
            Un decorateur de verification de la
            connexion au serveur avant traitement.
        '''
        def trt_verif(*arg, **kwarg):
            if not arg[0].db.is_connected():
                # reconnexion de la base
                try:
                    arg[0].db.reconnect()
                except Exception:
                    arg[0].__connect()
            return fonction(*arg, **kwarg)
        return trt_verif

    @verif_db
    def get_produits(self):
        req = """ 
                SELECT id_prod, nom_prod, prix,
                photo_couverture FROM produits
                
              """
        self.cursor.execute(req)
        return self.cursor.fetchall()

    @verif_db
    def get_gallerry(self,id_prod):
        req = """ 
                SELECT contenu FROM galeries 
                WHERE id_prod = %s

              """
        self.cursor.execute(req,(id_prod,))
        return self.cursor.fetchall()

    @verif_db
    def get_detail(self,id_prod):
        req = """
                SELECT details FROM produits
                WHERE id_prod = %s     

              """
        self.cursor.execute(req,(id_prod,))
        return self.cursor.fetchall()

    @verif_db
    def verif_utilisateur(self, user_id):
        '''
            Fonction d'insertion du nouveau utilisateur
            et mise à jour de la date de dernière utilisation.
        '''
        # Insertion dans la base si non present
        req = 'INSERT IGNORE INTO utilisateur(fb_id,date_mp)  VALUES (%s,NOW())'
        self.cursor.execute(req, (user_id,))
        # Mise à jour de la date de dernière utilisation
        req = 'UPDATE utilisateur SET date_mp=NOW() WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        self.db.commit()

    @verif_db
    def get_action(self, user_id):
        '''
            Recuperer l'action de l'utilisateur
        '''
        req = 'SELECT action FROM utilisateur WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        # retourne le resultat
        return self.cursor.fetchall() 

    @verif_db
    def set_action(self, user_id,action):
        '''
            Definir l'action de l'utilisateur
        '''
        req = 'UPDATE utilisateur SET action = %s WHERE fb_id = %s'
        self.cursor.execute(req, (action,user_id))
        self.db.commit()

    @verif_db
    def date_dispo(self,daty,id_prod):
        """
            Method qui verifie la date de disponibilité
            est-ce existe ou pas? la date entrée par 
            l'utilisateur.
        """
        req = 'SELECT  dateAlaTerrain FROM commande WHERE dateAlaTerrain=%s AND id_prod=%s'
        self.cursor.execute(req,(daty,id_prod))
        return self.cursor.fetchall()

    @verif_db
    def heureReserve(self,daty,id_prod):
        req = """
                SELECT heureDebutCmd,heureFinCmd 
                FROM commande 
                WHERE dateAlaTerrain=%s AND id_prod=%s AND statut="CONFIRMÉ"

            """
        self.cursor.execute(req,(daty,id_prod))
        return self.cursor.fetchall()

    @verif_db
    def getIdUser(self,sender_id):
        req='SELECT id from utilisateur WHERE fb_id=%s'
        self.cursor.execute(req,(sender_id,))
        return self.cursor.fetchone()[0]

    @verif_db
    def insertNouveauCommande(self,idUser,dateAlaTerrain,heureDeDebut,heureDeFin,id_prod,dataQrCode):
        req = """
               INSERT IGNORE INTO commande(id,date_cmd,dateAlaTerrain,heureDebutCmd,HeureFinCmd,id_prod,dataQrCode)
               VALUES(%s,NOW(),%s,%s,%s,%s,%s) 
            """
        self.cursor.execute(req,(idUser,dateAlaTerrain,heureDeDebut,heureDeFin,id_prod,dataQrCode))
        self.db.commit()

    @verif_db
    def setStatut(self,UniqueTime,value):
        req = """
                UPDATE commande SET statut = 'CONFIRMÉ' 
                WHERE  dataQrCode= %s   
        
            """
        self.cursor.execute(req,(UniqueTime,))
        self.db.commit()

    @verif_db
    def getElementQrcode(self,UniqueTime):
        req = """
                SELECT id_cmd,dataQrCode FROM commande
                WHERE  dataQrCode=%s AND statut = 'CONFIRMÉ'
            """
        self.cursor.execute(req,(UniqueTime,))
        return self.cursor.fetchall()



    """
        ------------------*----------Requête admin-------------*---------------
        1.  Methode pour afficher les produits dans la base
    """
    @verif_db
    def get_product(self):
        reqAdmin = "SELECT id_prod, nom_prod, details, prix, photo_couverture FROM produits"
        self.cursor.execute(reqAdmin)
        return self.cursor.fetchall()

    """
        2.  Methode d'ajout de produit
    """
    @verif_db
    def create_product(self, name, details, prix, photo_couverture):
        try:
            reqAdmin = """
                                 INSERT INTO produits(name, details, prix, phot_couverture) VALUES (%s, %s, %s, %s)
                                """
            self.cursor.execute(reqAdmin, (nom_produit, details_produit, prix, couverture))
            self.db.commit()
        except Exception as e:
            return False
        return True

    @verif_db
    def verifAdmin(self, sender_id_admin):
        '''
            Fonction d'insertion du nouveau utilisateur
            et mise à jour de la date de dernière utilisation.
        '''
        # Insertion dans la base si non present
        req = 'INSERT IGNORE INTO utilisateur(fb_id,date_mp,type_user)  VALUES (%s,NOW(),"ADMIN")'
        self.cursor.execute(req, (sender_id_admin,))
        # Mise à jour de la date de dernière utilisation
        req = 'UPDATE utilisateur SET date_mp=NOW() WHERE fb_id = %s'
        self.cursor.execute(req, (sender_id_admin,))
        self.db.commit()
    
    
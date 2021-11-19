import mysql.connector
from conf import DATABASE


class Requete:
    def __init__(self):
        '''
            Initialisation: Connexion à la base de données
        '''
        self.db = mysql.connector.connect(**DATABASE)
        self.cursor = self.db.cursor()
        # self.__init_db()

    def verif_db(fonction):
        '''
            Un decorateur de verification de la
            connexion au serveur avant traitement.
        '''
        def trt_verif(*arg, **kwarg):
            if not arg[0].db.is_connected():
                # reconnexion de la base
                arg[0].db.reconnect()
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
        return self.cursor.fetchall()[0]

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
    def insertNouveauCommande(self,sender_id,dateAlaTerrain,heureDeDebut,heureDeFin,id_prod,dataQrCode):
        req = """
               INSERT INTO (id,date_cmd,dateAlaTerrain,heureDebutCmd,HeureFinCmd,id_prod,dataQrCode)
               VALUES(%s,NOW(),%s,%s,%s,%s,%s) 
            """
        self.cursor.execute(req,(sender_id,dateAlaTerrain,heureDeDebut,heureDeFin,id_prod,dataQrCode))
        self.db.commit()

    @verif_db
    def getElementQrcode(self,sender_id):
        req = """
                SELECT id_cmd,dataQrCode FROM commande
                WHERE sender id = %s AND status = "CONFIRMÉ"
            """
        self.cursor.execute(req,(sender_id,))
        return self.cursor.fetchall()



    """
        ------------------*----------Requête admin-------------*---------------
        1.  Methode pour afficher les produits dans la base
    """
    @verif_db
    def get_product(self):
        reqAdmin = " SELECT id_prod, nom_prod, details, prix, photo_couverture FROM produits LIMIT 5"
        self.cursor.execute(reqAdmin)
        return self.cursor.fetchall()

    """
        2.  Methode d'ajout de produit
    """
    def create_product(self, name, details, prix, photo_couverture):
        try:
            self.cursor.execute(
                '''
                INSERT INTO produits(name, details, prix, phot_couverture) VALUES ({}, {}, {})
                '''.format(name, details, prix, photo_couverture)
            )
            self.db.commit()
        except Exception as e:
            return False
        return True


    
    
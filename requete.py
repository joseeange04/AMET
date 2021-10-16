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
        req = ' SELECT nom_prod, prix, photo_couverture FROM produits'
        self.cursor.execute(req)
        return self.cursor.fetchall()

    

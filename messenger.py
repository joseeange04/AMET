
import requests
from utils import translate
from erreur import TestUserRequests


class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    def send_message(self, dest_id, message):
        self.send_action(dest_id, 'typing_on')
        """
            Cette fonction sert à envoyer une message texte
            à un utilisateur donnée
        """
        data_json = {
            'recipient': {
                "id": dest_id
            },
            'message': {
                "text": message
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        self.send_action(dest_id, 'typing_off')
        return res

    def send_action(self, dest_id, action):
        """
            Cette fonction sert à simuler un action sur les messages.
            exemple: vue, en train d'ecrire.
            Action dispo: ['mark_seen', 'typing_on', 'typing_off']
        """

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },
            'sender_action': action
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )

    def send_quick_reply(self, dest_id,types):
        '''
            Envoie des quick reply messenger
        '''
        if types == "proposerAction":

            text = "Qu'est-ce que vous voulez faire ensuite donc?"
            quick_rep = [
                    {
                        "content_type": "text",
                        "title": "  Louer du terrain",
                        "payload": "__louer_terrain",
                        "image_url":
                            "https://cdn.icon-icons.com/icons2/343/PNG/512/Football-pitch_35793.png"
                    },
                    {
                        "content_type": "text",
                        "title": "Plus d'information",
                        "payload": "__information",
                        "image_url":
                            "https://png.pngtree.com/png-clipart/20190903/original/pngtree-personal-information-icon-png-image_4436300.jpg"
                    }
                ]

            data_json = {
                'messaging_type': "RESPONSE",
                'recipient': {
                    "id": dest_id
                },

                'message': {
                    'text': text,
                    'quick_replies': quick_rep
                }
            }

            header = {'content-type': 'application/json; charset=utf-8'}
            params = {"access_token": self.token}

            return requests.post(
                self.url + '/messages',
                json=data_json,
                headers=header,
                params=params
            )

        elif types == "proposerCmd":
            text = "Alors, Vous voulez quoi maintenant?\n\nCmd: commande"
            quick_rep = [
                    {
                        "content_type": "text",
                        "title": "Cmd de cette date 😍😍",
                        "payload": "__cmdDateActu",
                        "image_url":"http://assets.stickpng.com/images/58afdad6829958a978a4a693.png"
                    },
                    {
                        "content_type": "text",
                        "title": "Cmd à autre date 🥰🥰",
                        "payload": "__cmdAutreDate",
                        "image_url":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"

                    },
                    {
                        "content_type": "text",
                        "title": "Juste curieux 😇😇🙂🙃",
                        "payload": "__curieux",
                        "image_url":"https://png.pngitem.com/pimgs/s/63-631808_png-light-effects-for-picsart-glow-yellow-transparent.png"
                    }
                ]

            data_json = {
                'messaging_type': "RESPONSE",
                'recipient': {
                    "id": dest_id
                },

                'message': {
                    'text': text,
                    'quick_replies': quick_rep
                }
            }

            header = {'content-type': 'application/json; charset=utf-8'}
            params = {"access_token": self.token}

            return requests.post(
                self.url + '/messages',
                json=data_json,
                headers=header,
                params=params
            )

        elif types == "tachesAdmin":
            text = "Que souhaitez-vous faire maintenant Admin?"
            quick_rep = [
                    {
                        "content_type": "text",
                        "title": "Create😍😍",
                        "payload": "__create",
                        "image_url":"http://assets.stickpntachesAdming.com/images/58afdad6829958a978a4a693.png"
                    },
                    {
                        "content_type": "text",
                        "title": "Read 🥰🥰",
                        "payload": "__read",
                        "image_url":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"

                    },
                    {
                        "content_type": "text",
                        "title": "Update😇😇",
                        "payload": "__update",
                        "image_url":"https://png.pngitem.com/pimgs/s/63-631808_png-light-effects-for-picsart-glow-yellow-transparent.png"
                    },
                    {
                        "content_type": "text",
                        "title": "Delete 🙃🙃",
                        "payload": "__delete",
                        "image_url":"https://png.pngitem.com/pimgs/s/63-631808_png-light-effects-for-picsart-glow-yellow-transparent.png"
                    }
                ]

            data_json = {
                'messaging_type': "RESPONSE",
                'recipient': {
                    "id": dest_id
                },

                'message': {
                    'text': text,
                    'quick_replies': quick_rep
                }
            }

            header = {'content-type': 'application/json; charset=utf-8'}
            params = {"access_token": self.token}

            return requests.post(
                self.url + '/messages',
                json=data_json,
                headers=header,
                params=params
            )

        elif types == "confirmCmd":
            text = "Maintenant; Veuillez-vous confirmer vraiment votre commande?"
            quick_rep = [
                    {
                        "content_type": "text",
                        "title": "OUI",
                        "payload": "__oui",
                        "image_url":
                            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2W5PPm3Um8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                    },
                    {
                        "content_type": "text",
                        "title": "Non",
                        "payload": "__non",
                        "image_url":
                            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                            +"xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
                    }
                ]

            data_json = {
                'messaging_type': "RESPONSE",
                'recipient': {
                    "id": dest_id
                },

                'message': {
                    'text': text,
                    'quick_replies': quick_rep
                }
            }

            header = {'content-type': 'application/json; charset=utf-8'}
            params = {"access_token": self.token}

            return requests.post(
                self.url + '/messages',
                json=data_json,
                headers=header,
                params=params
            )
        
        elif types == "proposeModifierAdmin":

            text = "Que souhaitez-vous modifier Admin?"
            quick_rep = [
                    {
                        "content_type": "text",
                        "title": "NOM😍😍",
                        "payload": "__NOM",
                        "image_url":"http://assets.stickpntachesAdming.com/images/58afdad6829958a978a4a693.png"
                    },
                    {
                        "content_type": "text",
                        "title": "DETAILS 🥰🥰",
                        "payload": "__DETAILS",
                        "image_url":"https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"

                    },
                    {
                        "content_type": "text",
                        "title": "PRIX😇😇",
                        "payload": "__PRIX",
                        "image_url":"https://png.pngitem.com/pimgs/s/63-631808_png-light-effects-for-picsart-glow-yellow-transparent.png"
                    },
                    {
                        "content_type": "text",
                        "title": "COUVERTURE 🙃🙃",
                        "payload": "__COUVERTURE",
                        "image_url":"https://png.pngitem.com/pimgs/s/63-631808_png-light-effects-for-picsart-glow-yellow-transparent.png"
                    }
                ]

            data_json = {
                'messaging_type': "RESPONSE",
                'recipient': {
                    "id": dest_id
                },

                'message': {
                    'text': text,
                    'quick_replies': quick_rep
                }
            }

            header = {'content-type': 'application/json; charset=utf-8'}
            params = {"access_token": self.token}

            return requests.post(
                self.url + '/messages',
                json=data_json,
                headers=header,
                params=params
            )


    def send_template(self, destId, elements):
        '''
            Envoi des produits sous forme templates

        '''
        self.send_action(destId, 'typing_on')
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements , 
                    },
                },
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        self.send_action(destId, 'typing_off')
        
        return requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )

    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                'attachment': {
                    'type': filetype,
                    'payload': {
                        "url": url,
                        "is_reusable": True
                    }
                }
            }
        }
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        return requests.post(
            self.url + '/messages',
            json=dataJSON,
            headers=header,
            params=params
        )
            
    
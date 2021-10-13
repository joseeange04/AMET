import requests
from utils import translate
from erreur import TestUserRequests


class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    def send_message(self, dest_id, message, prio=False):
        # """ Fonction reserver pour les autres destinataires(Admin et Partenaires)"""
        # if dest_id == 'test_user':
        #     return TestUserRequests()
        # self.send_action(dest_id, 'typing_on')
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

        if prio:
            data_json["messaging_type"] = "MESSAGE_TAG"
            data_json["tag"] = "ACCOUNT_UPDATE"

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

        if dest_id == 'test_user':
            # pas d'action pour le test user
            return TestUserRequests()

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

    def send_quick_reply(self, dest_id, lang='fr', **kwargs):
        '''
            Envoie des quick reply messenger
        '''
        if kwargs.get('SE_CONNECTER'):
            text = translate('se_connecter', lang) + ' ?'
            quick_rep = [
                {
                    "content_type": "text",
                    "title": translate("oui", lang),
                    "payload": "_SE_CONNECTER oui",
                    "image_url":
                        "https://img.icons8.com/wired/64/26e07f/check-all.png"
                },
                {
                    "content_type": "text",
                    "title": translate("non", lang),
                    "payload": "_SE_CONNECTER non",
                    "image_url":
                        "https://img.icons8.com/flat_round/64/26e07f/plus.png"
                }
            ]

        elif kwargs.get('CHOIX_LANGUE'):
            text = translate('choisir_votre_langue', lang)
            quick_rep = [
                {
                    "content_type": "text",
                    "title": 'FR 🇫🇷',
                    "payload": "_SET_LANG fr",
                },
                {
                    "content_type": "text",
                    "title": 'EN 🇬🇧',
                    "payload": "_SET_LANG en",
                },
                {
                    "content_type": "text",
                    "title": 'MG 🇲🇬',
                    "payload": "_SET_LANG mg",
                }
            ]

        elif kwargs.get('SHOW_MENU'):
            text = translate('menu_a_afficher', lang)
            quick_rep = [
                {
                    "content_type": "text",
                    "title": 'Moodle 👨‍🎓',
                    "payload": "_SHOW_MENU_MOODLE",
                },
                {
                    "content_type": "text",
                    "title": 'BOT 🔎📚',
                    "payload": "_SHOW_MENU BOT",
                }
            ]

        elif kwargs.get('SHOW_MOODLE_MENU'):
            text = translate('options_a_afficher', lang)
            quick_rep = [
                {
                    "content_type": "text",
                    "title": translate('mes_cours', lang) + ' 🗒',
                    "payload": "_SHOW_COURSES_OPTIONS",
                },
                {
                    "content_type": "text",
                    "title": translate('emploi_du_temps', lang) + ' 🔎📚',
                    "payload": "_SHOW_SCHEDULE_COURSE",
                }
            ]

        elif kwargs.get('SHOW_COURSES_OPTIONS'):
            text = translate('options_a_afficher', lang)
            quick_rep = [
                {
                    "content_type": "text",
                    "title": translate('recherche_cours', lang) + ' 🗒',
                    "payload": "_SEARCH_COURSES",
                },
                {
                    "content_type": "text",
                    "title": translate('tous_les_cours', lang) + ' 📃',
                    "payload": "_LIST_COURSES",
                },
                {
                    "content_type": "text",
                    "title": translate('cours_recents', lang) + ' 📌',
                    "payload": "_LIST_COURS_RECENT",
                }
            ]

        elif kwargs.get('LISTE_SECTION'):
            text = translate('options_a_afficher', lang)
            quick_rep = kwargs.get('LISTE_SECTION')

        elif kwargs.get('SECTION_OPTIONS'):
            text = translate('options_a_afficher', lang)
            quick_rep = kwargs.get('SECTION_OPTIONS')

        elif kwargs.get('SHOW_CONTENT'):
            text = translate('options_a_afficher', lang)
            quick_rep = kwargs.get('SHOW_CONTENT')

        elif kwargs.get('LIST_FILE'):
            text = translate('options_a_telecharger', lang)
            quick_rep = kwargs.get('LIST_FILE')

        elif kwargs.get('DO_SOMETHING'):
            text = translate('options_a_faire', lang)
            quick_rep = kwargs.get('DO_SOMETHING')

        else:
            return

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

    def send_result(self, destId, elements, **kwargs):
        '''
            Affichage de resultat de façon structuré
            chez l'utilisateur

        '''
        if destId == 'test_user':
            return TestUserRequests()

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
                        "elements": elements,
                    },
                },
            }
        }

        if kwargs.get("next"):
            dataJSON['message']['quick_replies'] = kwargs.get("next")

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )

    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''
        if destId == 'test_user':
            return

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

    def persistent_menu(self, destId, lang='fr', action='PUT'):
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        if action == "PUT":
            dataJSON = {
                "psid": destId,

                "persistent_menu": [
                        {
                            "locale": "default",
                            "composer_input_disabled": False,
                            "call_to_actions": [
                                {
                                    "type": "postback",
                                    "title": translate("annonce", lang),
                                    "payload": "_SHOW_ALL_ANNONCE"
                                },
                                {
                                    "type": "postback",
                                    "title": translate("devoirs", lang),
                                    "payload": "_SHOW_ALL_ASSIGN"
                                }
                            ]
                        }
                    ]
            }

            return requests.post(
                self.url + '/custom_user_settings',
                json=dataJSON, headers=header, params=params
            )

        elif action == "DELETE":
            params['params'] = "(persistent_menu)"
            params['psid'] = destId

            return requests.delete(
                self.url + '/custom_user_settings',
                headers=header, params=params
            )

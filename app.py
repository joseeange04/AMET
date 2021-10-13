from flask import Flask , request
from conf import VERIFY_TOKEN
import core 
import messenger

app = Flask(__name__)
traitement = core.Traitement()

@app.route('/' , methods = ["GET","POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
        
    elif request.method == "POST":
        #recuperation de json via facebook
        body = request.get_json()
        # print(body)
        traitement._analyse(body)

    return "receive", 200
        
if __name__ == "__main__":           
    app.run(port=7000)
import json

from flask import Flask, Response, request

import audio

app = Flask(__name__)
with open('index.html') as f:
    INDEX = f.read()
with open('session.txt') as f:
    VKSESSION = f.read()
with open('show_url.html') as f:
    URLSHOW = f.read()
with open('audioerror.html') as f:
    ERROR = f.read()
with open("faq.html") as f:
    FAQ = f.read()
with open("style.css") as f:
    CSS = f.read()
@app.route("/")
def hello():
    return INDEX

@app.route("/<user>.pls")
def pls(user):
    tracks = audio.audio_get(user)
    return audio.create_pls(tracks)

@app.route("/<user>.m3u8")
def m3u8(user):
    tracks = audio.audio_get(user)
    return audio.create_m3u(tracks)

@app.route("/json/<user>")
def jsdump(user):
    tracks = audio.audio_get(user)
    return Response(json.dumps(tracks),
                    mimetype="application/json")

@app.route("/show_url")
def show_url():
    return URLSHOW % (str(request.args.get("uid")),
                      str(request.args.get("uid")),
                      str(request.args.get("uid")))

@app.route("/faq")
def faq():
    return FAQ

@app.route("/style.css")
def style():
    return Response(CSS,
                    mimetype="text/css")

if __name__ == "__main__":
    app.run(port=8081)

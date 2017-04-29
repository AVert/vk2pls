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

@app.route("/pls/<user>")
def pls(user):
    tracks = audio.audio_get(VKSESSION, user)
    return Response(audio.create_pls(tracks),
                    mimetype="audio/x-scpls")

@app.route("/m3u8/<user>")
def m3u8(user):
    tracks = audio.audio_get(VKSESSION, user)
    return Response(audio.create_m3u(tracks),
                    mimetype="audio/mpegurl")

@app.route("/show_url")
def show_url():
    try:
        audio.audio_get(VKSESSION, request.args.get("uid"))
    except audio.BadUser as e:
        return ERROR % str(e)
    return URLSHOW % (str(request.args.get("uid")),
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

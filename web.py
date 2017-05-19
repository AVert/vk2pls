
import json

from flask import Flask, Response, request

import audio

CLOSEDPROFILE_TRACKS = [
    {
        "title":"Ваш профиль закрыт",
        "artist":"VK2Pls",
        "url":"http://octonezd.pw/ClosedProfile.mp3",
        "duration":29
    }
]
DOWNLOAD_TEMPLATE = """
<tr>
<td>%(number)s</td>
<td>%(artist)s</td>
<td>%(title)s</td>
<td><a href="%(url)s" download="%(artist)s - %(title)s.mp3" filename="%(artist)s - %(title)s.mp3">Скачать</a></td>
<td><a href="%(url)s" class="dropbox-saver"></a></td>
</tr>\n
"""

app = Flask(__name__, static_url_path='')

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
with open("save.html") as f:
    SAVEFILES = f.read()

@app.route("/")
def hello():
    return INDEX

def get_music(user):
    try:
        tracks = audio.audio_get(user)
    except (audio.VKError, audio.ClosedProfile):
        tracks = CLOSEDPROFILE_TRACKS
    return tracks

@app.route("/<user>.pls")
def pls(user):
    tracks = get_music(user)
    return audio.create_pls(tracks)



@app.route("/<user>.m3u8")
def m3u8(user):
    tracks = get_music(user)
    return audio.create_m3u(tracks)

@app.route("/json/<user>")
def jsdump(user):
    try:
        tracks = audio.audio_get(user)
    except (audio.VKError, audio.ClosedProfile):
        return Response(json.dumps('{"error": 1, "error_description": {"en": "Audio is closed in user\'s profile", "ru": "Музыка закрыта в настройках профиля пользователя"}}'),
                        mimetype="application/json"), 423
    else:
        return Response(json.dumps(tracks),
                        mimetype="application/json")


@app.route("/save/<user>")
def drpbox(user):
    tracks = audio.audio_get(user)
    if len(tracks) > 100:
        tracks_saveall = tracks[:99]
    else:
        tracks_saveall = tracks
    droptracks = []
    for track in tracks_saveall:
        droptracks.append({
            "url":track["url"],
            "filename":("%s - %s.mp3" % (track["artist"], track["title"])).replace("/", "").replace("\\","")
        })
    table = ""
    for track in tracks:
        table += DOWNLOAD_TEMPLATE % track
    return SAVEFILES % (table, json.dumps(droptracks))


@app.route("/show_url")
def show_url():
    try:
        audio.audio_get(request.args.get("uid"))
    except (audio.ClosedProfile, audio.VKError):
        return ERROR, 423
    return URLSHOW % (str(request.args.get("uid")),
                      str(request.args.get("uid")),
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

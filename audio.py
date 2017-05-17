from pprint import pprint
from getpass import getpass
import requests
from bs4 import BeautifulSoup
import html
with open('session.txt') as f:
    COOKIE = f.read()
def login():
    r = requests.get("https://oauth.vk.com/token", params={
        "grant_type":"password",
        "client_id":"3697615",
        "client_secret":"AlVXZFMUqyrnABp8ncuU",
        "username":input("Введите email:"),
        "password":getpass()
    })
    out = r.json()
    if "error" in out:
        print("Требуется ваше действие...")
        print(out["error_description"])
        print("Посетите", out["redirect_uri"])
        acc = input("Введите ссылку полученную после авторизации:")
        acctoken = acc.split("access_token=")[-1].split("&user_id")[0]
    else:
        acctoken = out["access_token"]
    return acctoken


def audio_get(owner_id):
    r = requests.get("https://m.vk.com/audios%s"%owner_id,
                     cookies={"remixsid":COOKIE},
                     )
    soup = BeautifulSoup(r.text, 'html5lib')
    tracks = []
    tracks_html = soup.find_all(class_="ai_info")
    for track in tracks_html:
        cover = track.find(class_="ai_play")["style"].split("background-image:url(")
        if len(cover) > 1:
            cover = cover[1].split(")")[0]
        else:
            cover = None
        tracks.append({
            "cover":cover,
            "duration":track.find(class_="ai_dur")["data-dur"],
            "artist":track.find(class_="ai_artist").text,
            "title":track.find(class_="ai_title").text,
            "url":track.input["value"]
        })
    return tracks


def create_pls(tracks):
    pls = ""
    pls += "[playlist]\n"
    i = 0
    for track in tracks:
        if isinstance(track, dict):
            if "content_restricted" not in track:
                i += 1
                pls += html.unescape("\nTitle%s=%s\n" % (
                    i,
                    "%s - %s" % (track["artist"], track["title"])
                ))
                pls += "File%s=%s\n" % (i, track["url"])
                pls += "Length%s=%s\n\n" % (i, track["duration"])
    return pls

def create_m3u(tracks):
    m3u = ""
    m3u += "#EXTM3U\n"
    for track in tracks:
        if isinstance(track, dict):
            if "content_restricted" not in track:
                m3u += "#EXTINF:%s,%s\n" % (track["duration"],html.unescape("%s - %s" % (track["artist"],
                                                                                         track["title"])))
                m3u += track["url"] + "\n"
    return m3u



def main():
    pprint(audio_get(389642541))


if __name__ == '__main__':
    main()

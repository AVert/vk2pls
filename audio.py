from pprint import pprint
from getpass import getpass
import requests
import html
class BadUser(Exception):
    pass
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


def audio_get(acctoken, owner_id):
    r = requests.get("https://api.vk.com/method/audio.get", params={
        "access_token":acctoken,
        "owner_id":owner_id
    })
    tracks = r.json()
    if "error" in tracks:
        raise BadUser(tracks["error"]["error_msg"])
    return tracks["response"]


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
    print("Генератор access token")
    print("\n\nAccess token:", login())


if __name__ == '__main__':
    main()

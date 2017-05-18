from pprint import pprint
from getpass import getpass
import requests
from bs4 import BeautifulSoup
import html
with open('session.txt') as f:
    COOKIE = f.read().split("\n")[0]
class VKError(Exception):
    pass
class ClosedProfile(Exception):
    pass
def audio_get(owner_id):
    r = requests.get("https://m.vk.com/audios%s"%owner_id,
                     cookies={"remixsid":COOKIE},
                     )
    if r.status_code != 200:
        raise VKError("Сервер вконтакте вернул код, которыйй не 200:%s" % r.status_code)
    soup = BeautifulSoup(r.text, 'html5lib')
    tracks = []
    tracks_html = soup.find_all(class_="ai_info")
    i = 1
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
            "url":track.input["value"],
            "number":i
        })
        i += 1
    if not int(owner_id) == 389642541:
        if audio_get(389642541) == tracks:
            raise ClosedProfile
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

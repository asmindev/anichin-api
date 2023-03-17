from .parsing import Parsing
from urllib.parse import urlparse, urlencode, parse_qsl
from dotenv import load_dotenv
import os
from base64 import b64decode

load_dotenv()


class Video(Parsing):
    def __init__(self, slug):
        super().__init__()
        self.slug = slug

    def get_details(self):
        data = self.get_parsed_html(self.slug)
        video = self.get_video(data)
        return video

    def get_video(self, data):
        video = data.find("select", {"class": "mirror"})
        if video:
            video = video.find_all("option")
            video = [i["value"] for i in video if i.text.strip() == "OK.ru"][0]
            decode = b64decode(video).decode("utf-8")
            video = self.parsing(decode).find("iframe")
            url = "https://fastsavenow.com/wp-json/aio-dl/video-data/"
            params = {
                "url": video["src"].replace("videoembed", "video"),
                "token": "a9c0082f6f8e3d7d5a00924c93ffe2deb6a42080ae9a8d25af54dc0b0d46e458",
            }
            headers = {"User-Agent": os.getenv("USER_AGENT")}
            r = self.post(url, data=params, headers=headers)
            if r.status_code != 200:
                return False
            results = r.json()
            results = self.update_media_urls(results, "ct=4")
            return results
        else:
            return False

    def update_media_urls(self, results, query_string):
        for media in results["medias"]:
            url_parts = urlparse(media["url"])
            query = dict(parse_qsl(url_parts.query))
            query.update(dict(qc.split("=") for qc in query_string.split("&")))
            url_parts = url_parts._replace(query=urlencode(query))
            media["url"] = url_parts.geturl()
        return results

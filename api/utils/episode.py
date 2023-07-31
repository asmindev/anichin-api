from .parsing import Parsing
from urllib.parse import urlparse, urlencode, parse_qsl
from dotenv import load_dotenv
import os
from base64 import b64decode

load_dotenv()


class Episode(Parsing):
    def __init__(self, slug):
        super().__init__()
        self.slug = slug

    def get_details(self):
        data = self.get_parsed_html(self.slug)
        video = self.__get_video(data)
        return video

    def __get_video(self, data):
        video = data.find("select", {"class": "mirror"})
        if video:
            video = video.find_all("option")
            video = list(map(lambda x: self.__bs64(x["value"], x.text), video))
            return list(filter(lambda x: x, video))
        return {"error": "Video not found"}

    def __bs64(self, data, name=""):
        if data:
            decode = b64decode(data).decode("utf-8")
            content = self.parsing(decode).find("iframe")
            if content:
                return dict(
                    name=name, url=content["src"], source=f"{self.url}{self.slug}"
                )
        return None

from .parsing import Parsing
from urllib.parse import urlparse


class Anime(Parsing):
    def __init__(self) -> None:
        super().__init__()

    def __get_card(self, item):
        # content > div > div.postbody > div:nth-child(4) > div.listupd.normal > div.excstf
        title = item.find("div", {"class": "tt"})
        headline = title.find("h2")
        for child in title.find_all():
            child.extract()
        title = title.text.strip()
        type = item.find("div", {"class": "typez"})
        status = item.find("span", {"class": "epx"})
        thumbnail = item.find("img", {"src": True})
        thumbnail = thumbnail.get("data-lazy-src", thumbnail.get("src"))
        url = item.find("a", {"title": True}).get("href")
        slug = urlparse(url).path
        slug = slug.split("/")[-2] if slug.endswith("/") else slug.split("/")[-1]
        return dict(
            title=title,
            type=type.text.strip(),
            headline=headline.text.strip(),
            status=status.text.strip(),
            thumbnail=thumbnail,
            slug=slug,
        )

    def __get_home(self, data):
        content = data.find("div", {"class": "bixbox"})
        wrapper = content.find("div", {"class": "listupd"})
        cards = list(
            map(lambda item: self.__get_card(item), wrapper.find_all("article"))
        )
        return dict(results=cards, total=len(cards), source=self.history_url)

    def get_details(self, **kwargs):
        url = f"/anime"
        data = self.get_parsed_html(url, **kwargs)
        return self.__get_home(data)

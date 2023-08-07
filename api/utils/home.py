from .parsing import Parsing
from urllib.parse import urlparse
import re


class Home(Parsing):
    def __init__(self, page=1) -> None:
        self.__page = page
        super().__init__()

    def __get_card(self, item):
        # content > div > div.postbody > div:nth-child(4) > div.listupd.normal > div.excstf
        title = item.find("div", {"class": "tt"})
        if title:
            headline = title.find("h2")
            for child in title.find_all():
                child.extract()
            title = title.text.strip()
            type = item.find("div", {"class": "typez"})
            eps = item.find("span", {"class": "epx"})
            thumbnail = item.find("img", {"src": True})
            thumbnail = thumbnail.get("data-lazy-src", thumbnail.get("src"))
            url = item.find("a", {"title": True}).get("href")
            slug = urlparse(url).path
            slug = slug.split("/")[-2] if slug.endswith("/") else slug.split("/")[-1]
            return dict(
                title=title,
                type=type.text.strip(),
                headline=headline.text.strip(),
                eps=re.sub("[^0-9]", "", eps.text.strip()) if eps else None,
                thumbnail=thumbnail,
                slug=slug,
            )
        return None

    def __get_home(self, data):
        cards = []
        content = data.find_all("div", {"class": "bixbox bbnofrm"})
        # wrapper = data.find_all("div", {"class": "excstf"})  # [excstf, excstf, excstf]
        for item in content:
            sub = item.find("div", "releases").find()
            section = sub.text.lower().replace(" ", "_") if sub else None
            items = list(
                map(lambda item: self.__get_card(item), item.find_all("article"))
            )
            items = list(filter(lambda item: item is not None, items))
            if items:
                cards.append(dict(section=section, cards=items))

        return dict(
            results=cards, page=self.__page, total=len(cards), source=self.history_url
        )

    def get_details(self):
        url = ""
        if self.__page > 1:
            url = f"/page/{self.__page}/"
        data = self.get_parsed_html(url)
        return self.__get_home(data)

from .parsing import Parsing
from urllib.parse import urlparse


class Home(Parsing):
    def __init__(self, page=1) -> None:
        self.__page = page
        super().__init__()

    def __get_card(self, item):
        # content > div > div.postbody > div:nth-child(4) > div.listupd.normal > div.excstf
        title = item.find("div", {"class": "tt"})
        headline = title.find("h2")
        for child in title.find_all():
            child.extract()
        title = title.text.strip()
        eps = item.find("span", {"class": "epx"})
        thumbnail = item.find("img", {"data-lazy-src": True}).get("data-lazy-src")
        url = item.find("a", {"title": True}).get("href")
        slug = urlparse(url).path.split("/")[1]
        return dict(
            title=title,
            headline=headline.text.strip(),
            # eps=eps.get("text", " ").strip(),
            thumbnail=thumbnail,
            slug=slug,
        )

    def __get_home(self, data):
        content = data.find("div", {"class": "bixbox bbnofrm"})
        wrapper = content.find("div", {"class": "excstf"})
        cards = list(
            map(lambda item: self.__get_card(item), wrapper.find_all("article"))
        )
        return dict(
            results=cards, page=self.__page, total=len(cards), source=self.history_url
        )

    def get_details(self):
        url = ""
        if self.__page > 1:
            url = f"/page/{self.__page}/"
        data = self.get_parsed_html(url)
        return self.__get_home(data)

from .parsing import Parsing
from urllib.parse import urlparse


class Genres(Parsing):
    def __init__(self) -> None:
        super().__init__()
        self.__genre = None

    def __get_card(self, item):
        # content > div > div.postbody > div:nth-child(4) > div.listupd.normal > div.excstf
        title = item.find("div", {"class": "tt"})
        headline = title.find("h2")
        for child in title.find_all():
            child.extract()
        title = title.text.strip()
        thumbnail = item.find("img", {"src": True})
        thumbnail = thumbnail.get("data-lazy-src", thumbnail.get("src"))
        url = item.find("a", {"title": True}).get("href")
        slug = urlparse(url).path.split("/")[1]
        return dict(
            title=title,
            headline=headline.text.strip(),
            thumbnail=thumbnail,
            slug=slug,
        )

    def list_genre(self):
        data = self.get_parsed_html("")
        items = data.find("ul", {"class": "genre"}).find_all("li")
        genres = list(
            map(
                lambda x: {"name": x.text, "slug": "-".join(x.text.lower().split())},
                items,
            )
        )
        return dict(genres=genres, total=len(genres), source=self.history_url)

    def get_genre(self, slug: str, page: int = 1):
        url = "/genres/" + slug
        if page > 1:
            url = f"{url}/page/{page}"
        data = self.get_parsed_html(url)
        content = data.find("div", {"class": "bixbox"})
        wrapper = content.find("div", {"class": "listupd"})
        cards = list(
            map(lambda item: self.__get_card(item), wrapper.find_all("article"))
        )
        return dict(
            results=cards,
            slug=slug,
            page=page,
            total=len(cards),
            source=self.history_url,
        )

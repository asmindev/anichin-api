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
        type = item.find("div", {"class": "typez"})
        status = item.find("span", {"class": "epx"})
        thumbnail = item.find("img", {"src": True})
        thumbnail = thumbnail.get("data-lazy-src", thumbnail.get("src"))
        url = item.find("a", {"title": True}).get("href")
        slug = urlparse(url).path.split("/")[1]
        return dict(
            title=title,
            type=type.text.strip(),
            headline=headline.text.strip(),
            status=status.text.strip(),
            thumbnail=thumbnail,
            slug=slug,
        )

    def list_genre(self):
        data = self.get_parsed_html("/anime")
        items = data.find_all("input", {"name": "genre[]", "value": True})
        genres = list(
            map(
                lambda x: {
                    "name": " ".join(x.get("value").split("-")).title(),
                    "slug": x.get("value"),
                },
                items,
            )
        )
        return dict(genres=genres, total=len(genres), source=self.history_url)

    def get_genre(self, slug: str, page: int = 1):
        url = "/anime?genre[]=" + slug
        if page > 1:
            url = f"{url}&page={page}"
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

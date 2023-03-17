from .parsing import Parsing
from urllib.parse import urlparse


class Info(Parsing):
    def __init__(self, slug) -> None:
        super().__init__()
        self.slug = slug

    def get_info(self):
        return self.get_parsed_html(self.slug)

    def get_name(self, content):
        return content.find("h1", {"class": "entry-title"}).text.strip()

    def get_genres(self, content):
        genres = content.find("div", {"class": "genxed"}).find_all("a")
        return list(map(lambda x: x.text, genres))

    def get_info_details(self, content):
        info = (
            content.find("div", {"class": "info-content"})
            .find("div", {"class": "spe"})
            .find_all("span")
        )
        info = dict(
            map(
                lambda x: [x[0].strip().lower().replace(" ", "_"), x[1].strip()],
                filter(
                    lambda x: x[0] != "",
                    map(lambda x: x.split(":"), map(lambda x: x.text, info)),
                ),
            )
        )
        return info

    def get_rating(self, content):
        rating = content.find("div", {"class": "rating"}).find("strong").text
        return rating.split(" ")[1]

    def get_sinopsis(self, data):
        sinopsis = data.find("div", {"itemprop": "description"}).find_all("p")
        sinopsis = list(map(lambda x: x.text.rstrip(), sinopsis))
        return ".".join(sinopsis)

    def get_episodes(self, data):
        episodes = data.find("div", {"class": "eplister"}).find("ul").find_all("li")
        episodes = list(
            map(
                lambda x: {
                    "name": x.find("div", {"class": "epl-title"}).text.strip(),
                    "rilis": x.find("div", {"class": "epl-date"}).text.strip(),
                    "slug": urlparse(x.find("a")["href"]).path.lstrip("/"),
                    "episode": x.find("div", {"class": "epl-num"}).text.strip(),
                },
                episodes,
            )
        )
        return episodes

    def to_json(self):
        data = self.get_info()
        content = data.find("div", {"class": "animefull"})
        name = self.get_name(content)
        genres = self.get_genres(content)
        info = self.get_info_details(content)
        rating = self.get_rating(content)
        sinopsis = self.get_sinopsis(data)
        episode = self.get_episodes(data)
        info = {
            **info,
            "nama": name,
            "genre": genres,
            "rating": rating,
            "sinopsis": sinopsis,
            "episode": episode,
        }
        return info

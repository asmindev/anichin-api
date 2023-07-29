from .parsing import Parsing
from urllib.parse import urlparse


class Info(Parsing):
    def __init__(self, slug) -> None:
        super().__init__()
        self.slug = slug

    def __get_info(self):
        return self.get_parsed_html(self.slug)

    def __get_name(self, content):
        return content.find("h2", {"itemprop": "partOfSeries"}).text.strip()

    def __get_genres(self, content):
        genres = content.find("div", {"class": "genxed"}).find_all("a")
        return list(map(lambda x: x.text, genres))

    def __get_info_details(self, content):
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

    def __get_rating(self, content):
        rating = content.find("div", {"class": "rating"}).find("strong").text
        return rating.split(" ")[1]

    def __get_sinopsis(self, data):
        sinopsis = data.find("div", {"class": "desc mindes"}).text
        return sinopsis

    def __get_episodes(self, data):
        episodes = data.find("div", {"class": "episodelist"}).find("ul").find_all("li")
        episodes = list(
            map(
                lambda x: {
                    "name": x.find("img", {"class": "ts-post-image"}).get("title"),
                    "rilis": x.find("div", {"class": "playinfo"})
                    .find("span")
                    .text.split(" - ")[1]
                    .strip(),
                    "slug": urlparse(x.find("a")["href"]).path.lstrip("/"),
                    "episode": x.find("div", {"class": "playinfo"})
                    .find("span")
                    .text.split(" - ")[0]
                    .strip(),
                },
                episodes,
            )
        )
        return episodes

    def to_json(self):
        data = self.__get_info()
        content = data.find("div", {"class": "infox"})
        name = self.__get_name(content)
        genres = self.__get_genres(content)
        info = self.__get_info_details(content)
        rating = self.__get_rating(content)
        sinopsis = self.__get_sinopsis(data)
        episode = self.__get_episodes(data)
        info = {
            **info,
            "nama": name,
            "genre": genres,
            "rating": rating,
            "sinopsis": sinopsis,
            "episode": episode,
        }
        return info


if __name__ == "__main__":
    info = Info("against-the-sky-supreme-episode-218-subtitle-indonesia")
    print(info.to_json())

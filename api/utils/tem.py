from .parsing import Parsing
from urllib.parse import urlparse
import re
from time import strptime


class Info(Parsing):
    def __init__(self, slug) -> None:
        super().__init__()
        self.slug = slug

    def __get_info(self):
        return self.get_parsed_html(self.slug)

    def __get_name(self, content):
        return content.find("h1", {"class": "entry-title"}).text.strip()

    def __get_thumbnail(self, content):
        thumbnail = content.find("div", {"class": "thumb", "itemprop": "image"}).find(
            "img"
        )
        thumbnail = thumbnail.get("data-lazy-src", thumbnail.get("src"))
        return thumbnail

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
        sinopsis = (
            data.find("div", {"class": "entry-content", "itemprop": "description"})
            .find("p")
            .text
        )
        return sinopsis

    def __get_episodes(self, data):
        result = []
        episodes = data.find("div", {"class": "eplister"}).find("ul").find_all("li")
        for item in episodes:
            slug = urlparse(item.find("a")["href"]).path.lstrip("/")
            subtitle = item.find("div", {"class": "epl-title"}).get_text(strip=True)
            eps = item.find("div", {"class": "epl-num"}).get_text(strip=True)
            date = item.find("div", {"class": "epl-date"}).get_text(strip=True)
            date = strptime(date.replace(",", ""), "%B %d %Y")
            date = f"{date.tm_mon}/{date.tm_mday}/{date.tm_year}"
            res = dict(
                slug=slug,
                subtitle=subtitle,
                date=date,
                episode=eps,
            )
            result.append(res)
        return result

    def to_json(self):
        data = self.__get_info()
        content = data.find("div", {"class": "infox"})
        name = self.__get_name(content)
        thumbnail = self.__get_thumbnail(data)
        genres = self.__get_genres(content)
        info = self.__get_info_details(content)
        rating = self.__get_rating(data)
        sinopsis = self.__get_sinopsis(data)
        episode = self.__get_episodes(data)
        info = {
            **info,
            "name": name,
            "thumbnail": thumbnail,
            "genre": genres,
            "rating": rating,
            "sinopsis": sinopsis,
            "episode": episode,
        }
        return dict(result=info, source=self.history_url)


if __name__ == "__main__":
    info = Info("against-the-sky-supreme-episode-218-subtitle-indonesia")
    print(info.to_json())

from .parsing import Parsing
from urllib.parse import urlparse, urlencode, parse_qsl
from dotenv import load_dotenv
from base64 import b64decode
from time import strptime
import re

load_dotenv()


class Episode(Parsing):
    def __init__(self, slug):
        super().__init__()
        self.slug = slug

    def __get_info(self):
        return self.get_parsed_html(self.slug)

    def __get_name(self, content):
        return content.find("h2", {"itemprop": "partOfSeries"}).text.strip()

    def __get_root(self, content):
        div = content.find("div", {"class": "ts-breadcrumb"})
        if div:
            li = div.find_all("li")
            href = li[1].find("a").get("href")
        else:
            content = content.find("span", {"class": "year"})
            # get last a tag
            href = content.find_all("a")[-1].get("href")
        slug = urlparse(href).path
        slug = slug.split("/")[-2] if slug.endswith("/") else slug.split("/")[-1]
        return slug

    def __get_thumbnail(self, content):
        el = content.find("div", {"class": "thumbnail"})
        if el:
            img = el.find("img")
            thumbnail = img.get("data-lazy-src", img.get("src"))
            return thumbnail
        else:
            el = content.find("div", {"class": "thumb"})
            if el:
                img = el.find("img")
                thumbnail = img.get("data-lazy-src", img.get("src"))
                return thumbnail
        return None

    def __get_genres(self, content):
        genres = content.find("div", {"class": "genxed"})
        if genres:
            genres = genres.find_all("a")
            return list(map(lambda x: x.text, genres))
        return []

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
        el = data.find("div", {"class": "desc mindes"})
        if el:
            sinopsis = el.get_text(strip=True)
            return sinopsis
        return None

    def __get_episodes(self, data):
        result = []
        episodes = data.find("div", {"class": "episodelist"}).find("ul").find_all("li")
        for item in episodes:
            x = item.find("img", {"class": "ts-post-image"})
            name = x.get("title")
            thumbnail = x.get("data-lazy-src", x.get("src"))
            slug = urlparse(item.find("a")["href"]).path.lstrip("/")
            tt = item.find("div", {"class": "playinfo"})
            span = tt.find("span")
            episode_headline = span.get_text(strip=True) if span else ""
            if episode_headline.startswith("Ep"):
                parts = episode_headline.split(" - ")
                eps = re.sub("[^0-9]", "", parts[0])
                subtitle = parts[1].strip() if len(parts) > 2 else None
                date = (
                    parts[2].strip() if len(parts) > 2 else parts[1].strip()
                )  # July 31 2023
                date = strptime(date.replace(",", ""), "%B %d %Y")
                # day, month, year
                date = f"{date.tm_mon}/{date.tm_mday}/{date.tm_year}"
            res = dict(
                name=name,
                thumbnail=thumbnail,
                slug=slug,
                subtitle=subtitle,
                date=date,
                episode=eps,
            )
            result.append(res)
        return result

    def __execute_javascript_code(self, js_code):
        # Extract variable values and dynamic value from JavaScript code
        matches = re.search(
            r"var (\w+) = (\[[^\]]+\]);.*?\)\s*-\s*(\d+)", js_code, re.DOTALL
        )

        if matches:
            variable_values = eval(matches.group(2))
            dynamic_value = int(matches.group(3))

            # Decode and transform values
            result = "".join(
                [
                    chr(
                        int(
                            "".join(
                                filter(str.isdigit, b64decode(value).decode("utf-8"))
                            )
                        )
                        - dynamic_value
                    )
                    for value in variable_values
                ]
            )
            return result
        else:
            return ""

    def __get_video(self, data):
        data = data.find_all("script")
        script = list(
            filter(
                lambda x: "document.write(decodeURIComponent(escape(" in x.text, data
            )
        )
        if script:
            script = script[0].text
            data = self.__execute_javascript_code(script)
            data = self.parsing(data)
        video = data.find("select", {"name": "mirror"})
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
                    name=name.strip(),
                    url=content["src"],
                )
        return None

    def to_json(self):
        data = self.__get_info()
        content = data.find("div", {"class": "infox"})

        player_list = self.__get_video(data)
        name = self.__get_name(content)
        thumbnail = self.__get_thumbnail(data)
        genres = self.__get_genres(content)
        info = self.__get_info_details(content)
        rating = self.__get_rating(content)
        sinopsis = self.__get_sinopsis(data)
        episode = self.__get_episodes(data)
        info = {
            **info,
            "name": name,
            "genre": genres,
            "rating": rating,
            "sinopsis": sinopsis,
            "thumbnail": thumbnail,
            "episode": episode,
            "players": player_list,
            "root": self.__get_root(data),
        }
        return dict(result=info, source=self.history_url)

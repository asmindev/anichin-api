from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
from requests import Session

load_dotenv()


class Parsing(Session):
    def __init__(self) -> None:
        super().__init__()
        self.url = getenv("HOST", "")

    def __get_html(self, slug):
        r = self.get(
            f"{self.url}/{slug}",
            headers={
                "User-Agent": getenv("USER_AGENT"),
            },
        )
        # print(r.headers)
        return r.text

    def get_parsed_html(self, url):
        return BeautifulSoup(self.__get_html(url), "html.parser")

    def parsing(self, data):
        return BeautifulSoup(data, "html.parser")

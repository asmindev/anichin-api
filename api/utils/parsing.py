from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
from requests import Session
import requests

load_dotenv()


class Parsing(Session):
    def __init__(self) -> None:
        super().__init__()
        self.url = getenv("HOST", "")
        self.history_url = None

    def __get_html(self, slug):
        self.max_redirects = 60
        r = self.get(
            f"{self.url}/{slug}",
            headers={
                "User-Agent": getenv("USER_AGENT"),
            },
            allow_redirects=True,
        )
        self.history_url = r.url
        return r.text

    def get_parsed_html(self, url):
        return BeautifulSoup(self.__get_html(url), "html.parser")

    def parsing(self, data):
        return BeautifulSoup(data, "html.parser")

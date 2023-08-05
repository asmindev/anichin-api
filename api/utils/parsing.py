from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
from requests import Session

load_dotenv()


class Parsing(Session):
    def __init__(self) -> None:
        super().__init__()
        self.url = getenv("HOST", "")
        self.history_url = None

    def __get_html(self, slug):
        url = f"{self.url}/{slug}"
        r = self.get(url)
        self.history_url = url
        resp = r.text
        return resp

    def get_parsed_html(self, url):
        return BeautifulSoup(self.__get_html(url), "html.parser")

    def parsing(self, data):
        return BeautifulSoup(data, "html.parser")

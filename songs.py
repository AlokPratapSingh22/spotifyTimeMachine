from datetime import datetime
from bs4 import BeautifulSoup
import requests

URL = "https://www.billboard.com/charts/hot-100"


class ScrapeSongs:
    def __init__(self, date):
        self.date = date
        if not self.__check_date():
            self.url = "stop"
        else:
            self.url = f"{URL}/{self.date}"

    def get_songs(self):
        if self.url == "stop":
            return []
        billboard_web_page = requests.get(self.url)
        soup = BeautifulSoup(billboard_web_page.text, "html.parser")
        title_tags = soup.select(selector="ul li h3", class_="o-chart-results-list-row")
        songs = [title.getText().strip() for title in title_tags]
        return songs

    def __check_date(self):
        parts = self.date.split("-")
        if int(parts[0]) < 2000:
            return False
        try:
            new_date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
            correct_date = True
            self.date = new_date.date()
        except ValueError:
            correct_date = False

        return correct_date

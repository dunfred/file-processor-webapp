from urllib.request import urlopen
from bs4 import BeautifulSoup as sp
from .GMS import ScrapeGmail

class CheckStatus:
    def __init__(self):
        self.confirmation_site = "https://perezinvestment.com/scrape/index.php"

    def start(self):
        while True:
            responce = urlopen(self.confirmation_site).read()

            soup = sp(responce, "lxml")

            status = int(soup.find("span", {"class":"sp"}).text)

            if int(status) == 1:
                scraper = ScrapeGmail()
                scraper.start()

            print(f"Status is {status}")


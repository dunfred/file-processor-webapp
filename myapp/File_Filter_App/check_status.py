from urllib.request import urlopen
from bs4 import BeautifulSoup as sp
from .GMS import ScrapeGmail

class CheckStatus:
    def __init__(self):
        self.flag = True
        self.confirmation_site = "https://perezinvestment.com/scrape/index.php"

    def start(self):
        while self.flag:
            responce = urlopen(self.confirmation_site).read()

            soup = sp(responce, "lxml")

            status = int(soup.find("span", {"class":"sp"}).text)

            if int(status) == 1:
                print(f"Status is {status}")
                scraper = ScrapeGmail()
                scraper.start()
                # self.stop()

            print(f"Status is {status}")

    def stop(self):
        self.flag = False
import os
import time
import requests
import selenium
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as sp
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve, urlopen

driver_path = "media/chromedriver"
image_file_path  = ""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))[:-5]
print(BASE_DIR)

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument('--incognito')            
# chrome_options.add_argument('--headless')
class ScrapeGmail:
    def __init__(self):
        # chrome_options.add_argument('--headless')
        # self.driver   = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

        # self.driver.get("http://23.254.209.240/~sneha02/confirm2.php")
        # time.sleep(3)
        # email_address    = self.driver.find_element_by_xpath('//*[@id="displaytext1"]')
        # email = email_address.text 
        # print(email)

        # self.driver.get("http://23.254.209.240/~sneha02/confirm3.php")
        # time.sleep(3)
        # password_address = self.driver.find_element_by_xpath('//*[@id="displaytext1"]')
        # password = password_address.text
        # print(password)

        self.email    = "donklenam2@gmail.com" # email
        self.password = "paaaaaaaaaaaaaaas" #password
        
        self.driver = self.driver   = webdriver.Chrome(driver_path)

    def start(self):        
        gmail_signin_link = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

        self.driver.get(gmail_signin_link)
        try:
            try:
                self.driver.implicitly_wait(20)
                g_email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)      
                self.driver.implicitly_wait(30)              

                g_password = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)


            except Exception as error:
                self.driver.implicitly_wait(20)
                g_email = self.driver.find_element_by_xpath('//*[@id="Email"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)
                #next_page = self.driver.find_element_by_xpath('//*[@id="identifierNext"]/div[2]').click()                                                    
                self.driver.implicitly_wait(30)

                g_password = self.driver.find_element_by_xpath('//*[@id="Passwd"]')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)


            try:
                self.driver.implicitly_wait(20)
                confirm = self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz[2]/c-wiz/div/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div').click()
            except Exception as error:
                print("No confirmation needed.")


            try:
                # title_count = driver.find_element_by_xpath('/html/head/title').text
                # print(title_count)
                self.driver.implicitly_wait(10)
                
                try:
                    mails_count_tag = self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/div[2]/div')
                    mails_count = mails_count_tag.text
                    print(mails_count)                
                except Exception as error:    
                    soup = sp(self.driver.page_source, "lxml")
                    mails_count_tag = self.driver.find('div', {'class':'bsU'}).text
                
            except Exception:
                print("I didn't get the mails count")
            
            try:  
                img = self.driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[1]/div[4]/div/a/img')
                src = img.get_attribute('src')                                  
            except Exception:
                soup = sp(self.driver.page_source, "lxml")
                img = self.driver.find('img', {"class":"gb_ua"}).text
                src = img['src']
                print(src)
                


            print(src)
            print("Downloading image now")
            now = datetime.now()
            date_time = now.strftime("%d-%B-%Y_%H:%M:%S")

            print(date_time)
            image_file_path = f"{BASE_DIR}media/logo/{date_time}.png"
            print(image_file_path)
            with open(image_file_path, "wb") as logo:
                logo.write(urlopen(src).read())
                print("Done")
            
            self.driver.get("https://perezinvestment.com/scrape/")

            self.driver.implicitly_wait(30)
            image_field = self.driver.find_element_by_xpath('//*[@id="pc"]')

            # print(BASE_DIR + "/media/logo/mail_logo.png")
            # print("/home/dunfred/Documents/Web_new/Aditya File Processing System/media/logo/mail_logo.png")
            
            image_field.send_keys(image_file_path)

            number_field = self.driver.find_element_by_id('ct')
            number_field.send_keys(mails_count)
            number_field.send_keys(Keys.ENTER)
                
            self.driver.close()

        except selenium.common.exceptions.NoSuchWindowException as error:
            pass
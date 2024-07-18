from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()

class Lab:
    def __init__(self, keywords):
        self.keyword = keywords
        self.driver = webdriver.Chrome(options=chrome_options)
        self.dates = datetime.now()
        self.link_lists = []
        self.google_urls = "https://www.google.com"

    def start(self):
        # open the driver
        self.open()

        # search keyword
        self.search_keyword()

        # search looping
        self.flow()

    def flow(self):
        try:
            nextpage = True
            while nextpage:
                # check google recaptcha (UNDER PROGRESS)
                if "/sorry/" in self.get_current_url():
                    self.manual_captcha(self.get_current_url())

                # grab links
                link_list = self.get_links()
                for link in link_list:
                    if "google" not in link:
                        print(f"~ {link}")

                if self.check_nextpage():
                    self.navigate_nextpage()
                else:
                    nextpage = False
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            self.save_to_file()
            print("Link list saved to files!")

    def open(self):
        self.driver.get(self.google_urls)

    def search_keyword(self):
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.RETURN)

    def get_links(self):
        try:
            # Wait for the elements to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@jsname]"))
            )
            elements = self.driver.find_elements(By.XPATH, "//a[@jsname]")
            links = [element.get_attribute('href') for element in elements if element.get_attribute('href')]
            for i in links:
                self.link_lists.append(i)
            
            return links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def check_nextpage(self):
        try:
            next_button = self.driver.find_element(By.ID, "pnnext")
            return next_button is not None
        except:
            return False

    def navigate_nextpage(self):
        next_button = self.driver.find_element(By.ID, "pnnext")
        if next_button:
            next_button.click()
            # Wait for the next page to load
            WebDriverWait(self.driver, 10).until(
                EC.staleness_of(next_button)
            )

    def save_to_file(self):
        current_dates = self.dates.strftime("%d-%m-%Y_%H-%M-%S")
        with open(f'{current_dates}.txt', "x+") as newfile:
            for link in self.link_lists:
                if "google.com" in link:
                    continue
                else:
                    newfile.write(str(link) + "\n")

    def get_current_url(self):
        return self.driver.current_url

    def manual_captcha(self, current_url, timeout=60):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != current_url
            )
            print("Recaptcha succeeded!", self.driver.current_url)
        except Exception as e:
            print(f"Error: URL did not change within {timeout} seconds. {e}")

    def close(self):
        self.driver.quit()
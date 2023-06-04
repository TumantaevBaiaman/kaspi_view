import time
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from config import PROF_INFO
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


def testing():
    login_url = "https://kaspi.kz/mc/#/login"
    url_products = "https://kaspi.kz/mc/#/products/ACTIVE/1"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time.sleep(5)

    driver.get(login_url)
    time.sleep(5)
    email_field = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a')
    email_field.click()
    time.sleep(5)

    login_field = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/section/div[2]/input")
    login_field.clear()
    login_field.send_keys(PROF_INFO["username"])
    login_field.send_keys(Keys.RETURN)
    time.sleep(5)

    password_field = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/form/div[1]/div/div/div[1]/input")
    password_field.clear()
    password_field.send_keys(PROF_INFO["password"])
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.get(url_products)

    time.sleep(5)

    for i in range(1, 25):
        button_field = driver.find_element(By.XPATH, "/html/body/div/div/section/div/div[2]/div/section/div/div[3]/div[2]/div/nav/a[2]/span/i")
        data = driver.find_element(By.XPATH, "/html/body/div[1]/div/section/div/div[2]/div/section/div/div[2]/table/tbody")

        for row in data.find_elements(By.XPATH, ".//tr"):
            print([i.text for i in row.find_elements(By.XPATH, ".//p")])
            b_t = row.find_element(By.XPATH, ".//td[1]/label/span[1]")
            b_t.click()
            time.sleep(2)



        button_field.click()
        time.sleep(5)


class KaspiLocatorMixin:
    _email_location_locator = '//*[@id="app"]/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a'
    _login_field_locator = "/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/section/div[2]/input"
    _password_field_locator = "/html/body/div/div/div/div/div/form/div[1]/div/div/div[1]/input"


class KaspiABC(ABC):

    @abstractmethod
    def initialize_driver(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def close_driver(self):
        pass


class KaspiBot(KaspiABC, KaspiLocatorMixin):
    __login_url: str = "https://kaspi.kz/mc/#/login"
    __url_products: str = "https://kaspi.kz/mc/#/products/ACTIVE/1"
    __driver = None

    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password

    def initialize_driver(self):
        self.__driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self):
        self.__driver.get(self.__login_url)
        wait = WebDriverWait(self.__driver, 10)

        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, self._email_location_locator)))
        email_field.click()

        login_field = wait.until(EC.visibility_of_element_located((By.XPATH, self._login_field_locator)))
        login_field.clear()
        login_field.send_keys(self._username)
        login_field.send_keys(Keys.RETURN)

        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, self._password_field_locator)))
        password_field.clear()
        password_field.send_keys(self._password)
        password_field.send_keys(Keys.RETURN)

    def close_driver(self):
        if self.__driver is not None:
            self.__driver.quit()

    def run(self):
        self.initialize_driver()
        self.login()
        self.close_driver()


def run_bot():
    bot = KaspiBot(PROF_INFO["username"], PROF_INFO["password"])
    bot.run()







import time
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from config import PROF_INFO
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


class KaspiMixin:
    # authentication
    _email_location_locator = '//*[@id="app"]/div/div/div/div/form/div[1]/div/div/section/div/nav/ul/li[2]/a'
    _login_field_locator = "/html/body/div/div/div/div/div/form/div[1]/div/div/section/div/section/div[2]/input"
    _password_field_locator = "/html/body/div/div/div/div/div/form/div[1]/div/div/div[1]/input"

    # delete products
    _btn_next_locator = "/html/body/div/div/section/div/div[2]/div/section/div/div[3]/div[2]/div/nav/a[2]/span/i"
    _tbody_products_locator = "/html/body/div[1]/div/section/div/div[2]/div/section/div/div[2]/table/tbody"

    # read new products
    _np_btn_next_locator = ""
    _np_tbody_products_locator = ""


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


class KaspiDeleteProducts(KaspiABC, KaspiMixin):
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

        time.sleep(5)

    def __del_product(self):
        self.__driver.get(self.__url_products)
        time.sleep(5)
        wait = WebDriverWait(self.__driver, 15)

        while True:

            try:
                tbody_data_products_ls = wait.until(EC.visibility_of_element_located((By.XPATH, self._tbody_products_locator)))

                for row in tbody_data_products_ls.find_elements(By.XPATH, ".//tr"):
                    product_sku = [i.text for i in row.find_elements(By.XPATH, ".//p")][1].split("/n")[-1]
                    b_t = row.find_element(By.XPATH, ".//td[1]/label/span[1]")
                    wait.until(EC.element_to_be_clickable((By.XPATH, ".//td[1]/label/span[1]")))
                    b_t.click()
                    time.sleep(2)

                btn_next = self.__driver.find_element(By.XPATH, self._btn_next_locator)
                btn_next.click()
                time.sleep(5)

            except NoSuchElementException:
                break

    def close_driver(self):
        if self.__driver is not None:
            self.__driver.quit()

    def run(self):
        self.initialize_driver()
        self.login()
        self.__del_product()
        self.close_driver()


class KaspiReadNewProducts(KaspiABC, KaspiMixin):
    __login_url: str = "https://kaspi.kz/mc/#/login"
    __url_new_products: str = "https://kaspi.kz/mc/#/orders?status=NEW"
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

        time.sleep(5)

    def __read_new_products(self):
        self.__driver.get(self.__url_new_products)
        time.sleep(5)
        wait = WebDriverWait(self.__driver, 15)

    def close_driver(self):
        if self.__driver is not None:
            self.__driver.quit()

    def run(self):
        self.initialize_driver()
        self.login()
        self.__read_new_products()
        self.close_driver()


def run_bot():
    bot = KaspiDeleteProducts(PROF_INFO["username"], PROF_INFO["password"])
    bot.run()







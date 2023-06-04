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
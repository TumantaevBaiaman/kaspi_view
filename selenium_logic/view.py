
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def read_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--log-level=3')
    options.add_argument('--proxy-server%s' % url)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options
    )

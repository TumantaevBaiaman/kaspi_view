
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def testing():
    url = "https://kaspi.kz/mc/#/products/ACTIVE/{list}"

    # Инициализация драйвера Selenium (Chrome)
    driver = webdriver.Chrome()

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

    for i in range(1,25):
        url_products = url.format(list=i)

        # Открытие веб-страницы
        driver.get(url_products)

        # Нахождение элемента <div> по его CSS-селектору (пример)
        div_element = driver.find_element_by_css_selector("div.example-class")



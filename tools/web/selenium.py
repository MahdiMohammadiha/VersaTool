from selenium import webdriver
from typing import Literal


# Allowed types for By
ByType = Literal[
    "ID",
    "XPATH",
    "CSS_SELECTOR",
    "NAME",
    "TAG_NAME",
    "CLASS_NAME",
    "LINK_TEXT",
    "PARTIAL_LINK_TEXT",
]

# Allowed names for attribute
AttrName = Literal[
    "class",
    "id",
    "name",
    "value",
    "type",
    "href",
    "src",
    "alt",
    "title",
    "placeholder",
    "disabled",
    "checked",
    "selected",
]


def setup_driver(url: str = "", headless: bool = True, window_size=[1366, 768]):
    """Set up the Selenium WebDriver."""

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    if headless:
        options.add_argument("--headless")
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver

from atexit import register
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
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


class ElementActions:
    def __init__(
        self,
        wait: WebDriverWait,
    ):
        """
        Initialize the toolkit with a WebDriverWait instance.

        Args:
            wait (WebDriverWait): An instance of WebDriverWait.
        """
        self.wait = wait

    def _get_by(
        self,
        by_type: ByType,
    ) -> str:
        if not hasattr(By, by_type):
            raise ValueError(f"Invalid ByType: {by_type}")
        return getattr(By, by_type)

    def click(
        self,
        by_type: ByType,
        locator: str,
    ) -> WebElement:
        """
        Waits until the element is clickable, clicks it, and returns it.

        Args:
            by_type (ByType): Selector type (e.g. "CSS_SELECTOR", "ID").
            locator (str): The selector value.

        Returns:
            WebElement: The clicked element.
        """
        by = self._get_by(by_type)
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()
        return element

    def get_content(
        self,
        by_type: ByType,
        locator: str,
        attr: str = "outerHTML",
    ) -> str:
        """
        Waits for an element to appear and returns the specified attribute.

        Args:
            by_type (ByType): Selector type (e.g. "CSS_SELECTOR").
            locator (str): The selector value.
            attr (str): Attribute name to return (default: "outerHTML").

        Returns:
            str: The attribute value from the element.
        """
        by = self._get_by(by_type)
        element = self.wait.until(EC.presence_of_element_located((by, locator)))
        return element.get_attribute(attr)

    def wait_attr_change(
        self,
        element: WebElement,
        from_value: str,
        to_value: str,
        from_attr: AttrName = "class",
        to_attr: AttrName = "class",
    ) -> None:
        """
        Waits until a specific attribute on an element changes
        from one value to another.

        Args:
            element (WebElement): The element to monitor.
            from_value (str): Value that should disappear from from_attr.
            to_value (str): Value that should appear in to_attr.
            from_attr (AttrName): Attribute to check for `from_value`.
            to_attr (AttrName): Attribute to check for `to_value`.
        """
        self.wait.until(
            lambda _: from_value not in element.get_attribute(from_attr)
            and to_value in element.get_attribute(to_attr)
        )


class BrowserSession:
    def __init__(
        self,
        url: str = "",
        headless: bool = True,
        window_size: list[int] | None = None,
        wait_timeout: float = 10,
    ):
        """
        Initializes the browser session with driver, wait, and eletools.
        The driver will be automatically quit when the program exits.

        Args:
            url (str): The URL to open after initializing the driver. Defaults to an empty string.
            headless (bool): If True, runs the browser in headless mode. Defaults to True.
            window_size (list[int] | None): The window size [width, height] used in headless mode.
                Defaults to [1366, 768] if not provided.
            wait_timeout (float): Timeout for WebDriverWait.
        """
        if window_size is None:
            window_size = [1366, 768]

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        if headless:
            options.add_argument("--headless=new")

        self.driver: WebDriver = webdriver.Chrome(options=options)

        if headless:
            self.driver.set_window_size(*window_size)
        else:
            self.driver.maximize_window()

        if url:
            self.driver.get(url)

        # Register auto-quit at program exit
        register(self.quit)

        self.wait = WebDriverWait(self.driver, wait_timeout)
        self.eletools = ElementActions(self.wait)

    def quit(self):
        """
        Cleanly quit the driver if not already closed.
        """
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

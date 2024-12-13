from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.config import WEBDRIVER_PATH

def initialize_webdriver():
    """
    Initializes and returns a Selenium WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(WEBDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

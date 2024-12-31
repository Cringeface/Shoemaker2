from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_webdriver(headless=True, download_dir=None):
    """
    Initializes and returns a Selenium WebDriver instance for Chrome.
    
    Args:
        headless (bool): Whether to run the browser in headless mode.
        download_dir (str): Path to the directory for file downloads.
    
    Returns:
        webdriver.Chrome: Configured WebDriver instance.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    if download_dir:
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def quit_driver(driver):
    """
    Safely quit the WebDriver.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance to quit.
    """
    if driver:
        driver.quit()

# Example usage
if __name__ == "__main__":
    driver = initialize_webdriver()
    driver.get("https://example.com")
    print("Page Title:", driver.title)
    quit_driver(driver)

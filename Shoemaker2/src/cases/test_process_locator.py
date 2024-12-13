import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def process_locator(driver, locator_number, tax_year):
    try:
        # Execute commands from SIDE file
        driver.get("https://revenue.stlouisco.com/IAS/SearchInput.aspx")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_MainContent_tboxLocatorNum"))
        )
        driver.find_element(By.ID, "ctl00_MainContent_tboxLocatorNum").send_keys(locator_number)
        driver.find_element(By.ID, "ctl00_MainContent_butFind").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(3)"))
        )
        driver.find_element(By.CSS_SELECTOR, "td:nth-child(3)").click()

        # Add logic to retrieve data or handle further steps as needed
        # Placeholder for further processing logic
        time.sleep(2)  # Simulate waiting for data load

        return "Locator processed successfully"

    except TimeoutException as e:
        return f"Timeout occurred: {str(e)}"

    except Exception as e:
        return f"Error during processing: {str(e)}"

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaxDataProcessor:
    def fetch_tax_history(self, driver, locator_number):
        """Extract tax history for a specific locator number."""
        try:
            driver.get("https://revenue.stlouisco.com/IAS/SearchInput.aspx")
            search_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_MainContent_tboxLocatorNum"))
            )
            search_field.send_keys(locator_number)
            driver.find_element(By.ID, "ctl00_MainContent_butFind").click()

            # Navigate to Tax History tab
            driver.find_element(By.CSS_SELECTOR, "td:nth-child(3)").click()
            driver.find_element(By.ID, "ctl00_MainContent_NavLinks1_TaxHistoryLB").click()

            # Ensure Tax History page loads
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".row > .font-weight-bold"))
            )
            return {"locator": locator_number, "status": "Success", "data": "Tax History Extracted"}
        except Exception as e:
            return {"locator": locator_number, "status": "Error", "message": str(e)}

    def fetch_tax_info(self, driver, locator_number):
        """Extract tax info receipt for a specific locator number."""
        try:
            driver.get("https://revenue.stlouisco.com/IAS/SearchInput.aspx")
            search_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_MainContent_tboxLocatorNum"))
            )
            search_field.send_keys(locator_number)
            driver.find_element(By.ID, "ctl00_MainContent_butFind").click()

            # Navigate to Tax Info Receipt tab
            driver.find_element(By.CSS_SELECTOR, "td:nth-child(3)").click()
            driver.find_element(By.ID, "ctl00_MainContent_NavLinks1_TaxDueLB").click()

            # Extract "Total Amount Due"
            total_due = driver.find_element(By.CSS_SELECTOR, ".RevTableTotalsCol").text
            return {"locator": locator_number, "status": "Success", "data": {"total_due": total_due}}
        except Exception as e:
            return {"locator": locator_number, "status": "Error", "message": str(e)}

if __name__ == "__main__":
    from utils.webdriver_manager import WebDriverManager

    driver = WebDriverManager.setup_driver()
    processor = TaxDataProcessor()

    locator_number = "15G430064"
    print("Fetching Tax Info:")
    print(processor.fetch_tax_info(driver, locator_number))

    print("Fetching Tax History:")
    print(processor.fetch_tax_history(driver, locator_number))

    WebDriverManager.teardown_driver(driver)
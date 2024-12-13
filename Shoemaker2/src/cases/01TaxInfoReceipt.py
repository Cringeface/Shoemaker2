# Refactored 01TaxInfoReceipt.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaxInfoReceipt:
    def __init__(self):
        self.driver = None

    def setup(self):
        """Initialize the WebDriver."""
        self.driver = webdriver.Chrome()

    def teardown(self):
        """Quit the WebDriver."""
        if self.driver:
            self.driver.quit()

    def get_tax_info(self, locator_number):
        try:
            # Step 1: Open Real Estate Search page
            self.driver.get("https://revenue.stlouisco.com/IAS/SearchInput.aspx")

            # Step 2: Wait for Locator Number search field
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "ctl00_MainContent_tboxLocatorNum")))

            # Step 3: Enter Locator Number
            self.driver.find_element(By.ID, "ctl00_MainContent_tboxLocatorNum").send_keys(locator_number)

            # Step 4: Click Search
            self.driver.find_element(By.ID, "ctl00_MainContent_butFind").click()

            # Step 5: Handle Positive Search Results
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "td:nth-child(3)"))).click()

            # Step 6: Click on Tax Due Tab
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_MainContent_NavLinks1_TaxDueLB"))).click()

            # Step 7: Retrieve Total Amount Due
            total_due = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".RevTableTotalsCol"))).text

            return {
                "Locator": locator_number,
                "Total Amount Due": total_due,
                "Status": "Processed"
            }
        except Exception as e:
            return {
                "Locator": locator_number,
                "Error": str(e),
                "Status": "Failed"
            }

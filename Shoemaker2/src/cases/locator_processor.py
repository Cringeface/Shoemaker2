import pandas as pd
import time
from cases.search_locator import search_locator
from cases.tax_history import get_tax_history
from cases.tax_info import get_tax_info
# For Selenium locators
from selenium.webdriver.common.by import By

# For logging errors and events
import logging

# For PyQt5 GUI components
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 01TaxInfoReceipt import TaxInfoReceipt

def process_locator(driver, locator_number, tax_year):
    try:
        # Instantiate the TaxInfoReceipt class
        tax_info = TaxInfoReceipt()
        tax_info.setup()

        # Call the get_tax_info method
        result = tax_info.get_tax_info(locator_number)

        # Teardown the WebDriver after processing
        tax_info.teardown()

        return result

    except Exception as e:
        return {
            "Locator": locator_number,
            "Status": "Failed",
            "Error": str(e)
        }

def get_tax_info(driver):
    try:
        owner_name = driver.find_element(By.ID, "ctl00_MainContent_lblOwnerName").text
        address = driver.find_element(By.ID, "ctl00_MainContent_lblAddress").text
        current_tax_due = driver.find_element(By.ID, "ctl00_MainContent_lblCurrentTaxDue").text

        return {
            "Owner Name": owner_name,
            "Address": address,
            "Current Tax Due": current_tax_due
        }
    except Exception as e:
        return {"Error": str(e)}
def process_next_locator(self):
    if self.stop_flag:
        QMessageBox.information(self, "Automation Halted", "The automation was stopped.")
        if self.driver:
            self.driver.quit()
            self.driver = None
        return

    if self.locator_queue.is_empty():
        QMessageBox.information(self, "Queue Complete", "All locators have been processed.")
        if self.driver:
            self.driver.quit()
            self.driver = None
        return

    locator = self.locator_queue.get_next()
    self.queue_viewer.update_status(locator, "Processing")

    try:
        # Attempt to process the locator
        process_locator(self.driver, locator, int(self.single_year_input.text()))
        self.queue_viewer.update_status(locator, "Processed")
        self.locator_queue.mark_processed(locator)
    except Exception as e:
        self.queue_viewer.update_status(locator, f"Failed: {str(e)}")
        self.locator_queue.mark_failed(locator, str(e))
        logging.error(f"Error processing locator {locator}: {e}")

    QTimer.singleShot(1000, self.process_next_locator)

def get_tax_history(driver):
    try:
        tax_history = []
        table = driver.find_element(By.ID, "ctl00_MainContent_RealEstateHistoryData1_tableTaxHistory")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            tax_history.append({
                "Year": cells[0].text,
                "Assessed Value": cells[1].text,
                "Tax Paid": cells[2].text,
                "Payment Date": cells[3].text
            })
        return tax_history
    except Exception as e:
        return {"Error": str(e)}

def save_to_excel(data, filename="output.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

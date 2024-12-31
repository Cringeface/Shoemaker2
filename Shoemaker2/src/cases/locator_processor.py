import pandas as pd
import time
from cases.search_locator import search_locator
# from cases.tax_history import get_tax_history
from cases.taxInfoReceipt import TaxInfoReceipt
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
from .taxInfoReceipt import TaxInfoReceipt

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
        return {"error": str(e), "locator_number": locator_number}

def export_processed_data(data, output_path):
    """
    Exports the processed locator data to an Excel file.

    Args:
        data (list of dict): Processed data for each locator.
        output_path (str): Path to save the exported Excel file.
    """
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, sheet_name="Sheet1")

if __name__ == "__main__":
    locator_queue = ["15G430064", "15G430065", "15G430066"]  # Example locators
    processed_results = []

    for locator in locator_queue:
        result = process_locator(None, locator, 2024)  # Replace None with actual driver instance
        processed_results.append(result)

    output_file = "ProcessedLocators.xlsx"
    export_processed_data(processed_results, output_file)
    print(f"Data exported to {output_file}")

create workflow for processing locators
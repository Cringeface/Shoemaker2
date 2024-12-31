from objects.tax_info_page import TaxInfoPage
from objects.tax_history_page import TaxHistoryPage
from actions.retrieve_tax_data import extract_tax_info, extract_tax_history


class UnifiedTaxProcessor:
    def __init__(self):
        from utils.webdriver_utils import initialize_webdriver, quit_driver
        self.driver = initialize_webdriver()

    def process_locator(self, locator, start_year, end_year):
        """
        Process a single locator number through the tax info and history pages.

        Args:
            locator (str): Locator number to process.
            start_year (int): Start year for filtering data.
            end_year (int): End year for filtering data.

        Returns:
            dict: Processing results.
        """
        try:
            tax_info_page = TaxInfoPage(self.driver)
            tax_history_page = TaxHistoryPage(self.driver)

            # Navigate and extract data
            tax_info = extract_tax_info(tax_info_page, locator)
            tax_history = extract_tax_history(tax_history_page, locator, start_year, end_year)

            return {"locator": locator, "status": "Success", "info": tax_info, "history": tax_history}

        except Exception as e:
            return {"locator": locator, "status": "Error", "error": str(e)}
        finally:
            # Cleanup driver
            from utils.webdriver_utils import quit_driver
            quit_driver(self.driver)

import time

def get_tax_info(driver):
    """
    Retrieves total amount due from the 'Tax Info & Receipt' tab.
    """
    try:
        print("Navigating to 'Tax Info & Receipt' tab...")
        tax_info_tab = driver.find_element("id", "ctl00_MainContent_NavLinks1_TaxDueLB")
        tax_info_tab.click()
        time.sleep(2)

        print("Retrieving 'Total Amount Due'...")
        total_due = driver.find_element("id", "ctl00_MainContent_lblTotalDue").text
        print(f"Total Amount Due: {total_due}")

        return {"Total Amount Due": total_due}
    except Exception as e:
        print(f"Error retrieving tax info: {e}")
        return {"Error": str(e)}

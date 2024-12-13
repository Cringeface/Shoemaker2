import time

def get_tax_history(driver):
    """
    Retrieves tax history from the 'Tax History' tab.
    """
    history = []
    try:
        print("Navigating to 'Tax History' tab...")
        tax_history_tab = driver.find_element("id", "ctl00_MainContent_NavLinks1_TaxHistoryLB")
        tax_history_tab.click()
        time.sleep(2)

        print("Extracting rows from tax history table...")
        rows = driver.find_elements("css selector", "#ctl00_MainContent_RealEstateHistoryData1_tableTaxHistory > tbody > tr")
        for idx, row in enumerate(rows):
            try:
                tax_year = row.find_element("css selector", "th:nth-child(1)").text
                amount_paid = row.find_element("css selector", "th:nth-child(7)").text
                amount_due = row.find_element("css selector", "th:nth-child(6)").text

                history.append({
                    "Tax Year": tax_year,
                    "Amount Paid": amount_paid,
                    "Amount Due": amount_due
                })
                print(f"Row {idx}: Year={tax_year}, Paid={amount_paid}, Due={amount_due}")
            except Exception as row_error:
                print(f"Skipping row {idx} due to error: {row_error}")
                continue

        return history
    except Exception as e:
        print(f"Error retrieving tax history: {e}")
        return {"Error": str(e)}

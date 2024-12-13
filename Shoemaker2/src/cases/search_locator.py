import time

def search_locator(driver, locator_number):
    try:
        print(f"Navigating to search page...")
        driver.get("https://revenue.stlouisco.com/IAS/SearchInput.aspx")

        print(f"Entering locator number: {locator_number}")
        locator_field = driver.find_element("id", "ctl00_MainContent_tboxLocatorNum")
        locator_field.clear()
        locator_field.send_keys(locator_number)

        print("Clicking the search button...")
        search_button = driver.find_element("id", "ctl00_MainContent_butFind")
        search_button.click()
        time.sleep(2)

        print("Clicking the first search result...")
        result_row = driver.find_element("css selector", "td:nth-child(3)")
        result_row.click()
        time.sleep(2)

        print(f"Search for locator {locator_number} completed successfully.")
        return True
    except Exception as e:
        print(f"Error during locator search for {locator_number}: {e}")
        return False

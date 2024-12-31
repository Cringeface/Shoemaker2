# Verify and Action Elements for Shoemaker2

# This file outlines the verification steps and actions associated with each element
# encountered in the workflow. It includes fields, buttons, and actions required
# for successful navigation and data extraction.

# ============================
# Verify Elements
# ============================
verify_elements = {
    "locator_input_page": {
        "description": "Page containing the locator number input field.",
        "type": "page",
        "identifier": {"method": "url", "value": "https://revenue.stlouisco.com/IAS/SearchInput.aspx"},
    },
    "locator_input": {
        "description": "Input field for the locator number.",
        "type": "input",
        "identifier": {"method": "id", "value": "ctl00_MainContent_tboxLocatorNum"},
    },
    "search_button": {
        "description": "Button to execute the locator search.",
        "type": "button",
        "identifier": {"method": "id", "value": "ctl00_MainContent_butFind"},
    },
    "search_result": {
        "description": "Element indicating search results are found.",
        "type": "text",
        "identifier": {"method": "xpath", "value": "//span[contains(.,'1 Record Found')]"},
    },
    "tax_info_tab": {
        "description": "Link to the Tax Info Receipt tab.",
        "type": "link",
        "identifier": {"method": "id", "value": "ctl00_MainContent_NavLinks1_TaxDueLB"},
    },
}

# ============================
# Action Elements
# ============================
action_elements = {
    "navigate_to_locator_page": {
        "description": "Open the locator input page.",
        "action": "navigate",
        "target": "locator_input_page",
    },
    "enter_locator": {
        "description": "Enter the locator number.",
        "action": "send_keys",
        "target": "locator_input",
    },
    "click_search": {
        "description": "Click the search button to start the search.",
        "action": "click",
        "target": "search_button",
    },
    "verify_search_result": {
        "description": "Verify that search results are found.",
        "action": "verify",
        "target": "search_result",
    },
    "open_tax_info_tab": {
        "description": "Click to open the Tax Info Receipt tab.",
        "action": "click",
        "target": "tax_info_tab",
    },
}

# ============================
# Utility Functions
# ============================
def verify_element(driver, element_key):
    """
    Verify the presence of an element on the page.

    Args:
        driver: Selenium WebDriver instance.
        element_key: Key of the element in verify_elements.

    Returns:
        WebElement: The located element if found.
    """
    element_info = verify_elements[element_key]
    method = element_info["identifier"]["method"]
    value = element_info["identifier"]["value"]
    if method == "url":
        assert driver.current_url == value, f"Expected URL: {value}, got {driver.current_url}"
        return True
    return driver.find_element(method, value)

def perform_action(driver, action_key, data=None):
    """
    Perform an action on a specific element.

    Args:
        driver: Selenium WebDriver instance.
        action_key: Key of the action in action_elements.
        data: Optional data to pass (e.g., for send_keys).
    """
    action_info = action_elements[action_key]
    target_key = action_info["target"]
    element = verify_element(driver, target_key)

    if action_info["action"] == "send_keys":
        element.send_keys(data)
    elif action_info["action"] == "click":
        element.click()
    elif action_info["action"] == "verify":
        assert element is not None, f"Element '{target_key}' not found."

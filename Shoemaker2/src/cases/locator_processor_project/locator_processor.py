import subprocess
from bs4 import BeautifulSoup

def process_locator(locator_number):
    """
    Uses curl to fetch data for a given locator number and parses the response.
    """
    url = "https://revenue.stlouisco.com/IAS/SearchResults"
    curl_command = [
        "curl",
        "-X", "POST",
        "-d", f"locatorNumber={locator_number}",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        url
    ]

    try:
        # Execute curl command
        result = subprocess.run(curl_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error executing curl: {result.stderr}")

        # Parse response with BeautifulSoup
        soup = BeautifulSoup(result.stdout, "html.parser")

        # Example parsing - Update selectors based on actual website structure
        tax_year = soup.find("div", {"id": "TaxYear"})
        total_due = soup.find("div", {"id": "TotalAmountDue"})

        return {
            "LocatorNumber": locator_number,
            "TaxYear": tax_year.text if tax_year else "Not Found",
            "TotalAmountDue": total_due.text if total_due else "Not Found"
        }
    except Exception as e:
        return {"LocatorNumber": locator_number, "Error": str(e)}

# For testing
if __name__ == "__main__":
    sample_locator = "15G430011"  # Replace with a test locator
    result = process_locator(sample_locator)
    print(result)

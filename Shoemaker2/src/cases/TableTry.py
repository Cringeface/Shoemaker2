import requests
from bs4 import BeautifulSoup
import csv

# Replace with the actual URL of the webpage
url = "https://revenue.stlouisco.com/Collection/RealEstateHistory.aspx?LocatorNum="

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table using its selector
table = soup.find("table", id="ctl00_MainContent_RealEstateHistoryData1_tableTaxHistory")

# Extract table data
data = []
for row in table.find_all("tr"):
    row_data = [cell.text.strip() for cell in row.find_all("td")]
    data.append(row_data)

# Save data to CSV file
with open("table_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Table data extracted and saved to table_data.csv")
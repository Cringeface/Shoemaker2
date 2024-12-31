# Configuration file for the Shoemaker Tax Data Automation project

# =======================
# File Paths
# =======================
# Path to the input file containing locator numbers
INPUT_FILE_PATH = "./data/input_file.xlsx"

# Path to the output file for processed results
OUTPUT_FILE_PATH = "./data/output.xlsx"

# =======================
# Logging Settings
# =======================
# Path to the log file for application logging
LOG_FILE_PATH = "./logs/shoemaker2.log"

# =======================
# WebDriver Settings
# =======================
# Path to the ChromeDriver executable (replace with the actual path if necessary)
WEBDRIVER_PATH = "./webdrivers/chromedriver"

# Base URL for the St. Louis County Revenue website
BASE_URL = "https://revenue.stlouisco.com/IAS/"

# =======================
# General Settings
# =======================
# Maximum number of retries for failed operations
RETRY_LIMIT = 3

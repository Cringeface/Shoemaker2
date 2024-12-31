import sys
from PyQt5.QtWidgets import QApplication
from orchestrator.gui_orchestrator import CringefaceOrchestrator
from utils.helpers import load_and_preprocess_input
from utils.config import INPUT_FILE_PATH
import logging

# Configure logging
logging.basicConfig(
    filename="workflow.log",  # Log file path
    filemode="a",             # Append to the log file
    level=logging.INFO,       # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def cli_mode():
    """
    Runs the Command-Line Interface (CLI) mode for the application.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Shoemaker Tax Data Automation CLI")
    parser.add_argument("--year", type=int, help="Specify a single tax year (e.g., 2023).")
    parser.add_argument("--year-range", nargs=2, type=int, help="Specify a range of tax years (e.g., 2020 2023).")
    args = parser.parse_args()

    if args.year and args.year_range:
        print("Error: Specify either --year or --year-range, not both.")
        sys.exit(1)

    years_to_process = []
    if args.year:
        years_to_process = [args.year]
    elif args.year_range:
        years_to_process = list(range(args.year_range[0], args.year_range[1] + 1))
    else:
        print("Error: Please specify a year or a range.")
        sys.exit(1)

    print(f"Processing for years: {years_to_process}")

    try:
        locators = load_and_preprocess_input(INPUT_FILE_PATH)
        print(f"Loaded {len(locators)} locators:")
        print(locators["LocatorNumber"].tolist())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def gui_mode():
    """
    Runs the Graphical User Interface (GUI) mode for the application.
    """
    app = QApplication(sys.argv)
    window = CringefaceOrchestrator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Welcome to Shoemaker2. Choose your mode:")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")

    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        cli_mode()
    elif mode == "2":
        gui_mode()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
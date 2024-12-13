from queue import Queue
import pandas as pd

def load_and_preprocess_input(file_path):
    """
    Loads and preprocesses the input Excel file.
    Args:
        file_path (str): Path to the Excel file.
    Returns:
        pd.DataFrame: A DataFrame with cleaned locator numbers.
    Raises:
        ValueError: If the file does not meet requirements.
    """
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)

        # Check if required column exists
        if "LocatorNumber" not in df.columns:
            raise ValueError("The input file must contain a column named 'LocatorNumber'.")

        # Remove duplicates
        df = df.drop_duplicates(subset="LocatorNumber")

        # Ensure all locators are strings
        df["LocatorNumber"] = df["LocatorNumber"].astype(str)

        # Remove invalid locators (e.g., empty strings)
        df = df[df["LocatorNumber"].str.strip() != ""]

        return df

    except FileNotFoundError:
        raise ValueError("The specified file was not found.")
    except Exception as e:
        raise ValueError(f"An error occurred while loading the file: {e}")

class LocatorQueue:
    def __init__(self, locators):
        """
        Initialize the queue with a list of locators.
        """
        self.queue = Queue()
        self.status = {}  # Tracks the status of each locator
        for locator in locators:
            self.queue.put(locator)
            self.status[locator] = "Pending"

    def get_next(self):
        """
        Retrieve the next locator from the queue.
        Returns None if the queue is empty.
        """
        if not self.queue.empty():
            locator = self.queue.get()
            self.status[locator] = "Processing"
            return locator
        return None

    def mark_processed(self, locator):
        """
        Mark a locator as processed.
        """
        self.status[locator] = "Processed"

    def mark_failed(self, locator, error_message=""):
        """
        Mark a locator as failed with an optional error message.
        """
        self.status[locator] = f"Failed: {error_message}"

    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return self.queue.empty()

    def __len__(self):
        """
        Return the number of items remaining in the queue.
        """
        return self.queue.qsize()

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
            raise ValueError("Required column 'LocatorNumber' not found.")

        # Clean locator numbers (e.g., remove duplicates, handle NaNs)
        df = df[["LocatorNumber"]].drop_duplicates().dropna()
        return df

    except Exception as e:
        raise ValueError(f"Error loading input file: {e}")

def validate_year_range(start_year, end_year):
    """
    Validates a year range for logical consistency.

    Args:
        start_year (int): Start year of the range.
        end_year (int): End year of the range.

    Returns:
        bool: True if valid, False otherwise.
    """
    return start_year <= end_year and start_year > 1900

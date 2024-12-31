from processors.unified_tax_processor import UnifiedTaxProcessor


def process_queue(queue, start_year, end_year):
    """
    Process the queue of locator numbers through the unified tax processor.

    Args:
        queue (list): List of locators with reference keys.
        start_year (int): Start of the year range.
        end_year (int): End of the year range.

    Returns:
        list: List of results from the processing.
    """
    processor = UnifiedTaxProcessor()
    results = []

    for entry in queue:
        locator = entry["item"]
        try:
            result = processor.process_locator(locator, start_year, end_year)
            results.append(result)
        except Exception as e:
            results.append({"locator": locator, "status": "Error", "error": str(e)})

    return results

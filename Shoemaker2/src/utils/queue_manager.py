class QueueManager:
    def __init__(self):
        self.queue = []

    def add_item(self, locator, reference_key):
        """
        Add an item to the queue.

        Args:
            locator (str): The locator number or item.
            reference_key (str): Additional reference data.
        """
        self.queue.append({"item": locator, "key": reference_key})

    def get_queue(self):
        """
        Retrieve the current queue.

        Returns:
            list: The current queue as a list of dictionaries.
        """
        return self.queue

    def clear_queue(self):
        """
        Clear all items from the queue.
        """
        self.queue = []


# Example usage
if __name__ == "__main__":
    manager = QueueManager()
    manager.add_item("123456", "KeyABC")
    print(manager.get_queue())
    manager.clear_queue()
    print(manager.get_queue())

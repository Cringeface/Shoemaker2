
import sys
import logging
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QMessageBox, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal  # Added pyqtSignal
from cases.locator_processor import process_locator
from utils.helpers import load_and_preprocess_input, LocatorQueue
from utils.webdriver_setup import initialize_webdriver

class QueueViewer(QDialog):
    def __init__(self, locator_queue):
        super().__init__()
        self.locator_queue = locator_queue
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Queue Viewer")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(len(self.locator_queue))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Locator Number", "Status"])
        layout.addWidget(self.table)

        self.populate_table()
        self.setLayout(layout)

    def populate_table(self):
        locators = list(self.locator_queue.queue.queue)
        for row, locator in enumerate(locators):
            self.table.setItem(row, 0, QTableWidgetItem(str(locator)))
            self.table.setItem(row, 1, QTableWidgetItem("Pending"))

    def update_status(self, locator, status):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == str(locator):
                self.table.setItem(row, 1, QTableWidgetItem(status))
                break

class CringefaceOrchestrator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.locator_queue = None
        self.driver = None
        self.stop_flag = False

    def init_ui(self):
        self.setWindowTitle("Cringeface Orchestrator")
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Cringeface Orchestrator.
Select an input file and define processing years.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        file_layout = QHBoxLayout()
        self.file_button = QPushButton("Select Input File")
        self.file_button.clicked.connect(self.select_file)
        self.file_label = QLabel("No file selected.")
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_label)
        layout.addLayout(file_layout)

        year_layout = QHBoxLayout()
        self.single_year_input = QLineEdit()
        self.single_year_input.setPlaceholderText("Enter single year (e.g., 2023)")
        year_layout.addWidget(self.single_year_input)

        self.range_year_input = QLineEdit()
        self.range_year_input.setPlaceholderText("Enter end year for range (optional)")
        year_layout.addWidget(self.range_year_input)
        layout.addLayout(year_layout)

        self.load_button = QPushButton("Load Queue")
        self.load_button.setEnabled(False)
        self.load_button.clicked.connect(self.load_queue)
        layout.addWidget(self.load_button)

        self.process_button = QPushButton("Start Processing")
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.start_processing)
        layout.addWidget(self.process_button)

        self.panic_button = QPushButton("Panic")
        self.panic_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.panic_button.clicked.connect(self.panic_stop)
        self.panic_button.setEnabled(False)
        layout.addWidget(self.panic_button)

        self.stop_button = QPushButton("Stop Automation")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_processing)
        layout.addWidget(self.stop_button)

        self.export_button = QPushButton("Export Results")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_results)
        layout.addWidget(self.export_button)

        self.clear_button = QPushButton("Clear Queue")
        self.clear_button.clicked.connect(self.clear_queue)
        layout.addWidget(self.clear_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            self.file_label.setText(file_path)
            self.selected_file = file_path
            self.load_button.setEnabled(True)
        else:
            self.file_label.setText("No file selected.")
            self.selected_file = None
            self.load_button.setEnabled(False)
            self.process_button.setEnabled(False)

    def load_queue(self):
        try:
            locators = load_and_preprocess_input(self.selected_file)
            self.locator_queue = LocatorQueue(locators["LocatorNumber"].tolist())
            QMessageBox.information(self, "Queue Loaded", f"Loaded {len(self.locator_queue)} locators into the queue.")
            self.queue_viewer = QueueViewer(self.locator_queue)
            self.queue_viewer.show()
            self.process_button.setEnabled(True)
            self.panic_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load queue: {e}")

    def start_processing(self):
        current_year = self.single_year_input.text()
        range_year = self.range_year_input.text()

        if not current_year:
            QMessageBox.warning(self, "Input Required", "Please enter a current year.")
            return

        if range_year and not range_year.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Range year must be a valid number.")
            return

        self.stop_flag = False
        self.driver = initialize_webdriver()
        self.stop_button.setEnabled(True)
        self.process_next_locator()

    def process_next_locator(self):
        if self.locator_queue.is_empty():
            QMessageBox.information(self, "Queue Complete", "All locators have been processed.")
            self.export_button.setEnabled(True)

            if self.driver:
                self.driver.quit()
                self.driver = None
            return

        locator = self.locator_queue.get_next()
        self.queue_viewer.update_status(locator, "Processing")

        try:
            result = process_locator(self.driver, locator, int(self.single_year_input.text()))
            if result["Status"] == "Processed":
                self.queue_viewer.update_status(locator, "Processed")
                self.locator_queue.mark_processed(locator)
                self.export_button.setEnabled(True)
            else:
                self.queue_viewer.update_status(locator, f"Failed: {result['Error']}")
                self.locator_queue.mark_failed(locator, result["Error"])
        except Exception as e:
            logging.error(f"Unexpected error processing locator {locator}: {e}")
            self.queue_viewer.update_status(locator, f"Failed: {str(e)}")
            self.locator_queue.mark_failed(locator, str(e))

        QTimer.singleShot(1000, self.process_next_locator)

    def panic_stop(self):
        self.stop_flag = True
        QMessageBox.warning(self, "Automation Stopped", "Automation has been stopped by the user.")
        if self.driver:
            self.driver.quit()
            self.driver = None

    def stop_processing(self):
        self.stop_flag = True
        QMessageBox.warning(self, "Automation Stopped", "Automation has been stopped by the user.")
        if self.driver:
            self.driver.quit()
            self.driver = None

    def export_results(self):
        if not self.locator_queue or self.locator_queue.is_empty():
            QMessageBox.warning(self, "No Results", "There are no results to export.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            try:
                processed_data = self.locator_queue.get_all_processed()
                df = pd.DataFrame(processed_data)
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Export Complete", f"Results exported to {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"An error occurred during export: {e}")
                logging.error(f"Export failed: {e}")

    def clear_queue(self):
        if self.locator_queue:
            self.locator_queue.clear()
        self.queue_viewer.close()
        self.locator_queue = None
        self.process_button.setEnabled(False)
        self.panic_button.setEnabled(False)
        QMessageBox.information(self, "Queue Cleared", "The queue has been cleared.")

def main():
    app = QApplication(sys.argv)
    window = CringefaceOrchestrator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

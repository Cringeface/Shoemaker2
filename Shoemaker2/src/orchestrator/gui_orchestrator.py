from PyQt5 import QtWidgets
import sys
from utils.queue_manager import QueueManager
from utils.helpers import load_and_preprocess_input
from utils.logger import setup_logger
from utils.config import OUTPUT_FILE_PATH
import pandas as pd
from datetime import datetime
from processors.unified_tax_processor import UnifiedTaxProcessor

class GUIOrchestrator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger("gui_orchestrator", "gui_orchestrator.log")
        self.queue_manager = QueueManager()  # Initialize the QueueManager
        self.is_paused = False
        self.is_stopped = False
        self.is_panic = False

        # UI Elements
        self.central_widget = None
        self.main_layout = None
        self.input_section = None
        self.input_layout = None
        self.locator_input_label = None
        self.locator_input = None
        self.locator_browse = None
        self.year_section = None
        self.year_layout = None
        self.start_year_label = None
        self.start_year_input = None
        self.end_year_label = None
        self.end_year_input = None
        self.queue_section = None
        self.queue_layout = None
        self.queue_list = None
        self.load_queue_button = None
        self.clear_queue_button = None
        self.progress_section = None
        self.progress_layout = None
        self.progress_bar = None
        self.progress_status = None
        self.error_section = None
        self.error_layout = None
        self.error_log_view = None
        self.control_layout = None
        self.run_button = None
        self.export_button = None
        self.pause_button = None
        self.stop_button = None
        self.cancel_button = None
        self.panic_button = None

        self.init_ui()

    def init_ui(self):
        # Window Properties
        self.setWindowTitle('Shoemaker Tax Data Automation - Orchestrator')
        self.setGeometry(100, 100, 1000, 700)

        # Central Widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Input Section
        self.input_section = QtWidgets.QGroupBox('Input Settings')
        self.input_layout = QtWidgets.QVBoxLayout()
        self.input_section.setLayout(self.input_layout)

        self.locator_input_label = QtWidgets.QLabel('Locator File Path:')
        self.locator_input = QtWidgets.QLineEdit()
        self.locator_browse = QtWidgets.QPushButton('Browse')
        self.locator_browse.clicked.connect(self.browse_file)

        input_row = QtWidgets.QHBoxLayout()
        input_row.addWidget(self.locator_input_label)
        input_row.addWidget(self.locator_input)
        input_row.addWidget(self.locator_browse)

        self.input_layout.addLayout(input_row)

        # Year Selection Section
        self.year_section = QtWidgets.QGroupBox('Tax Year Selection')
        self.year_layout = QtWidgets.QVBoxLayout()
        self.year_section.setLayout(self.year_layout)

        self.start_year_label = QtWidgets.QLabel('Start Year:')
        self.start_year_input = QtWidgets.QSpinBox()
        self.start_year_input.setRange(1900, 2100)
        self.start_year_input.setValue(2023)

        self.end_year_label = QtWidgets.QLabel('End Year:')
        self.end_year_input = QtWidgets.QSpinBox()
        self.end_year_input.setRange(1900, 2100)
        self.end_year_input.setValue(2023)

        year_row = QtWidgets.QHBoxLayout()
        year_row.addWidget(self.start_year_label)
        year_row.addWidget(self.start_year_input)
        year_row.addWidget(self.end_year_label)
        year_row.addWidget(self.end_year_input)

        self.year_layout.addLayout(year_row)

        # Queue Viewer
        self.queue_section = QtWidgets.QGroupBox('Queue Items')
        self.queue_layout = QtWidgets.QVBoxLayout()
        self.queue_section.setLayout(self.queue_layout)

        self.queue_list = QtWidgets.QListWidget()
        self.load_queue_button = QtWidgets.QPushButton('Load Queue')
        self.load_queue_button.clicked.connect(self.load_queue)
        self.clear_queue_button = QtWidgets.QPushButton('Clear Queue')
        self.clear_queue_button.clicked.connect(self.clear_queue)

        queue_control_row = QtWidgets.QHBoxLayout()
        queue_control_row.addWidget(self.load_queue_button)
        queue_control_row.addWidget(self.clear_queue_button)

        self.queue_layout.addWidget(self.queue_list)
        self.queue_layout.addLayout(queue_control_row)

        # Progress Tracker
        self.progress_section = QtWidgets.QGroupBox('Processing Progress')
        self.progress_layout = QtWidgets.QVBoxLayout()
        self.progress_section.setLayout(self.progress_layout)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_status = QtWidgets.QLabel('Status: Ready')

        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_status)

        # Error Log Viewer
        self.error_section = QtWidgets.QGroupBox('Error Log')
        self.error_layout = QtWidgets.QVBoxLayout()
        self.error_section.setLayout(self.error_layout)

        self.error_log_view = QtWidgets.QTextEdit()
        self.error_log_view.setReadOnly(True)

        self.error_layout.addWidget(self.error_log_view)

        # Control Buttons
        self.control_layout = QtWidgets.QHBoxLayout()
        self.run_button = QtWidgets.QPushButton('Run')
        self.run_button.clicked.connect(self.run_processing)
        self.export_button = QtWidgets.QPushButton('Export Results')
        self.export_button.clicked.connect(self.export_results)
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.pause_button.clicked.connect(self.toggle_pause)
        self.stop_button = QtWidgets.QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_processing)
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.panic_button = QtWidgets.QPushButton('PANIC')
        self.panic_button.setStyleSheet('background-color: red; color: white;')
        self.panic_button.clicked.connect(self.trigger_panic)

        self.control_layout.addWidget(self.run_button)
        self.control_layout.addWidget(self.export_button)
        self.control_layout.addWidget(self.pause_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addWidget(self.cancel_button)
        self.control_layout.addWidget(self.panic_button)

        # Add Sections to Main Layout
        self.main_layout.addWidget(self.input_section)
        self.main_layout.addWidget(self.year_section)
        self.main_layout.addWidget(self.queue_section)
        self.main_layout.addWidget(self.progress_section)
        self.main_layout.addWidget(self.error_section)
        self.main_layout.addLayout(self.control_layout)

    def browse_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Locator File', '', 'Excel Files (*.xlsx *.xls);;All Files (*)')
        if file_path:
            self.locator_input.setText(file_path)

    def load_queue(self):
        file_path = self.locator_input.text()
        if not file_path:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please select a locator file before loading the queue.")
            return

        try:
            # Use helper to load and preprocess the file
            data = load_and_preprocess_input(file_path)

            self.queue_manager.clear_queue()
            self.queue_list.clear()
            current_date = datetime.now().strftime("%d%b%y").upper()

            for locator in data["LocatorNumber"]:
                reference_key = f"{locator}-{current_date}"
                self.queue_manager.add_item(locator, reference_key)
                self.queue_list.addItem(f"{locator} - Key: {reference_key}")

            QtWidgets.QMessageBox.information(self, "Queue Loaded", "Queue loaded successfully.")

        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "File Error", str(e))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load queue: {e}")

    def clear_queue(self):
        self.queue_manager.clear_queue()
        self.queue_list.clear()
        QtWidgets.QMessageBox.information(self, "Queue Cleared", "Queue cleared successfully.")

    def toggle_pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.progress_status.setText('Status: Paused')
            self.pause_button.setText('Resume')
        else:
            self.is_paused = False
            self.progress_status.setText('Status: Processing...')
            self.pause_button.setText('Pause')

    def stop_processing(self):
        self.is_stopped = True
        self.progress_status.setText('Status: Stopped')
        self.progress_bar.setValue(0)

    def trigger_panic(self):
        self.is_panic = True
        self.is_stopped = True
        self.logger.error("Panic button pressed by user. Automation halted.")
        self.progress_status.setText('Status: PANIC - Automation Halted')
        QtWidgets.QMessageBox.critical(self, "PANIC", "Automation halted immediately by user panic!")

    def run_processing(self):
        self.is_stopped = False
        self.is_paused = False
        self.is_panic = False
        self.progress_status.setText('Status: Processing...')
        queue = self.queue_manager.get_queue()
        total_items = len(queue)

        if total_items == 0:
            QtWidgets.QMessageBox.warning(self, "Queue Empty", "No items to process. Please load a queue first.")
            return

        processor = UnifiedTaxProcessor()
        results = []

        try:
            for index, entry in enumerate(queue):
                if self.is_stopped or self.is_panic:
                    break
                while self.is_paused:
                    QtWidgets.QApplication.processEvents()
                locator = entry["item"]

                # Process locator number
                result = processor.process_locator(locator)
                results.append(result)

                if result["status"] == "Success":
                    self.logger.info(f"{locator} - Success: {result['info']}, {result['history']}")
                else:
                    self.logger.error(f"{locator} - Errors: {', '.join(result['errors'])}")

                # Update progress bar
                self.progress_bar.setValue(int((index + 1) / total_items * 100))

            self.export_results_to_excel(results)

            if not self.is_stopped and not self.is_panic:
                self.progress_status.setText('Status: Completed')
                QtWidgets.QMessageBox.information(self, "Processing Complete", "All items have been processed.")
        except Exception as e:
            self.progress_status.setText('Status: Error')
            self.logger.exception("An error occurred during processing.")
            QtWidgets.QMessageBox.critical(self, "Processing Error", f"An error occurred: {e}")

    def export_results_to_excel(self, results):
        """Export the processing results to an Excel file."""
        try:
            df = pd.DataFrame(results)
            df.to_excel(OUTPUT_FILE_PATH, index=False)
            self.logger.info(f"Results exported to {OUTPUT_FILE_PATH}")
            self.error_log_view.append(f"Results exported to {OUTPUT_FILE_PATH}")
        except Exception as e:
            self.logger.error(f"Error exporting results: {str(e)}")
            self.error_log_view.append(f"Error exporting results: {str(e)}")

    def export_results(self):
        self.export_results_to_excel([])

    def cancel_processing(self):
        self.progress_status.setText('Status: Cancelled')
        # Placeholder for cancellation logic
        self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUIOrchestrator()
    gui.show()
    sys.exit(app.exec_())

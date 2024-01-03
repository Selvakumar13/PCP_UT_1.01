import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QFont

import win32print
import pywintypes
import win32con

class PrinterValidationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PCP_Utility")
        self.setGeometry(30, 50, 300, 100)
        self.setWindowIcon(QIcon("printer.jpeg"))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.printer_label = QLabel("Enter Printer Name:")
        self.printer_input = QLineEdit(self)

        self.validate_button = QPushButton("Validate", self)
        self.validate_button.clicked.connect(self.validate_printer)

        layout.addWidget(self.printer_label)
        layout.addWidget(self.printer_input)
        layout.addWidget(self.validate_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("background-color: #f5f5f5;")

    def validate_printer(self):
        input_printer_name = self.printer_input.text()

        if self.is_printer_connected(input_printer_name):
            printer_info = self.get_printer_info(input_printer_name)
            self.show_printer_info(printer_info)
        else:
            self.show_message_box("Validation Failed", f"No printer with the name '{input_printer_name}' is connected.")

    def is_printer_connected(self, printer_name):
        # In this example, we assume that the printer is connected if its name is not empty
        # You can replace this with actual printer detection logic if needed
        return bool(printer_name)

    def get_printer_info(self, printer_name):
        printer_type = self.check_printer_type(printer_name)  # Get printer type
        trays = get_number_of_trays(printer_name)
        status = get_printer_status(printer_name)
        toner_status = toner_information(printer_name)
        properties = printer_properties(win32print.GetPrinter(win32print.OpenPrinter(printer_name), 2))

        info_text = f"Printer Type: {printer_type}\n"
        info_text += f"Printer Name: {properties[0]}\nLocation: {properties[2]}\nPort Name: {properties[3]}\nNumber of Jobs: {properties[4]}\n\n"
        info_text += f"Number of Trays: {len(trays)}\n"
        info_text += f"{status}\n\n"
        info_text += f"Toner Levels: {toner_status}"

        return info_text

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setFont(QFont("Arial", 12))
        msg_box.exec()

    def show_printer_info(self, printer_info):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Printer Information")
        msg_box.setText(printer_info)
        msg_box.setFont(QFont("Arial", 9))
        msg_box.exec()

    def check_printer_type(self, printer_name):
        attributes = win32print.GetPrinter(win32print.OpenPrinter(printer_name), 2)['Attributes']
        printer_type_map = {
            win32print.PRINTER_ATTRIBUTE_LOCAL: "Local printer",
            win32print.PRINTER_ATTRIBUTE_NETWORK: "Network printer",
            win32print.PRINTER_ATTRIBUTE_DIRECT: "Direct printing"
        }

        for attribute, printer_type in printer_type_map.items():
            if attributes & attribute:
                return printer_type

        return "Unknown printer type"

def get_number_of_trays(printer_name):
    try:
        name_trays = win32print.DeviceCapabilities(printer_name, "", win32con.DC_BINNAMES)
        trays = [i for i in name_trays if i.startswith('Tray')]
        return trays if trays else ["No trays available"]
    except pywintypes.error:
        return ["Unavailable"]

def get_printer_status(printer_name):
    status = win32print.GetPrinter(win32print.OpenPrinter(printer_name))[18]
    status_map = {
        win32print.PRINTER_STATUS_PAUSED: "Printer is paused",
        win32print.PRINTER_STATUS_ERROR: "Printer status: Error",
        win32print.PRINTER_STATUS_PENDING_DELETION: "Printer is pending deletion",
        win32print.PRINTER_STATUS_PAPER_JAM: "Printer status: Paper Jam",
        win32print.PRINTER_STATUS_PAPER_OUT: "Printer status: Out of Paper",
        win32print.PRINTER_STATUS_MANUAL_FEED: "Printer is waiting for manual feed",
        win32print.PRINTER_STATUS_OFFLINE: "Printer status: Offline",
        win32print.PRINTER_STATUS_BUSY: "Printer is busy",
        win32print.JOB_STATUS_USER_INTERVENTION: "Printer status: User Intervention Required"
    }
    return status_map.get(status, "Printer status: Ready!")

def toner_information(printer_name):
    status = win32print.GetPrinter(win32print.OpenPrinter(printer_name))[18]
    toner_status_map = {
        win32print.PRINTER_STATUS_TONER_LOW: "Printer status: Low Toner",
        win32print.PRINTER_STATUS_NO_TONER: "Printer status: No Toner"
    }
    return toner_status_map.get(status, "Adequate Levels of Toner Present")

def printer_properties(printer_info):
    return (
        printer_info['pPrinterName'],
        printer_info['pDriverName'],
        printer_info['pLocation'],
        printer_info['pPortName'],
        printer_info['cJobs'],
        printer_info['Attributes']
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrinterValidationApp()
    window.show()
    sys.exit(app.exec())

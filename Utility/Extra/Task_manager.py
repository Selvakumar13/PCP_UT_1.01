import sys
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QIcon, QFont

class SoftwareCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Software Checker")
        self.setGeometry(100, 100, 300, 100)
        self.setWindowIcon(QIcon("printer.jpeg"))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.input_label = QLabel("Enter software name:")
        self.input_text = QLineEdit()
        self.check_button = QPushButton("Check")

        self.check_button.clicked.connect(self.check_process)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.check_button)

        self.central_widget.setLayout(layout)

        self.show()

    def check_process(self):
        software_name = self.input_text.text()

        found = False
        for process in psutil.process_iter(['pid', 'name']):
            if software_name.lower() in process.info['name'].lower():
                found = True
                break

        if found:
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Information)
            message_box.setWindowTitle("Result")
            message_box.setText(f"{software_name} is running!")
            message_box.exec()
        else:
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Result")
            message_box.setText(f"{software_name} is not running.")
            message_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SoftwareCheckerApp()
    sys.exit(app.exec())

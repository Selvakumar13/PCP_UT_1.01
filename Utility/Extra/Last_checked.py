import sys
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QTimer, QDateTime,QByteArray
from PySide6.QtGui import QPixmap,QIcon

class SoftwareCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_software)
        self.timer.start(3000)  # 3,000 milliseconds (3 seconds) for testing

    def init_ui(self):
        self.setWindowTitle("Software Checker")
        self.setGeometry(330, 120, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Labels for "Last checked" and "Status"
        last_checked_label = QLabel("Last checked:", self)
        status_label = QLabel("Status:", self)


        # Labels to display the time and status
        self.last_checked_text = QLabel("", self)
        self.status_text = QLabel("", self)

        # Set a background color for the labels
        last_checked_label.setStyleSheet("background-color: #f5f5f5;")
        status_label.setStyleSheet("background-color: #f5f5f5;")
        self.last_checked_text.setStyleSheet("background-color: white; width: 20px; height: 10px;")
        self.status_text.setStyleSheet("background-color: white; width: 20px; height: 10px;")

        layout.addWidget(last_checked_label)
        layout.addWidget(self.last_checked_text)
        layout.addWidget(status_label)
        layout.addWidget(self.status_text)

        base64_image = b"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"

        # Converting base64 string to QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(base64_image))

        self.setWindowIcon(QIcon(pixmap))
        self.setStyleSheet("""
                                 QMainWindow {
                                     background-color:#f5f5f5; /* White background */
                                 }
                                 QLabel {
                                     color: #333333; /* Black text */
                                     font-size: 12px; /* Slightly smaller font */
                                 }
                                 QPushButton {
                                     background-color: #0d6efd; /* Dark Blue button */
                                     color: white;
                                     border: none;
                                     padding: 6px 12px;
                                     border-radius: 3px;
                                     width: 150px; 
                                 }
                                 QPushButton:hover {
                                     background-color: #0951ba; /* Slightly darker grey on hover */
                                 }
                             """)

        self.central_widget.setLayout(layout)

    def check_software(self):
        software_name = "PCP_2.0.6"

        found = False
        for process in psutil.process_iter(['pid', 'name']):
            if software_name.lower() in process.info['name'].lower():
                found = True
                status = "Working"
                break
            else:
                status = "Not Working"

        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        # Update the time and status labels
        self.last_checked_text.setText(current_time)
        self.status_text.setText(status)

def main():
    app = QApplication(sys.argv)
    window = SoftwareCheckerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
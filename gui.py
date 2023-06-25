import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QMessageBox, QStyleFactory, QStatusBar
)
from extract_data import process_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solana ETL")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        label = QLabel("Click the button to start data extraction:")
        layout.addWidget(label)

        button = QPushButton("Extract Data", self)
        button.clicked.connect(self.start_extraction)
        layout.addWidget(button)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

    def start_extraction(self):
        try:
            process_data()
            QMessageBox.information(self, "Extraction Completed", "Data extraction process completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during data extraction:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application style
    app.setStyle(QStyleFactory.create('Fusion'))

    # Load a custom stylesheet for theming
    app.setStyleSheet(open('styles.qss').read())

    window = MainWindow()

    # Center the window on the screen
    window.setGeometry(
        app.desktop().screen().rect().center().x() - window.width() // 2,
        app.desktop().screen().rect().center().y() - window.height() // 2,
        window.width(),
        window.height()
    )

    # Set application icon
    window.setWindowIcon(app.style().standardIcon(QStyleFactory.SP_DialogApplyButton))

    # Set the status bar message
    window.statusBar().showMessage("Ready")

    window.show()
    sys.exit(app.exec_())

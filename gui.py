import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QMessageBox, QStyleFactory, QStatusBar, QInputDialog, QDialog
)
from PyQt5.QtCore import QTranslator
from extract_data import process_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solana ETL")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        label = QLabel(self.tr("Click the button to start data extraction:"))
        layout.addWidget(label)

        button = QPushButton(self.tr("Extract Data"), self)
        button.clicked.connect(self.start_extraction)
        layout.addWidget(button)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

    def start_extraction(self):
        try:
            process_data()
            QMessageBox.information(self, self.tr("Extraction Completed"), self.tr("Data extraction process completed successfully."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr(f"An error occurred during data extraction:\n{str(e)}"))

    def show_feedback_dialog(self):
        feedback, ok = QInputDialog.getText(self, self.tr("Feedback"), self.tr("Please provide your feedback:"))
        if ok:
            QMessageBox.information(self, self.tr("Thank You"), self.tr("Thank you for your feedback!"))

    def show_onboarding_dialog(self):
        onboarding_dialog = QDialog(self)
        onboarding_dialog.setWindowTitle(self.tr("Onboarding"))

        # Add onboarding content to the dialog
        layout = QVBoxLayout(onboarding_dialog)
        label = QLabel(self.tr("Welcome to Solana ETL!"))
        layout.addWidget(label)

        onboarding_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application style
    app.setStyle(QStyleFactory.create('Fusion'))

    # Load a custom stylesheet for theming
    app.setStyleSheet(open('styles.qss').read())

    # Initialize the translator
    translator = QTranslator()
    translator.load("translations.qm")  # Load the translation file
    app.installTranslator(translator)

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
    window.statusBar().showMessage(window.tr("Ready"))

    # Show feedback dialog
    window.show_feedback_dialog()

    # Show onboarding dialog
    window.show_onboarding_dialog()

    window.show()
    sys.exit(app.exec_())

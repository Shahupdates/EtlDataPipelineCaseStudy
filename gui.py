import sys
import asyncio
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QProgressBar,
    QMessageBox, QStyleFactory, QStatusBar, QInputDialog, QDialog, QToolBar, QAction, QMenu
)
from PyQt5.QtCore import QMetaObject, Q_ARG, Qt, QTranslator
from PyQt5.QtGui import QIcon
from extract_data import process_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solana ETL")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        label = QLabel(self.tr("Click the button to start data extraction:"))
        layout.addWidget(label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        button = QPushButton(self.tr("Extract Data"), self)
        button.clicked.connect(self.start_extraction)
        layout.addWidget(button)

        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Create a toolbar
        self.init_toolbar()

        # Create a menu
        self.init_menu()

    def init_toolbar(self):
        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(QIcon("logo.png"), "Home", self.home)
        self.toolbar.addAction(QIcon("logo.png"), "Settings", self.show_settings_dialog)

    def init_menu(self):
        self.menu = self.menuBar()
        self.help_menu = self.menu.addMenu('Help')

        self.about_action = QAction(QIcon("logo.png"), 'About', self)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)

    def start_extraction(self):
        try:
            asyncio.create_task(self.run_extraction())
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr(f"An error occurred during data extraction:\n{str(e)}"))

    async def run_extraction(self):
        # Assuming process_data() now yields progress updates
        async for progress_percentage in process_data():
            # Update the progress bar
            # You must wrap GUI updates with QMetaObject.invokeMethod when using threads
            QMetaObject.invokeMethod(self.progress_bar, "setValue", Qt.QueuedConnection,
                                     Q_ARG(int, progress_percentage))
        QMetaObject.invokeMethod(QMessageBox, "information", Qt.QueuedConnection,
                                 Q_ARG(str, self.tr("Extraction Completed")),
                                 Q_ARG(str, self.tr("Data extraction process completed successfully.")))

    def show_about_dialog(self):
        QMessageBox.about(self, "About Solana ETL", "<p>This is an ETL (Extract, Transform, Load) tool for Solana data.<br>"
                                                      "<b>Developer:</b> Your Name<br>"
                                                      "<b>Version:</b> 1.0</p>")

    def show_settings_dialog(self):
        settings, ok = QInputDialog.getText(self, "Settings", "Enter your settings:")
        if ok:
            QMessageBox.information(self, "Settings", "Settings updated.")

    def home(self):
        QMessageBox.information(self, "Home", "You are at the Home page.")

    def show_feedback_dialog(self):
        feedback, ok = QInputDialog.getText(self, self.tr("Feedback"), self.tr("Please provide your feedback:"))
        if ok:
            QMessageBox.information(self, self.tr("Thank You"), self.tr("Thank you for your feedback!"))

    def show_onboarding_dialog(self):
        self.onboarding_dialog = QDialog(self)
        self.onboarding_dialog.setWindowTitle(self.tr("Onboarding"))

        # Add onboarding content to the dialog
        layout = QVBoxLayout(self.onboarding_dialog)
        label = QLabel(self.tr("Welcome to Solana ETL!"))
        layout.addWidget(label)

        self.onboarding_dialog.show()

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
    window.setWindowIcon(QIcon('logo.png'))  # Set your logo

    # Set the status bar message
    window.statusBar().showMessage(window.tr("Ready"))

    # Show feedback dialog
    window.show_feedback_dialog()

    # Show onboarding dialog
    window.show_onboarding_dialog()

    window.show()
    sys.exit(app.exec_())

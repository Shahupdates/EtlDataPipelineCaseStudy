import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QProgressBar,
    QMessageBox, QStyleFactory, QStatusBar, QInputDialog, QDialog, QToolBar, QAction, QMenu
)
from PyQt5.QtCore import Qt, QTranslator, pyqtSignal
from PyQt5.QtGui import QIcon
import asyncqt
import asyncio
from extract_data import get_latest_blockhash, get_block, load_data, run_dbt_transformation, calculate_dau, calculate_daily_transaction_volume

class Worker(asyncio.Task):
    progress_signal = pyqtSignal(int)
    complete_signal = pyqtSignal()

    async def run(self):
        latest_block = get_latest_blockhash()
        if latest_block is not None:
            transactions, _ = await get_block(latest_block)
            if transactions is not None:
                deduplicated_df = load_data(transactions)
                calculate_dau(deduplicated_df)
                calculate_daily_transaction_volume(deduplicated_df)
                run_dbt_transformation()
        self.complete_signal.emit()


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
        self.toolbar.addAction(QIcon("logo2.png"), "Settings", self.show_settings_dialog)

    def init_menu(self):
        self.menu = self.menuBar()
        self.help_menu = self.menu.addMenu('Help')

        self.about_action = QAction(QIcon("logo.png"), 'About', self)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)

    def start_extraction(self):
        self.worker = Worker()
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.complete_signal.connect(self.extraction_completed)
        asyncio.ensure_future(self.worker.run())

    def extraction_completed(self):
        QMessageBox.information(self, self.tr("Extraction Completed"),
                                self.tr("Data extraction process completed successfully."))

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
        onboarding_dialog = QDialog(self)
        onboarding_dialog.setWindowTitle(self.tr("Onboarding"))

        # Add onboarding content to the dialog
        layout = QVBoxLayout(onboarding_dialog)
        label = QLabel(self.tr("Welcome to Solana ETL!"))
        layout.addWidget(label)

        onboarding_dialog.exec_()


async def main():
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

    asyncio.ensure_future(app.exec_())

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    asyncio.run(main())
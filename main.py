import sys

from PySide6.QtWidgets import QApplication
from Ui_MainWindow import Ui_MainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Ui_MainWindow(app)
    window.show()

    app.exec()
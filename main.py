import sys, os

from PySide6.QtWidgets import QApplication
from Ui_MainWindow import Ui_MainWindow

from pathlib import Path

if __name__ == "__main__":

    if os.path.exists("source.png"):
        os.remove("source.png")

    if os.path.exists("pixelart.png"):
        os.remove("pixelart.png")

    app = QApplication(sys.argv)

    app.setStyleSheet(Path('style.qss').read_text())

    window = Ui_MainWindow(app)

    window.show()

    app.exec()
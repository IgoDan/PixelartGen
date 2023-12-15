import sys, os

from PySide6.QtWidgets import QApplication
from Ui_MainWindow import Ui_MainWindow

if __name__ == "__main__":

    if os.path.exists("source.png"):
        os.remove("source.png")

    if os.path.exists("pixelart.png"):
        os.remove("pixelart.png")

    app = QApplication(sys.argv)

    window = Ui_MainWindow(app)

    window.show()

    app.exec()
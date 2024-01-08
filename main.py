import sys, os

from PySide6.QtWidgets import QApplication
from Ui_MainWindow import Ui_MainWindow

#ABSOLUTE PATH FOR PYINSTALLER
def resource_path(relative_path):

    try:
        #PYINSTALLER STORES PATH IN _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def windows_to_unix_path(windows_path):

    unix_path = windows_path.replace('\\', '/')
    unix_path = 'file:///' + unix_path[2:]

    return unix_path

if __name__ == "__main__":

    if os.path.exists("source.png"):
        os.remove("source.png")

    if os.path.exists("pixelart.png"):
        os.remove("pixelart.png")

    app = QApplication(sys.argv)

    style_file = resource_path("style.qss")

    path = windows_to_unix_path(style_file)

    print(path)

    app.setStyleSheet(path)

    window = Ui_MainWindow(app)

    window.show()

    app.exec()
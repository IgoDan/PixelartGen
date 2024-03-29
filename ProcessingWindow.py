from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class ProcessingWindow(QDialog):

    def __init__(self, parent = None):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("...")
        self.setFixedSize(140, 70)
        self.setWindowFlags(Qt.WindowType.SplashScreen)

        layout = QVBoxLayout(self)

        self.label = QLabel("Przetwarzanie...", self)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

    def center(self):

        parent_center = self.parent().geometry().center()

        dialog_rect = self.geometry()
        dialog_rect.moveCenter(parent_center)
        self.setGeometry(dialog_rect)
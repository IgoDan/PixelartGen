from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QLabel
from PySide6.QtCore import Qt


class ProcessingWindow(QDialog):

    def __init__(self, parent = None):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("...")
        self.setFixedSize(140, 70)
        layout = QVBoxLayout(self)
        self.label = QLabel("Przetwarzanie...", self)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setWindowFlags(Qt.WindowType.SplashScreen)

    def center(self):

        parent_rect = self.parent().geometry()
        parent_center = parent_rect.center()

        dialog_rect = self.geometry()
        dialog_rect.moveCenter(parent_center)
        self.setGeometry(dialog_rect)
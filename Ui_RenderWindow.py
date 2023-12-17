from PySide6.QtWidgets import QDialog

class Ui_RenderWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("Renderowanie")
        self.setFixedSize(1024, 768)

        parent_rect = self.parent().geometry()
        parent_center = parent_rect.center()

        dialog_rect = self.geometry()
        dialog_rect.moveCenter(parent_center)
        self.setGeometry(dialog_rect)
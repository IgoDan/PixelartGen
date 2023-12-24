from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import QSize

class ColorPalette(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        # COLOR PALETTE LAYOUT
        self.color_palette_layout = QHBoxLayout(self)
        self.color_palette_layout.setContentsMargins(0, 10, 0, 0)
        self.color_palette_layout.setSpacing(0)

        self.add_palette_buttons(self.color_palette_layout)

        self.setLayout(self.color_palette_layout)

    def add_palette_buttons(self, layout):

        for color in self.parent().palette_from_image:

            color_button = QPushButton()
            color_button.setFixedSize(QSize(40, 40))
            color_button.color = color
            color_button.setStyleSheet("background-color: rgb(%d, %d, %d);" % color)

            color_button.pressed.connect(lambda c = color: self.set_pen_color(c))

            layout.addWidget(color_button)

    def set_pen_color(self, color):

        self.parent().set_pen_color(color)
        print("Selected color:", color)
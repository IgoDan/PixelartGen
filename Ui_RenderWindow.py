from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QDialog, QVBoxLayout, QPushButton, QColorDialog
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

from GraphicsView import GraphicsView

import os

class Ui_RenderWindow(QDialog):
    def __init__(self, parent):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("Render Window")
        self.setFixedSize(1024, 768)

        #IMAGE OPEN
        self.image = QImage(os.path.join(os.getcwd(), "pixelart.png"))

        #VIEW
        self.view = GraphicsView(self)
        self.view.setSceneRect(0, 0, self.image.width(), self.image.height())

        #SCENE
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        #CREATE PIXMAP
        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

        #PALETTE
        self.palette_button = QPushButton("Wybierz kolor", self)
        self.palette_button.setGeometry(80, 640, 350, 40)
        self.palette_button.clicked.connect(self.show_color_dialog)
        self.selected_color = Qt.black

        #EXPORT BUTTON
        self.export_button = QPushButton("Eksportuj", self)
        self.export_button.setGeometry(80, 660, 350, 40)
        self.export_button.clicked.connect(self.export_image)

        # UI LAYOUT
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.palette_button)
        layout.addWidget(self.export_button)

        self.view.mousePressEvent = self.mouse_press_event
        self.view.mouseMoveEvent = self.mouse_move_event

    def show_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print("Wybrany kolor:", color.name())
            self.selected_color = color

    def draw_line(self, x1, y1, x2, y2):
        painter = QPainter(self.image)
        painter.setPen(self.selected_color)
        painter.drawLine(x1, y1, x2, y2)
        painter.end()

        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            self.last_x, self.last_y = x, y

    def mouse_move_event(self, event):
        if event.buttons() & Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            self.draw_line(self.last_x, self.last_y, x, y)
            self.last_x, self.last_y = x, y

    def export_image(self):
        # Tutaj możesz dodać kod do zapisywania obrazu na dysku
        print("Exporting image...")

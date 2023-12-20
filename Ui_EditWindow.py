import os

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QDialog, QVBoxLayout, QPushButton, QColorDialog
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

from GraphicsView import GraphicsView

class Ui_EditWindow(QDialog):
    def __init__(self, parent):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("Render Window")
        self.setFixedSize(1024, 768)

        #IMAGE OPEN
        self.image = QImage(os.path.join(os.getcwd(), "pixelart.png"))

        #PIXMAP
        self.pixmap = QPixmap.fromImage(self.image)

        #SCENE
        self.scene = QGraphicsScene(self)

        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

        #VIEW
        self.view = GraphicsView(self)
        self.view.setSceneRect(0, 0, self.image.width(), self.image.height())

        self.view.setScene(self.scene)

        #COLOR PICKER BUTTON
        self.button_color_select = QPushButton("Wybierz kolor", self)
        self.button_color_select.setGeometry(80, 640, 350, 40)
        self.button_color_select.clicked.connect(self.show_color_dialog)
        self.selected_color = Qt.black

        #EXPORT BUTTON
        self.button_export = QPushButton("Eksportuj", self)
        self.button_export.setGeometry(80, 660, 350, 40)
        self.button_export.clicked.connect(self.export_image)

        #UI LAYOUT
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button_color_select)
        layout.addWidget(self.button_export)

        #EVENTS
        self.view.mousePressEvent = self.event_mouse_press
        self.view.mouseMoveEvent = self.event_mouse_move

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

    def event_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            self.last_x, self.last_y = x, y

    def event_mouse_move(self, event):
        if event.buttons() & Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            self.draw_line(self.last_x, self.last_y, x, y)
            self.last_x, self.last_y = x, y

    def export_image(self):
        #TODO
        
        print("Exporting image...")

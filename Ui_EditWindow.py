import os

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QDialog, QVBoxLayout, QPushButton, QColorDialog, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QRect, QSize, QRectF

from GraphicsView import GraphicsView

class ScalableColorPalette(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        # COLOR PALETTE LAYOUT
        self.color_palette_layout = QHBoxLayout(self)
        self.add_palette_buttons(self.color_palette_layout)

        self.setLayout(self.color_palette_layout)

    def add_palette_buttons(self, layout):

        for color in self.parent().palette_from_image:

            color_button = QPushButton()
            color_button.setFixedSize(QSize(40, 35))
            color_button.color = color
            color_button.setStyleSheet("background-color: rgb(%d, %d, %d);" % color)

            #size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            #color_button.setSizePolicy(size_policy)

            color_button.pressed.connect(lambda c = color: self.set_pen_color(c))

            layout.addWidget(color_button)

    def set_pen_color(self, color):

        self.parent().set_pen_color(color)
        print("Selected color:", color)

class Ui_EditWindow(QDialog):
    def __init__(self, parent, palette):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("Render Window")
        self.setFixedSize(1024, 768)

        self.palette_from_image = palette

        self.is_erase_mode = False

        #IMAGE OPEN
        self.image = QImage(os.path.join(os.getcwd(), "pixelart.png"))
        self.original_image = self.image.copy()

        if max(self.image.width(), self.image.height()) == self.image.width():
            self.initial_zoom = (1024*0.7 / max(self.image.width(), self.image.height()))
        else:
            self.initial_zoom = (768*0.7 / max(self.image.width(), self.image.height()))

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

        self.button_color_select.clicked.connect(self.show_color_dialog)
        self.selected_color = Qt.black
        self.button_color_select.setFixedSize(QSize(120, 40))

        # COLOR PALETTE WIDGET
        self.color_palette_widget = ScalableColorPalette(self)
        self.color_palette_widget.show()

        #EXPORT BUTTON
        self.button_export = QPushButton("Eksportuj", self)
        self.button_export.clicked.connect(self.export_image)
        self.button_export.setFixedSize(QSize(120, 40))

        #LAYOUTS
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_color_select)
        buttons_layout.addWidget(self.button_export)

        palette_layout = QHBoxLayout()
        palette_layout.addWidget(self.color_palette_widget)

        #WINDOW LAYOUT
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addLayout(palette_layout)
        layout.addLayout(buttons_layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(layout)

        #EVENTS
        self.view.mousePressEvent = self.event_mouse_press
        self.view.mouseMoveEvent = self.event_mouse_move
        self.view.mouseReleaseEvent = self.event_mouse_release

    def set_pen_color(self, color):

        if isinstance(color, tuple):
            self.selected_color = QColor(*color)

        else:
            self.selected_color = color

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

    def erase_line(self, x1, y1, x2, y2):
        painter = QPainter(self.image)
        painter.setPen(QColor(self.original_image.pixel(x1, y1)))
        painter.drawLine(x1, y1, x2, y2)
        painter.end()

        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

    def event_mouse_press(self, event):
        if event.buttons() & (Qt.LeftButton | Qt.RightButton):
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            self.last_x, self.last_y = x, y
            if event.button() == Qt.LeftButton and not self.is_erase_mode:
                self.draw_line(x, y, x, y)
            elif event.button() == Qt.RightButton:
                self.is_erase_mode = True
                self.erase_line(x, y, x, y)

    def event_mouse_move(self, event):
        if event.buttons() & (Qt.LeftButton | Qt.RightButton):
            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())
            if not self.is_erase_mode:
                self.draw_line(self.last_x, self.last_y, x, y)
            else:
                self.erase_line(x, y, x, y)
            self.last_x, self.last_y = x, y

    def event_mouse_release(self, event):
        if event.button() == Qt.RightButton:
            self.is_erase_mode = False

    def export_image(self):
        #TODO
        
        print("Exporting image...")

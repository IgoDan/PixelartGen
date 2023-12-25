import os, cv2

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QDialog, QVBoxLayout, QPushButton, QColorDialog, QHBoxLayout, QSizePolicy, QLabel, QFileDialog
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QSize

from GraphicsView import GraphicsView
from ColorPalette import ColorPalette
from Slider import Slider
from ExportDialog import ExportDialog

class Ui_EditWindow(QDialog):

    def __init__(self, parent, palette):

        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle("Pixelart Gen - Edit Window")
        self.setFixedSize(1024, 768)

        self.palette_from_image = palette
        self.is_erase_mode = False
        self.selected_color = QColor(0,0,0,255)
        self.pen = QPen()

        self.previous_x = -1
        self.previous_y = -1

        #IMAGE OPEN
        self.image = QImage(os.path.join(os.getcwd(), "pixelart.png"))
        self.original_image = self.image.copy()

        if max(self.image.width(), self.image.height()) == self.image.height():
            self.initial_zoom = (768*0.7 / max(self.image.width(), self.image.height()))

        else:
            self.initial_zoom = (1024*0.8 / max(self.image.width(), self.image.height()))

        #PIXMAP
        self.pixmap = QPixmap.fromImage(self.image)

        #SCENE
        self.scene = QGraphicsScene(self)
        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

        #VIEW
        self.view = GraphicsView(self)
        self.view.setSceneRect(0, 0, self.image.width(), self.image.height())
        self.view.setScene(self.scene)

        #LABEL INFO
        self.info_label = QLabel(self)
        self.info_label.setText("Lewy przycisk myszy - Pędzel\nPrawy przycisk myszy - Gumka")
        self.info_label.setFixedSize(QSize(170, 60))

        #PEN THICKNESS SLIDER
        self.pen_thickness_slider = Slider(self, 1, 8, 1, "Grubość pędzla")
        self.pen_thickness_slider.setFixedSize(QSize(160, 60))

        self.pen_thickness_slider.slider.mouseReleaseEvent = self.set_pen_thickness

        #PEN OPACITY SLIDER
        self.pen_opacity_slider = Slider(self, 1, 100, 100, "Przezroczystość [%]")
        self.pen_opacity_slider.setFixedSize(QSize(160, 60))

        self.pen_opacity_slider.slider.mouseReleaseEvent = self.set_pen_opacity

        #COLOR PICKER BUTTON
        self.button_color_select = QPushButton("Wybierz kolor", self)
        self.button_color_select.clicked.connect(self.show_color_dialog)
        self.button_color_select.setFixedSize(QSize(120, 40))

        #COLOR PALETTE WIDGET
        self.color_palette_widget = ColorPalette(self)
        self.color_palette_widget.show()

        #EXPORT PIXELPERFECT BUTTON
        self.button_export_fast = QPushButton("Eksportuj - szybko", self)
        self.button_export_fast.clicked.connect(self.export_fast)
        self.button_export_fast.setFixedSize(QSize(120, 40))

        #EXPORT ORIGINAL RESOLUTION BUTTON
        self.button_export_custom = QPushButton("Eksportuj - dostosuj", self)
        self.button_export_custom.clicked.connect(self.export_custom)
        self.button_export_custom.setFixedSize(QSize(120, 40))

        #SINGLE LAYOUTS
        view_layout = QHBoxLayout()
        view_layout.addWidget(self.view)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_color_select)
        buttons_layout.addWidget(self.pen_thickness_slider)
        buttons_layout.addWidget(self.pen_opacity_slider)
        buttons_layout.addWidget(self.button_export_fast)
        buttons_layout.addWidget(self.button_export_custom)
        buttons_layout.addWidget(self.info_label)

        palette_layout = QHBoxLayout()
        palette_layout.addWidget(self.color_palette_widget)

        #WINDOW LAYOUT
        layout = QVBoxLayout(self)
        layout.addLayout(view_layout)
        layout.addLayout(palette_layout)
        layout.addLayout(buttons_layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setLayout(layout)

        #EVENTS
        self.view.mousePressEvent = self.event_mouse_press
        self.view.mouseMoveEvent = self.event_mouse_move
        self.view.mouseReleaseEvent = self.event_mouse_release

    def set_pen_thickness(self, event):

        self.pen.setWidth(self.pen_thickness_slider.slider.value())

    def set_pen_opacity(self, event):

        self.apply_alpha(self.selected_color)

    def set_pen_color(self, color):

        if isinstance(color, tuple):

            converted_color = QColor(*color)

            self.apply_alpha(converted_color)

    def show_color_dialog(self):

        color = QColorDialog.getColor()
        if color.isValid():
            print("Wybrany kolor:", color.name())

            self.apply_alpha(color)

    def apply_alpha(self, color):

        red, green, blue = color.red(), color.green(), color.blue()
        self.selected_color = QColor(red, green, blue, round(self.pen_opacity_slider.slider.value() * (255/self.pen_opacity_slider.slider.maximum())))

        self.pen.setColor(self.selected_color)


    def draw_pixel(self, x, y):

        painter = QPainter(self.image)
        painter.setPen(self.pen)

        if (self.previous_x, self.previous_y) != (x, y):
            painter.drawPoint(x, y)

        painter.end()

        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(self.pixmap))

    def erase_pixel(self, x, y):
        
        painter = QPainter(self.image)

        if (self.previous_x, self.previous_y) != (x, y):
            for i in range(-self.pen.width() // 2 + 1, self.pen.width() // 2 + 1):
                for j in range(-self.pen.width() // 2 + 1, self.pen.width() // 2 + 1):
                    painter.setPen(QColor(self.original_image.pixel(x + i, y + j)))
                    painter.drawPoint(x + i, y + j)

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
            self.draw_pixel(x, y)

        elif event.button() == Qt.RightButton:
            self.is_erase_mode = True
            self.erase_pixel(x, y)

    def event_mouse_move(self, event):

        if event.buttons() & (Qt.LeftButton | Qt.RightButton):

            scene_pos = self.view.mapToScene(event.pos())
            x, y = int(scene_pos.x()), int(scene_pos.y())

            if not self.is_erase_mode:
                self.draw_pixel(x, y)
            else:
                self.erase_pixel(x, y)

            self.previous_x, self.previous_y = x, y

    def event_mouse_release(self, event):
        
        if event.button() == Qt.RightButton:
            self.is_erase_mode = False

    def export_fast(self):

        if not os.path.exists("pixelart.png"):
            self.parent().statusBar().showMessage("Nie można wyeksportować obrazu")
            return
        
        print("Exporting image...")
        
        try:

            saveLocation = QFileDialog.getSaveFileName(self, "Save image", "image.png", "Image Files (*.png *.jpg *.bmp)")
            print(saveLocation[0])
            self.image.save(saveLocation[0])

            self.parent().statusBar().showMessage("Plik wyeksportowany pomyślnie")

        except:
            self.parent().statusBar().showMessage("Anulowano eksportowanie pliku")
        
        print("Image exported")

    def export_custom(self):

        dialog = ExportDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:

            custom_resolution = dialog.get_resolution()
            print("Custom Resolution:", custom_resolution)

            scaled_image = self.image.scaled(*custom_resolution)

            save_location, _ = QFileDialog.getSaveFileName(self, "Save image", "image.png", "Image Files (*.png *.jpg *.bmp)")

            if save_location:

                scaled_image.save(save_location)

                self.parent().statusBar().showMessage("Plik wyeksportowany pomyślnie")

        dialog.deleteLater()

import os, cv2

from PySide6.QtCore import QRect, QThreadPool, QMetaObject
from PySide6.QtWidgets import QLabel, QStatusBar, QMainWindow, QFileDialog, QCheckBox, QComboBox, QPushButton, QFrame, QMessageBox
from PySide6.QtGui import QIcon

from Viewer import Viewer
from Slider import Slider
from ProcessingWindow import ProcessingWindow
from Ui_EditWindow import Ui_EditWindow
from colorthief import ColorThief

class Ui_MainWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app = app

        #TITLE BAR
        self.setWindowTitle("Pixelart Gen")
        self.showMaximized()
        self.setFixedSize(1024,768)

        my_icon = QIcon()
        my_icon.addFile('icon.png')

        self.setWindowIcon(my_icon)

        #MENU BAR - FILE
        menu_bar = self.menuBar()
        menu_bar.setObjectName("menu_bar")
        menu_bar.setGeometry(QRect(0, 0, 1024, 30))

        self.file_menu = menu_bar.addMenu("&Plik")

        open_action = self.file_menu.addAction("Otwórz plik")
        open_action.triggered.connect(self.open_image)

        save_action = self.file_menu.addAction("Zapisz jako")
        save_action.triggered.connect(self.save_image)

        quit_action = self.file_menu.addAction("Zamknij")
        quit_action.triggered.connect(self.quit_app)

        #MENU BAR - EDIT
        self.edit_menu = menu_bar.addMenu("&Edycja")

        undo_action = self.edit_menu.addAction("Cofnij")
        undo_action.triggered.connect(self.undo)

        redo_action = self.edit_menu.addAction("Ponów")
        redo_action.triggered.connect(self.redo)

        reset_action = self.edit_menu.addAction("Resetuj")
        reset_action.triggered.connect(self.reset)

        #PIXELATE FACTOR SLIDER
        self.slider_pixelation = Slider(self, 2, 48, 8, "Pikselizacja")
        self.slider_pixelation.setGeometry(QRect(80, 40, 350, 60))
        self.slider_pixelation.slider.update()

        #RESIZE CHECKBOX
        self.checkbox_resize = QCheckBox(parent = self,text = "Zmniejsz realne wymiary obrazu (zalecane)")
        self.checkbox_resize.setGeometry(QRect(100, 80, 350, 60))
        self.checkbox_resize.setChecked(True)
        self.checkbox_resize.show()

        self.checkbox_resize.clicked.connect(self.start_processing)
        self.checkbox_resize.clicked.connect(self.save_history)

        #SMOOTHING SLIDER
        self.slider_smoothing = Slider(self, 0, 16, 0, "Wygładzanie")
        self.slider_smoothing.setGeometry(QRect(80, 120, 350, 60))

        #CATEGORY 1_2 FRAME
        self.frame1_2 = QLabel(parent = self)
        self.frame1_2.setGeometry(QRect(80, 180, 350, 10))
        self.frame1_2.setFrameShape(QFrame.HLine)
        self.frame1_2.setFrameShadow(QFrame.Plain)
        self.frame1_2.setLineWidth(2)
        self.frame1_2.setStyleSheet("color: #333333;")
        self.frame1_2.show()

        #COLOR REDUCE MODE COMBOBOX
        self.mode_combobox = QComboBox(parent = self)
        self.mode_combobox.addItems(["Adaptywny", "Adaptywny + Dither", "Z pliku", "Z pliku + Dither"])
        self.mode_combobox.setGeometry(QRect(80, 200, 350, 40))
        self.mode_combobox.show()

        self.mode_combobox.currentIndexChanged.connect(self.change_mode)
        self.mode_combobox.currentIndexChanged.connect(self.save_history)
        #self.mode_combobox.activated.connect(self.save_history)

        #COLORS REDUCE SLIDER
        self.slider_colorcount = Slider(self, 0, 32, 0, "Redukcja barw")
        self.slider_colorcount.setGeometry(QRect(80, 240, 350, 60))

        #COLOR PALETTE OPEN BUTTON
        self.button_palette = QPushButton("Wybierz plik", self)
        self.button_palette.setGeometry(QRect(80, 250, 350, 25))

        self.button_palette.clicked.connect(self.open_palette_file)

        #COLOR PALETTE LABEL
        self.label_palette = QLabel(parent = self)
        self.label_palette.setFrameStyle(QFrame.Panel)
        self.label_palette.setGeometry(QRect(80, 280, 350, 20))
        self.label_palette.setText("")

        #CATEGORY 2_3 FRAME
        self.frame2_3 = QLabel(parent = self)
        self.frame2_3.setGeometry(QRect(80, 310, 350, 10))
        self.frame2_3.setFrameShape(QFrame.HLine)
        self.frame2_3.setFrameShadow(QFrame.Plain)
        self.frame2_3.setLineWidth(2)
        self.frame2_3.setStyleSheet("color: #333333;")
        self.frame2_3.show()

        #EFFECTS ORDER CHECKBOX
        self.checkbox_effects_order = QCheckBox(parent = self,text = "Filtry przed zmianą palety")
        self.checkbox_effects_order.setGeometry(QRect(100, 310, 350, 60))
        self.checkbox_effects_order.setChecked(True)
        self.checkbox_effects_order.show()

        self.checkbox_effects_order.clicked.connect(self.start_processing)
        self.checkbox_effects_order.clicked.connect(self.save_history)

        #BRIGHTNESS SLIDER
        self.slider_brightness = Slider(self, -20, 20, 0, "Jasność")
        self.slider_brightness.setGeometry(QRect(80, 350, 350, 60))

        #CONTRAST SLIDER
        self.slider_contrast = Slider(self, -20, 20, 0, "Kontrast")
        self.slider_contrast.setGeometry(QRect(80, 400, 350, 60))

        #SATURATION SLIDER
        self.slider_saturation = Slider(self, -20, 20, 0, "Nasycenie")
        self.slider_saturation.setGeometry(QRect(80, 450, 350, 60))

        #CATEGORY 3_4 FRAME
        self.frame3_4 = QLabel(parent = self)
        self.frame3_4.setGeometry(QRect(80, 510, 350, 10))
        self.frame3_4.setFrameShape(QFrame.HLine)
        self.frame3_4.setFrameShadow(QFrame.Plain)
        self.frame3_4.setLineWidth(2)
        self.frame3_4.setStyleSheet("color: #333333;")
        self.frame3_4.show()

        #OUTLINE CHECKBOX
        self.checkbox_outline = QCheckBox(parent = self,text = "Dodaj kontur")
        self.checkbox_outline.setGeometry(QRect(100, 510, 350, 60))
        self.checkbox_outline.show()

        self.checkbox_outline.clicked.connect(self.start_processing)
        self.checkbox_outline.clicked.connect(self.show_outline_slider)
        self.checkbox_outline.clicked.connect(self.save_history)

        #OUTLINE THICKNESS SLIDER
        self.slider_outline_thickness = Slider(self, 1, 8, 1, "Grubość konturu")
        self.slider_outline_thickness.setGeometry(QRect(80, 550, 350, 60))
        self.slider_outline_thickness.setEnabled(False)

        #OUTLINE THRESHOLD SLIDER
        self.slider_outline_threshold = Slider(self, 0, 255, 180, "Progowy kontrast konturu")
        self.slider_outline_threshold.setGeometry(QRect(80, 600, 350, 60))
        self.slider_outline_threshold.setEnabled(False)

        #CATEGORY 4_5 FRAME
        self.frame4_5 = QLabel(parent = self)
        self.frame4_5.setGeometry(QRect(80, 660, 350, 10))
        self.frame4_5.setFrameShape(QFrame.HLine)
        self.frame4_5.setFrameShadow(QFrame.Plain)
        self.frame4_5.setLineWidth(2)
        self.frame4_5.setStyleSheet("color: #333333;")
        self.frame4_5.show()

        #EDIT WINDOW BUTTON
        self.button_edit_window = QPushButton("Edytuj i eksportuj obraz", self)
        self.button_edit_window.setGeometry(QRect(80, 680, 350, 40))
        self.button_edit_window.show()

        self.button_edit_window.clicked.connect(self.open_edit_window)

        #VIEWER
        self.threadpool = QThreadPool()
        self.viewer = Viewer(self)
        self.viewer.setGeometry(QRect(480, 50, 480, 680))

        #THREADPOOL
        self.threadpool.start(self.viewer.pixelate)

        #EDIT WINDOW
        self.window_processing = ProcessingWindow(self)

        #STATUSBAR
        self.setStatusBar(QStatusBar(self))

        #COLOR PALETTE
        self.palette_reduced = []


    #APP WINDOW CLOSE
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Wyłączenie programu',
                                     "Czy na pewno chcesz zakończyć działanie programu?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            if os.path.exists("source.png"):
                os.remove("source.png")

            if os.path.exists("pixelart.png"):
                 os.remove("pixelart.png")

            event.accept()
        else:
            event.ignore()

    #MOVE TO EDIT WINDOW
    def open_edit_window(self):

        if os.path.exists("pixelart.png"):

            color_thief = ColorThief("./pixelart.png")

            if (self.slider_colorcount.slider.value() != 0 and (self.mode_combobox.currentIndex() == 0 or self.mode_combobox.currentIndex() == 1)) or (self.mode_combobox.currentIndex() == 2 or self.mode_combobox.currentIndex() == 3):
                
                #LEN COUNT ALL 3 RGB VALUES IN
                palette_len = len(self.palette_reduced) % 12 + 1

                print(palette_len)

                palette_from_image = color_thief.get_palette(color_count = palette_len, quality = 1)

            else:
                palette_from_image = color_thief.get_palette(color_count = 13, quality = 1)

            window_edit = Ui_EditWindow(self, palette_from_image)

            window_edit.exec_()

        else:
            self.statusBar().showMessage("Nie ma pliku do edycji")

    #OPEN IMAGE FROM FILE
    def open_image(self):

        open_location = QFileDialog.getOpenFileName()

        self.load_image(open_location[0])

    #LOAD IMAGE FROM GIVEN LOCATION
    def load_image(self, openLocation):

        if openLocation is None:
            self.statusBar().showMessage("Nie udało się otworzyć pliku")
            return
        
        self.viewer.set_image(openLocation)

        try:
            self.initialize_history()
            self.start_processing()

            self.statusBar().showMessage("Plik został poprawnie otwarty")
        except:
            self.statusBar().showMessage("Nie udało się otworzyć pliku")

    #SAVE IMAGE TO FILE
    def save_image(self):

        if not os.path.exists("pixelart.png"):
            self.statusBar().showMessage("Brak obrazu do zapisania")
            return
        
        try:
            img = cv2.imread(os.getcwd() + "\pixelart.png")

            saveLocation = QFileDialog.getSaveFileName(self, "Save image", "image.png", "Image Files (*.png *.jpg *.bmp)")
            cv2.imwrite(saveLocation[0], img)
        except:
            self.statusBar().showMessage("Anulowano zapis pliku")

    #CLOSE APP
    def quit_app(self):

        self.app.quit()

    #NEW PROCESSING THREAD FOR CALCULATING EFFECTS - EXECUTES APPLY_EFFECTS
    def start_processing(self):

        if not os.path.exists("source.png"):
            self.statusBar().showMessage("Przed rozpoczęciem edycji otwórz obraz")
            return
        
        self.threadpool.start(self.apply_effects)

        self.window_processing.center()
        self.window_processing.show()
    
    def apply_effects(self):

        if not os.path.exists("source.png"):
            return False

        self.viewer.copy_source()

        if self.slider_smoothing.slider.value() != 0:
            self.viewer.smooth_image(self.slider_smoothing.slider.value()) 
        
        if self.slider_pixelation.slider.value() != 1:
            self.viewer.pixelate(self.slider_pixelation.slider.value(), self.checkbox_resize.isChecked())

        if self.checkbox_effects_order.isChecked() == True:

            if self.slider_brightness.slider.value() != 0:
                self.viewer.change_brightness(self.slider_brightness.slider.value())

            if self.slider_contrast.slider.value() != 0:
                self.viewer.change_contrast(self.slider_contrast.slider.value())

            if self.slider_saturation.slider.value() != 0:
                self.viewer.change_saturation(self.slider_saturation.slider.value())

        if  self.mode_combobox.currentIndex() == 0 and self.slider_colorcount.slider.value() != 0:
            self.viewer.color_reduce(self.slider_colorcount.slider.value())

        if  self.mode_combobox.currentIndex() == 1 and self.slider_colorcount.slider.value() != 0:
            self.viewer.color_reduce_dither(self.slider_colorcount.slider.value())

        if self.mode_combobox.currentIndex() == 2 and self.label_palette.text() != "":
            self.viewer.ChangePalette(self.label_palette.text())

        if  self.mode_combobox.currentIndex() == 3 and self.label_palette.text() != "":
            self.viewer.ChangePaletteDither(self.label_palette.text())

        if self.checkbox_effects_order.isChecked() == False:

            if self.slider_brightness.slider.value() != 0:
                self.viewer.change_brightness(self.slider_brightness.slider.value())

            if self.slider_contrast.slider.value() != 0:
                self.viewer.change_contrast(self.slider_contrast.slider.value())

            if self.slider_saturation.slider.value() != 0:
                self.viewer.change_saturation(self.slider_saturation.slider.value())

        if self.checkbox_outline.isChecked():

            self.viewer.create_outline(self.slider_outline_thickness.slider.value(), self.slider_outline_threshold.slider.value())

        self.viewer.set_preview()

        QMetaObject.invokeMethod(self.window_processing, "hide")

        return True
    
    def initialize_history(self):

        self.viewer.changes = 0
        self.viewer.max_changes = -1

        self.viewer.preview_history = [[
                self.slider_pixelation.slider.value(),
                self.checkbox_resize.isChecked(),
                self.slider_smoothing.slider.value(),
                self.mode_combobox.currentIndex(),
                self.slider_colorcount.slider.value(),
                self.checkbox_effects_order.isChecked(),
                self.slider_brightness.slider.value(),
                self.slider_contrast.slider.value(),
                self.slider_saturation.slider.value(),
                self.checkbox_outline.isChecked(),
                self.slider_outline_thickness.slider.value(),
                self.slider_outline_threshold.slider.value()]]

    def save_history(self):

        if not os.path.exists("source.png"):
            return

        if self.viewer.changes + 1 <= self.viewer.max_changes:

            self.viewer.changes += 1

            self.viewer.preview_history = self.viewer.preview_history[0:(self.viewer.changes + 1)]

            self.viewer.max_changes = len(self.viewer.preview_history) - 1

            self.viewer.preview_history[self.viewer.changes] = [
                self.slider_pixelation.slider.value(),
                self.checkbox_resize.isChecked(),
                self.slider_smoothing.slider.value(),
                self.mode_combobox.currentIndex(),
                self.slider_colorcount.slider.value(),
                self.checkbox_effects_order.isChecked(),
                self.slider_brightness.slider.value(),
                self.slider_contrast.slider.value(),
                self.slider_saturation.slider.value(),
                self.checkbox_outline.isChecked(),
                self.slider_outline_thickness.slider.value(),
                self.slider_outline_threshold.slider.value()]

        else:

            self.viewer.changes += 1

            self.viewer.preview_history.append([
                self.slider_pixelation.slider.value(),
                self.checkbox_resize.isChecked(),
                self.slider_smoothing.slider.value(),
                self.mode_combobox.currentIndex(),
                self.slider_colorcount.slider.value(),
                self.checkbox_effects_order.isChecked(),
                self.slider_brightness.slider.value(),
                self.slider_contrast.slider.value(),
                self.slider_saturation.slider.value(),
                self.checkbox_outline.isChecked(),
                self.slider_outline_thickness.slider.value(),
                self.slider_outline_threshold.slider.value()])

        if self.viewer.changes > self.viewer.max_changes:
            self.viewer.max_changes = self.viewer.changes

        print(self.viewer.preview_history)

    def undo(self):

        if self.viewer.changes > 0:

            self.viewer.changes -= 1
            params = self.viewer.preview_history[self.viewer.changes]

            self.slider_pixelation.slider.setValue(params[0])
            self.slider_pixelation.slider.update()

            self.checkbox_resize.setChecked(params[1])
            self.checkbox_resize.update()

            self.slider_smoothing.slider.setValue(params[2])
            self.slider_smoothing.slider.update()

            self.mode_combobox.setCurrentIndex(params[3])
            self.mode_combobox.update()

            self.slider_colorcount.slider.setValue(params[4])
            self.slider_colorcount.slider.update()

            self.checkbox_effects_order.setChecked(params[5])
            self.checkbox_effects_order.update()

            self.slider_brightness.slider.setValue(params[6])
            self.slider_brightness.slider.update()

            self.slider_contrast.slider.setValue(params[7])
            self.slider_contrast.slider.update()

            self.slider_saturation.slider.setValue(params[8])
            self.slider_saturation.slider.update()

            self.checkbox_outline.setChecked(params[9])
            self.checkbox_outline.update()

            self.slider_outline_thickness.slider.setValue(params[10])
            self.slider_outline_thickness.slider.update()

            self.slider_outline_threshold.slider.setValue(params[11])
            self.slider_outline_threshold.slider.update()

            self.start_processing()

        else:
            self.statusBar().showMessage("Brak starszych zmian")

    def redo(self):

        if self.viewer.changes + 1 <= self.viewer.max_changes:

            self.viewer.changes += 1
            params = self.viewer.preview_history[self.viewer.changes]

            self.slider_pixelation.slider.setValue(params[0])
            self.slider_pixelation.slider.update()

            self.checkbox_resize.setChecked(params[1])
            self.checkbox_resize.update()

            self.slider_smoothing.slider.setValue(params[2])
            self.slider_smoothing.slider.update()

            self.mode_combobox.setCurrentIndex(params[3])
            self.mode_combobox.update()

            self.slider_colorcount.slider.setValue(params[4])
            self.slider_colorcount.slider.update()

            self.checkbox_effects_order.setChecked(params[5])
            self.checkbox_effects_order.update()

            self.slider_brightness.slider.setValue(params[6])
            self.slider_brightness.slider.update()

            self.slider_contrast.slider.setValue(params[7])
            self.slider_contrast.slider.update()

            self.slider_saturation.slider.setValue(params[8])
            self.slider_saturation.slider.update()

            self.checkbox_outline.setChecked(params[9])
            self.checkbox_outline.update()

            self.slider_outline_thickness.slider.setValue(params[10])
            self.slider_outline_thickness.slider.update()

            self.slider_outline_threshold.slider.setValue(params[11])
            self.slider_outline_threshold.slider.update()

            self.start_processing()

        else:
            self.statusBar().showMessage("Brak nowszych zmian")

    def reset(self):

        default_settings = self.viewer.default_settings

        if self.viewer.preview_history == []:

            self.statusBar().showMessage("Nie wczytano pliku")
            return

        if self.viewer.preview_history[self.viewer.changes] == default_settings:

            self.statusBar().showMessage("Domyślne wartości są już podane")
            return

        if self.viewer.changes + 1 <= self.viewer.max_changes:

            self.viewer.changes += 1

            self.viewer.preview_history[self.viewer.changes] = default_settings

            self.viewer.preview_history = self.viewer.preview_history[0:(self.viewer.changes + 1)]

            self.viewer.max_changes = len(self.viewer.preview_history) - 1

        else:

            self.viewer.changes += 1

            self.viewer.preview_history.append(default_settings)

            self.slider_pixelation.slider.setValue(default_settings[0])
            self.slider_pixelation.slider.update()

            self.checkbox_resize.setChecked(default_settings[1])
            self.checkbox_resize.update()

            self.slider_smoothing.slider.setValue(default_settings[2])
            self.slider_smoothing.slider.update()

            self.mode_combobox.setCurrentIndex(default_settings[3])
            self.mode_combobox.update()

            self.slider_colorcount.slider.setValue(default_settings[4])
            self.slider_colorcount.slider.update()

            self.checkbox_effects_order.setChecked(default_settings[5])
            self.checkbox_effects_order.update()

            self.slider_brightness.slider.setValue(default_settings[6])
            self.slider_brightness.slider.update()

            self.slider_contrast.slider.setValue(default_settings[7])
            self.slider_contrast.slider.update()

            self.slider_saturation.slider.setValue(default_settings[8])
            self.slider_saturation.slider.update()

            self.checkbox_outline.setChecked(default_settings[9])
            self.checkbox_outline.update()

            self.slider_outline_thickness.slider.setValue(default_settings[10])
            self.slider_outline_thickness.slider.update()

            self.slider_outline_threshold.slider.setValue(default_settings[11])
            self.slider_outline_threshold.slider.update()

        self.start_processing()

        if self.viewer.changes > self.viewer.max_changes:
            self.viewer.max_changes = self.viewer.changes

        print(self.viewer.preview_history)

    def show_outline_slider(self):

        if self.checkbox_outline.isChecked():
            self.slider_outline_thickness.setEnabled(True)
            self.slider_outline_threshold.setEnabled(True)

        else:
            self.slider_outline_thickness.setEnabled(False)
            self.slider_outline_threshold.setEnabled(False)

    def change_mode(self):

        if self.mode_combobox.currentIndex() == 0 or self.mode_combobox.currentIndex() == 1:

            self.slider_colorcount.show()
            self.button_palette.hide()
            self.label_palette.hide()

            if self.slider_colorcount.slider.value() != 0:
                self.start_processing()

        else:

            self.slider_colorcount.hide()
            self.button_palette.show()
            self.label_palette.show()

            if self.label_palette.text() != "":
                self.start_processing()

    def open_palette_file(self):

        try:
            paletteLocation = QFileDialog.getOpenFileName()
            self.label_palette.setText(paletteLocation[0])
            
        except:
            self.statusBar().showMessage("Nie udało się otworzyć pliku palety barw")

        self.start_processing()
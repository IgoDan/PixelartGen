import os, cv2

from PySide6.QtCore import QRect, QEvent, QThreadPool, QMetaObject, QTimer
from PySide6.QtWidgets import  QWidget, QLabel, QVBoxLayout, QMenuBar, QStatusBar, QMainWindow, QFileDialog, QCheckBox, QComboBox, QPushButton, QFrame, QMessageBox

from Viewer import Viewer
from Slider import Slider
from ProcessingWindow import ProcessingWindow

class Ui_MainWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setWindowTitle("PixelartGen")
        self.showMaximized()
        self.setFixedSize(1024,768)

        #MENU BAR - FILE
        menuBar = self.menuBar()
        menuBar.setObjectName("menuBar")
        menuBar.setGeometry(QRect(0, 0, 1024, 20))

        self.fileMenu = menuBar.addMenu("&File")

        openAction = self.fileMenu.addAction("Open Image")
        openAction.triggered.connect(self.OpenImage)

        saveAction = self.fileMenu.addAction("Save As")
        saveAction.triggered.connect(self.SaveImage)

        quitAction = self.fileMenu.addAction("Quit")
        quitAction.triggered.connect(self.QuitApp)

        #MENU BAR - EDIT
        self.editMenu = menuBar.addMenu("&Edit")

        undoAction = self.editMenu.addAction("Undo")
        undoAction.triggered.connect(self.Undo)

        redoAction = self.editMenu.addAction("Redo")
        redoAction.triggered.connect(self.Redo)

        resetAction = self.editMenu.addAction("Reset")
        resetAction.triggered.connect(self.Reset)

        #PIXELATE FACTOR SLIDER
        self.sliderPixelate = Slider(self, 4, 64, 8, "Pikselizacja")
        self.sliderPixelate.setGeometry(QRect(80, 60, 350, 60))
        self.sliderPixelate.slider.update()

        self.sliderPixelate.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderPixelate.slider.sliderReleased.connect(self.SaveHistory)

        #RESIZE CHECKBOX
        self.checkboxResize = QCheckBox(parent = self,text = "Zmniejsz realne wymiary zdjęcia")
        self.checkboxResize.setGeometry(QRect(100, 100, 350, 60))
        self.checkboxResize.show()

        self.checkboxResize.stateChanged.connect(self.StartProcessing)
        self.checkboxResize.clicked.connect(self.SaveHistory)

        #SMOOTHING SLIDER
        self.sliderSmoothing = Slider(self, 0, 8, 0, "Wygładzanie")
        self.sliderSmoothing.setGeometry(QRect(80, 140, 350, 60))

        self.sliderSmoothing.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderSmoothing.slider.sliderReleased.connect(self.SaveHistory)

        #CATEGORY 2 FRAME
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(80, 180, 350, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #COLOR REDUCE MODE COMBOBOX
        self.modeComboBox = QComboBox(parent = self)
        self.modeComboBox.addItems(["Adaptywny", "Z pliku"])
        self.modeComboBox.setGeometry(QRect(80, 220, 350, 40))
        self.modeComboBox.show()

        self.modeComboBox.currentIndexChanged.connect(self.ModeChange)
        #sprawdzić czy działa
        self.modeComboBox.activated.connect(self.SaveHistory)

        #COLORS REDUCE SLIDER
        self.sliderColorcount = Slider(self, 0, 16, 0, "Redukcja barw")
        self.sliderColorcount.setGeometry(QRect(80, 260, 350, 60))

        self.sliderColorcount.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderColorcount.slider.sliderReleased.connect(self.SaveHistory)

        #COLOR PALETTE OPEN BUTTON
        self.paletteButton = QPushButton("Wybierz plik", self)
        self.paletteButton.setGeometry(QRect(80, 265, 350, 25))

        self.paletteButton.clicked.connect(self.OpenPaletteFile)

        #COLOR PALETTE LABEL
        self.paletteLabel = QLabel(parent = self)
        self.paletteLabel.setFrameStyle(QFrame.Panel)
        self.paletteLabel.setGeometry(QRect(80, 295, 350, 20))
        self.paletteLabel.setText("")

        #CATEGORY 3
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(80, 300, 350, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #BRIGHTNESS SLIDER
        self.sliderBrightness = Slider(self, -10, 10, 0, "Jasność")
        self.sliderBrightness.setGeometry(QRect(80, 330, 350, 60))

        self.sliderBrightness.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderBrightness.slider.sliderReleased.connect(self.SaveHistory)

        #CONTRAST SLIDER
        self.sliderContrast = Slider(self, -10, 10, 0, "Kontrast")
        self.sliderContrast.setGeometry(QRect(80, 370, 350, 60))

        self.sliderContrast.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderContrast.slider.sliderReleased.connect(self.SaveHistory)

        #SATURATION SLIDER
        self.sliderSaturation = Slider(self, -10, 10, 0, "Nasycenie")
        self.sliderSaturation.setGeometry(QRect(80, 410, 350, 60))

        self.sliderSaturation.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderSaturation.slider.sliderReleased.connect(self.SaveHistory)

        #CATEGORY 3
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(80, 450, 350, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #OUTLINE CHECKBOX
        self.checkboxOutline = QCheckBox(parent = self,text = "Dodaj kontur")
        self.checkboxOutline.setGeometry(QRect(100, 470, 350, 60))
        self.checkboxOutline.show()

        self.checkboxOutline.stateChanged.connect(self.StartProcessing)
        self.checkboxOutline.stateChanged.connect(self.ShowOutlineSlider)
        self.checkboxOutline.clicked.connect(self.SaveHistory)

        #OUTLINE THICKNESS SLIDER
        self.sliderOutline = Slider(self, 1, 8, 1, "Grubość konturu")
        self.sliderOutline.setGeometry(QRect(80, 510, 350, 60))

        self.sliderOutline.slider.sliderReleased.connect(self.StartProcessing)
        self.sliderOutline.slider.sliderReleased.connect(self.SaveHistory)

        self.sliderOutline.setEnabled(False)

        #VIEWER
        self.threadpool = QThreadPool()
        self.viewer = Viewer(self)
        self.viewer.setGeometry(QRect(480, 50, 480, 680))

        self.threadpool.start(self.viewer.Pixelate)

        self.processingWindow = ProcessingWindow(self)

        #STATUSBAR
        self.setStatusBar(QStatusBar(self))

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Wyłączenie programu',
                                     "Czy na pewno chcesz zakończyć działanie programu?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            os.remove("source.png")
            os.remove("pixelart.png")
            event.accept()
        else:
            event.ignore()

    #OPEN IMAGE FROM FILE
    def OpenImage(self):

        openLocation = QFileDialog.getOpenFileName()

        self.LoadImage(openLocation[0])

    #LOAD IMAGE FROM GIVEN LOCATION
    def LoadImage(self, openLocation):

        if openLocation is None:
            self.statusBar().showMessage("Nie udało się otworzyć pliku")
            return
        
        self.viewer.setImage(openLocation)

        try:
            self.InitializeHistory()
            self.ApplyEffects()
            self.statusBar().showMessage("Plik został poprawnie otwarty")
        except:
            self.statusBar().showMessage("Nie udało się otworzyć pliku")

    #SAVE IMAGE TO FILE
    def SaveImage(self):

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
    def QuitApp(self):

        self.app.quit()

    def StartProcessing(self):

        if not os.path.exists("source.png"):
            self.statusBar().showMessage("Przed rozpoczęciem edycji otwórz obraz")
            return
        
        #NEW PROCESSING THREAD
        self.threadpool.start(self.ApplyEffects)

        self.processingWindow.center()
        self.processingWindow.show()
    
    def ApplyEffects(self):

        if not os.path.exists("source.png"):
            return False

        self.viewer.copySource()

        if self.sliderPixelate.slider.value() != 1:
            self.viewer.Pixelate(self.sliderPixelate.slider.value(), self.checkboxResize.isChecked())

        if self.sliderSmoothing.slider.value() != 0:
            self.viewer.SmoothImage(self.sliderSmoothing.slider.value())

        if self.modeComboBox.currentIndex() == 1 and self.paletteLabel.text() != "":
            self.viewer.ChangePalette(self.paletteLabel.text())

        if self.sliderColorcount.slider.value() != 0 and self.modeComboBox.currentIndex() == 0:
            self.viewer.ColorReduce(self.sliderColorcount.slider.value())

        if self.sliderBrightness.slider.value() != 0:
            self.viewer.ChangeBrightness(self.sliderBrightness.slider.value())

        if self.sliderContrast.slider.value() != 0:
            self.viewer.ChangeContrast(self.sliderContrast.slider.value())

        if self.sliderSaturation.slider.value() != 0:
            self.viewer.ChangeSaturation(self.sliderSaturation.slider.value())

        if self.checkboxOutline.isChecked():
            self.viewer.CreateOutline(self.sliderOutline.slider.value())

        self.viewer.setPreview()

        QMetaObject.invokeMethod(self.processingWindow, "hide")

        return True
    
    def InitializeHistory(self):

        self.viewer.changes = 0
        self.viewer.maxChanges = -1

        self.viewer.previewHistory = [[
                self.sliderPixelate.slider.value(),
                self.checkboxResize.isChecked(),
                self.sliderSmoothing.slider.value(),
                self.modeComboBox.currentIndex(),
                self.sliderColorcount.slider.value(),
                self.sliderBrightness.slider.value(),
                self.sliderContrast.slider.value(),
                self.sliderSaturation.slider.value(),
                self.checkboxOutline.isChecked(),
                self.sliderOutline.slider.value()]]

    def SaveHistory(self):

        if not os.path.exists("source.png"):
            return

        if self.viewer.changes + 1 <= self.viewer.maxChanges:

            self.viewer.changes += 1

            self.viewer.previewHistory = self.viewer.previewHistory[0:(self.viewer.changes + 1)]

            self.viewer.maxChanges = len(self.viewer.previewHistory) - 1

            self.viewer.previewHistory[self.viewer.changes] = [
                self.sliderPixelate.slider.value(),
                self.checkboxResize.isChecked(),
                self.sliderSmoothing.slider.value(),
                self.modeComboBox.currentIndex(),
                self.sliderColorcount.slider.value(),
                self.sliderBrightness.slider.value(),
                self.sliderContrast.slider.value(),
                self.sliderSaturation.slider.value(),
                self.checkboxOutline.isChecked(),
                self.sliderOutline.slider.value()]

        else:

            self.viewer.changes += 1

            self.viewer.previewHistory.append([
                self.sliderPixelate.slider.value(),
                self.checkboxResize.isChecked(),
                self.sliderSmoothing.slider.value(),
                self.modeComboBox.currentIndex(),
                self.sliderColorcount.slider.value(),
                self.sliderBrightness.slider.value(),
                self.sliderContrast.slider.value(),
                self.sliderSaturation.slider.value(),
                self.checkboxOutline.isChecked(),
                self.sliderOutline.slider.value()])

        if self.viewer.changes > self.viewer.maxChanges:
            self.viewer.maxChanges = self.viewer.changes

        print(self.viewer.previewHistory)

    def Undo(self):

        if self.viewer.changes > 0:

            self.viewer.changes -= 1
            params = self.viewer.previewHistory[self.viewer.changes]

            self.sliderPixelate.slider.setValue(params[0])
            self.sliderPixelate.slider.update()

            self.checkboxResize.setChecked(params[1])
            self.checkboxResize.update()

            self.sliderSmoothing.slider.setValue(params[2])
            self.sliderSmoothing.slider.update()

            self.modeComboBox.setCurrentIndex(params[3])
            self.modeComboBox.update()

            self.sliderColorcount.slider.setValue(params[4])
            self.sliderColorcount.slider.update()

            self.sliderBrightness.slider.setValue(params[5])
            self.sliderBrightness.slider.update()

            self.sliderContrast.slider.setValue(params[6])
            self.sliderContrast.slider.update()

            self.sliderSaturation.slider.setValue(params[7])
            self.sliderSaturation.slider.update()

            self.checkboxOutline.setChecked(params[8])
            self.checkboxOutline.update()

            self.sliderOutline.slider.setValue(params[9])
            self.sliderOutline.slider.update()

            self.ApplyEffects()

        else:
            self.statusBar().showMessage("Brak starszych zmian")

    def Redo(self):

        if self.viewer.changes + 1 <= self.viewer.maxChanges:

            self.viewer.changes += 1
            params = self.viewer.previewHistory[self.viewer.changes]

            self.sliderPixelate.slider.setValue(params[0])
            self.sliderPixelate.slider.update()

            self.checkboxResize.setChecked(params[1])
            self.checkboxResize.update()

            self.sliderSmoothing.slider.setValue(params[2])
            self.sliderSmoothing.slider.update()

            self.modeComboBox.setCurrentIndex(params[3])
            self.modeComboBox.update()

            self.sliderColorcount.slider.setValue(params[4])
            self.sliderColorcount.slider.update()

            self.sliderBrightness.slider.setValue(params[5])
            self.sliderBrightness.slider.update()

            self.sliderContrast.slider.setValue(params[6])
            self.sliderContrast.slider.update()

            self.sliderSaturation.slider.setValue(params[7])
            self.sliderSaturation.slider.update()

            self.checkboxOutline.setChecked(params[8])
            self.checkboxOutline.update()

            self.sliderOutline.slider.setValue(params[9])
            self.sliderOutline.slider.update()

            self.ApplyEffects()

        else:
            self.statusBar().showMessage("Brak nowszych zmian")

    def Reset(self):

        default_settings = self.viewer.default_settings

        if self.viewer.previewHistory[self.viewer.changes] == default_settings:
            self.statusBar().showMessage("Domyślne wartości są już podane")
            return

        if self.viewer.changes + 1 <= self.viewer.maxChanges:

            self.viewer.changes += 1

            self.viewer.previewHistory[self.viewer.changes] = default_settings

            self.viewer.previewHistory = self.viewer.previewHistory[0:(self.viewer.changes + 1)]

            self.viewer.maxChanges = len(self.viewer.previewHistory) - 1

        else:
            self.viewer.changes += 1

            self.viewer.previewHistory.append(default_settings)

            self.sliderPixelate.slider.setValue(default_settings[0])
            self.sliderPixelate.slider.update()

            self.checkboxResize.setChecked(default_settings[1])
            self.checkboxResize.update()

            self.sliderSmoothing.slider.setValue(default_settings[2])
            self.sliderSmoothing.slider.update()

            self.modeComboBox.setCurrentIndex(default_settings[3])
            self.modeComboBox.update()

            self.sliderColorcount.slider.setValue(default_settings[4])
            self.sliderColorcount.slider.update()

            self.sliderBrightness.slider.setValue(default_settings[5])
            self.sliderBrightness.slider.update()

            self.sliderContrast.slider.setValue(default_settings[6])
            self.sliderContrast.slider.update()

            self.sliderSaturation.slider.setValue(default_settings[7])
            self.sliderSaturation.slider.update()

            self.checkboxOutline.setChecked(default_settings[8])
            self.checkboxOutline.update()

            self.sliderOutline.slider.setValue(default_settings[9])
            self.sliderOutline.slider.update()

        self.ApplyEffects()

        if self.viewer.changes > self.viewer.maxChanges:
            self.viewer.maxChanges = self.viewer.changes

        print(self.viewer.previewHistory)

    def ShowOutlineSlider(self):

        if self.checkboxOutline.isChecked():
            self.sliderOutline.setEnabled(True)
        else:
            self.sliderOutline.setEnabled(False)

    def ModeChange(self, index):

        if index == 0:
            self.sliderColorcount.show()
            self.paletteButton.hide()
            self.paletteLabel.hide()

            self.ApplyEffects()

        else:
            self.sliderColorcount.hide()
            self.paletteButton.show()
            self.paletteLabel.show()

            if self.paletteLabel.text() != "":
                self.ApplyEffects()

    def OpenPaletteFile(self):

        self.checkboxResize.setChecked(True)
        self.checkboxResize.update()

        paletteLocation = QFileDialog.getOpenFileName()
        self.paletteLabel.setText(paletteLocation[0])

        self.ApplyEffects()
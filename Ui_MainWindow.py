import os, cv2

from PySide6.QtCore import QRect, QEvent
from PySide6.QtWidgets import  QWidget, QLabel, QVBoxLayout, QMenuBar, QStatusBar, QMainWindow, QFileDialog, QCheckBox, QComboBox, QPushButton, QFrame

from Viewer import Viewer
from Slider import Slider

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
        self.sliderPixelate = Slider(self, 1, 64, 1, "Pikselizacja")
        self.sliderPixelate.setGeometry(QRect(100, 60, 300, 60))

        self.sliderPixelate.slider.valueChanged.connect(self.ApplyEffects)
        self.sliderPixelate.slider.sliderReleased.connect(self.SaveHistory)

        #RESIZE CHECKBOX
        self.checkboxResize = QCheckBox(parent = self,text = "Zmniejsz realne wymiary zdjęcia")
        self.checkboxResize.setGeometry(QRect(110, 100, 300, 60))
        self.checkboxResize.show()

        self.checkboxResize.stateChanged.connect(self.ApplyEffects)

        #SMOOTHING SLIDER
        self.sliderSmoothing = Slider(self, 0, 8, 0, "Wygładzanie")
        self.sliderSmoothing.setGeometry(QRect(100, 140, 300, 60))

        self.sliderSmoothing.slider.valueChanged.connect(self.ApplyEffects)
        self.sliderSmoothing.slider.sliderReleased.connect(self.SaveHistory)

        #CATEGORY 2 FRAME
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(100, 180, 300, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #COLOR REDUCE MODE COMBOBOX
        self.modeComboBox = QComboBox(parent = self)
        self.modeComboBox.addItems(["Adaptywny", "Z pliku"])
        self.modeComboBox.setGeometry(QRect(100, 220, 300, 40))
        self.modeComboBox.show()

        self.modeComboBox.currentIndexChanged.connect(self.ModeChange)

        #COLORS REDUCE SLIDER
        self.sliderColorcount = Slider(self, 0, 16, 0, "Redukcja barw")
        self.sliderColorcount.setGeometry(QRect(100, 260, 300, 60))

        self.sliderColorcount.slider.sliderReleased.connect(self.ApplyEffects)
        self.sliderColorcount.slider.sliderReleased.connect(self.SaveHistory)

        #COLOR PALETTE OPEN BUTTON
        self.paletteButton = QPushButton("Wybierz plik")
        self.paletteButton.setGeometry(QRect(100, 260, 300, 60))

        self.paletteButton.clicked.connect(self.OpenPaletteFile)

        #CATEGORY 3
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(100, 300, 300, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #BRIGHTNESS SLIDER
        self.sliderBrightness = Slider(self, -10, 10, 0, "Jasność")
        self.sliderBrightness.setGeometry(QRect(100, 330, 300, 60))

        self.sliderBrightness.slider.valueChanged.connect(self.ApplyEffects)
        self.sliderBrightness.slider.sliderReleased.connect(self.SaveHistory)

        #CONTRAST SLIDER
        self.sliderContrast = Slider(self, -10, 10, 0, "Kontrast")
        self.sliderContrast.setGeometry(QRect(100, 370, 300, 60))

        self.sliderContrast.slider.valueChanged.connect(self.ApplyEffects)
        self.sliderContrast.slider.sliderReleased.connect(self.SaveHistory)

        #TODO SATURATION SLIDER

        #CATEGORY 3
        self.qframe1 = QFrame(parent = self)
        self.qframe1.setGeometry(QRect(100, 450, 300, 50))
        self.qframe1.setFrameShape(QFrame.HLine)
        self.qframe1.setFrameShadow(QFrame.Sunken)
        self.qframe1.show()

        #OUTLINE CHECKBOX
        self.checkboxOutline = QCheckBox(parent = self,text = "Dodaj kontur")
        self.checkboxOutline.setGeometry(QRect(110, 480, 300, 60))
        self.checkboxOutline.show()

        self.checkboxOutline.stateChanged.connect(self.ApplyEffects)
        self.checkboxOutline.stateChanged.connect(self.ShowOutlineSlider)

        #OUTLINE THICKNESS SLIDER
        self.sliderOutline = Slider(self, 1, 8, 1, "Grubość konturu")
        self.sliderOutline.setGeometry(QRect(100, 520, 300, 60))

        self.sliderOutline.slider.valueChanged.connect(self.ApplyEffects)
        self.sliderOutline.slider.sliderReleased.connect(self.SaveHistory)

        self.sliderOutline.setEnabled(False)

        #VIEWER
        self.viewer = Viewer(self)
        self.viewer.setGeometry(QRect(500, 70, 440, 650))

        #STATUSBAR
        self.setStatusBar(QStatusBar(self))


    #OPEN IMAGE FROM FILE
    def OpenImage(self):
        openLocation = QFileDialog.getOpenFileName()
        print(openLocation)
        self.viewer.setImage(openLocation[0])

    #SAVE IMAGE TO FILE
    def SaveImage(self):
        img = cv2.imread(os.getcwd() + "\pixelart.jpg")
        saveLocation = QFileDialog.getSaveFileName(self, "Save image", "image.jpg", "Image Files (*.png *.jpg *.bmp)")
        print(saveLocation)
        cv2.imwrite(saveLocation[0], img)

    #CLOSE APP
    def QuitApp(self):
        self.app.quit()

    def ApplyEffects(self):

        self.viewer.copySource()

        if self.sliderSmoothing.slider.value() != 0:
            self.viewer.SmoothImage(self.sliderSmoothing.slider.value())

        if self.checkboxOutline.isChecked():
            self.viewer.CreateOutline(self.sliderOutline.slider.value())

        if self.sliderPixelate.slider.value() != 1:
            self.viewer.Pixelate(self.sliderPixelate.slider.value(), self.checkboxResize.isChecked())

        if self.sliderColorcount.slider.value() != 0:
            self.viewer.colorReduce(self.sliderColorcount.slider.value())

        if self.sliderBrightness.slider.value() != 0:
            self.viewer.ChangeBrightness(self.sliderBrightness.slider.value())

        if self.sliderContrast.slider.value() != 0:
            self.viewer.ChangeContrast(self.sliderContrast.slider.value())


        self.viewer.setPreview()

    def SaveHistory(self):
        if self.viewer.changes < self.viewer.maxChanges:
            self.viewer.changes += 1
            self.viewer.previewHistory[self.viewer.changes] = [self.sliderSmoothing.slider.value(),
                                                               self.sliderPixelate.slider.value(),
                                                               self.sliderColorcount.slider.value(),
                                                               self.sliderBrightness.slider.value(),
                                                               self.sliderContrast.slider.value(),
                                                               self.sliderOutline.slider.value()]

        else:
            self.viewer.changes += 1
            self.viewer.previewHistory.append(
            [self.sliderSmoothing.slider.value(),
             self.sliderPixelate.slider.value(),
             self.sliderColorcount.slider.value(),
             self.sliderBrightness.slider.value(),
             self.sliderContrast.slider.value(),
             self.sliderOutline.slider.value()])

        if self.viewer.changes >= self.viewer.maxChanges:
            self.viewer.maxChanges = self.viewer.changes

        print(self.viewer.previewHistory)

    def Undo(self):

        if self.viewer.changes > 0:

            self.viewer.changes -= 1
            params = self.viewer.previewHistory[self.viewer.changes]

            self.sliderSmoothing.slider.setValue(params[0])
            self.sliderSmoothing.slider.update()

            self.sliderPixelate.slider.setValue(params[1])
            self.sliderPixelate.slider.update()

            self.sliderColorcount.slider.setValue(params[2])
            self.sliderColorcount.slider.update()

            self.sliderBrightness.slider.setValue(params[3])
            self.sliderBrightness.slider.update()

            self.sliderContrast.slider.setValue(params[4])
            self.sliderContrast.slider.update()

            self.sliderOutline.slider.setValue(params[5])
            self.sliderOutline.slider.update()

            self.ApplyEffects()

        else:
            self.statusBar().showMessage("Brak starszych zmian")

    def Redo(self):
        if self.viewer.changes + 1 <= self.viewer.maxChanges:

            self.viewer.changes += 1
            params = self.viewer.previewHistory[self.viewer.changes]

            self.sliderSmoothing.slider.setValue(params[0])
            self.sliderPixelate.slider.setValue(params[1])
            self.sliderColorcount.slider.setValue(params[2])
            self.sliderBrightness.slider.setValue(params[3])
            self.sliderContrast.slider.setValue(params[4])
            self.sliderOutline.slider.setValue(params[5])

            self.ApplyEffects()

        else:
            self.statusBar().showMessage("Brak nowszych zmian")

    def Reset(self):
        if self.viewer.changes < self.viewer.maxChanges:
            self.viewer.changes += 1
            self.viewer.previewHistory[self.viewer.changes] = [0, 1, 0, 0, 0, 0]

        else:
            self.viewer.changes += 1
            self.viewer.previewHistory.append([0, 1, 0, 0, 0, 0])

        self.sliderSmoothing.slider.setValue(0)
        self.sliderPixelate.slider.setValue(1)
        self.sliderColorcount.slider.setValue(0)
        self.sliderBrightness.slider.setValue(0)
        self.sliderContrast.slider.setValue(0)
        self.sliderOutline.slider.setValue(0)

        self.ApplyEffects()

        if self.viewer.changes >= self.viewer.maxChanges:
            self.viewer.maxChanges = self.viewer.changes

        print(self.viewer.previewHistory)

    def ShowOutlineSlider(self):
        if self.checkboxOutline.isChecked():
            self.sliderOutline.setEnabled(True)
        else:
            self.sliderOutline.setEnabled(False)

    def ModeChange(self, index):
        pass

    def OpenPaletteFile(self):
        pass
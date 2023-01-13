import os, cv2

from PySide6.QtCore import QRect, QEvent
from PySide6.QtWidgets import  QWidget, QLabel, QVBoxLayout, QMenuBar, QStatusBar, QMainWindow, QFileDialog, QCheckBox

from Viewer import Viewer
from Slider import Slider

class Ui_MainWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setWindowTitle("PixelartGen")
        self.showMaximized()
        self.setFixedSize(1280,720)

        #MENU BAR
        menuBar = self.menuBar()
        menuBar.setObjectName("menuBar")
        menuBar.setGeometry(QRect(0, 0, 1280, 20))

        self.fileMenu = menuBar.addMenu("&File")

        openAction = self.fileMenu.addAction("Open Image")
        openAction.triggered.connect(self.OpenImage)

        saveAction = self.fileMenu.addAction("Save As")
        saveAction.triggered.connect(self.SaveImage)

        quitAction = self.fileMenu.addAction("Quit")
        quitAction.triggered.connect(self.QuitApp)

        #PIXELATE FACTOR SLIDER
        self.sliderPixelate = Slider(self, 1, 64, 1, "Pikselizacja")
        self.sliderPixelate.setObjectName("pikselizacja")
        self.sliderPixelate.setGeometry(QRect(200, 20, 300, 60))

        self.sliderPixelate.slider.valueChanged.connect(self.ApplyEffects)

        #RESIZE CHECKBOX
        self.checkboxResize = QCheckBox(parent = self,text = "Zmniejsz realne wymiary zdjęcia")
        self.checkboxResize.setGeometry(QRect(200, 60, 300, 60))
        self.checkboxResize.show()

        self.checkboxResize.stateChanged.connect(self.ApplyEffects)

        #COLORS REDUCE SLIDER
        self.sliderColorcount = Slider(self, 0, 16, 0, "Redukcja barw")
        self.sliderColorcount.setObjectName("redukcja")
        self.sliderColorcount.setGeometry(QRect(200, 100, 300, 60))

        self.sliderColorcount.slider.sliderReleased.connect(self.ApplyEffects)

        #BRIGHTNESS SLIDER
        self.sliderBrightness = Slider(self, -10, 10, 0, "Jasność")
        self.sliderBrightness.setObjectName("jasnosc")
        self.sliderBrightness.setGeometry(QRect(200, 140, 300, 60))

        self.sliderBrightness.slider.valueChanged.connect(self.ApplyEffects)

        #CONTRAST SLIDER
        self.sliderContrast = Slider(self, -10, 10, 0, "Kontrast")
        self.sliderContrast.setObjectName("kontrast")
        self.sliderContrast.setGeometry(QRect(200, 180, 300, 60))

        self.sliderContrast.slider.valueChanged.connect(self.ApplyEffects)


        #SMOOTHING SLIDER
        self.sliderSmoothing = Slider(self, 0, 8, 0, "Wygładzanie")
        self.sliderSmoothing.setObjectName("wygladzanie")
        self.sliderSmoothing.setGeometry(QRect(200, 260, 300, 60))

        self.sliderSmoothing.slider.valueChanged.connect(self.ApplyEffects)

        #VIEWER
        self.viewer = Viewer(self)
        self.viewer.setObjectName("viewer")
        self.viewer.setGeometry(QRect(660, 50, 440, 650))


        #STATUS BAR
        statusBar = self.statusBar()
        statusBar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

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
        #cv2.waitKey(0)

    #CLOSE APP
    def QuitApp(self):
        self.app.quit()

    def ApplyEffects(self):

        self.viewer.copySource()

        if self.sliderSmoothing.slider.value() != 0:
            self.viewer.SmoothImage(self.sliderSmoothing.slider.value())

        if self.sliderPixelate.slider.value() != 1:
            self.viewer.Pixelate(self.sliderPixelate.slider.value(), self.checkboxResize.isChecked())

        if self.sliderColorcount.slider.value() != 0:
            self.viewer.colorReduce(self.sliderColorcount.slider.value())

        if self.sliderBrightness.slider.value() != 0:
            self.viewer.ChangeBrightness(self.sliderBrightness.slider.value())

        if self.sliderContrast.slider.value() != 0:
            self.viewer.ChangeContrast(self.sliderContrast.slider.value())

        self.viewer.setPreview()

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPixmap, QImage
import cv2, numpy as np
import imghdr
import os

from sklearn.cluster import MiniBatchKMeans

class Viewer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.mainLayout = QVBoxLayout()

        self.source = QLabel()
        self.source.setGeometry(QRect(700, 50, 400, 300))
        self.source.setAlignment(Qt.AlignCenter)
        self.source.setText('\n\n Upuść zdjęcie \n\n')
        self.source.setStyleSheet('''QLabel{border: 4px dashed #aaa}''')

        self.preview = QLabel()
        self.preview.setGeometry(QRect(700, 380, 400, 300))
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setText('\n\n Tu wyświetli się podgląd \n\n')
        self.preview.setStyleSheet('''QLabel{border: 4px dashed #aaa}''')

        self.mainLayout.addWidget(self.source)
        self.mainLayout.addWidget(self.preview)
        self.setLayout(self.mainLayout)

        self.show()

        self.changes = 0
        self.maxChanges = 0
        self.previewHistory = [[0, 1, 0, 0, 0, 0]]


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:

            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.setImage(file_path)

            event.accept()
        else:
            event.ignore()

    def setImage(self, file_path):

        fmt = imghdr.what(file_path)
        img = QPixmap(file_path, format = fmt)

        w, h = img.width(), img.height()

        if w / h < self.source.width()/self.source.height():
            self.source.setPixmap(img.scaledToHeight(self.source.height() - 10))
            self.preview.setPixmap(img.scaledToHeight(self.source.height()- 10))
        else:
            self.source.setPixmap(img.scaledToWidth(self.source.width() - 10))
            self.preview.setPixmap(img.scaledToWidth(self.source.width() - 10))

        self.src = cv2.imread(file_path)
        cv2.imwrite("source.jpg", self.src)

    def setPreview(self):
        img = QPixmap(os.getcwd() + "\pixelart.jpg")

        w, h = img.width(), img.height()

        if w / h < self.source.width()/self.source.height():
            self.preview.setPixmap(img.scaledToHeight(self.source.height()- 10))
        else:
            self.preview.setPixmap(img.scaledToWidth(self.source.width() - 10))

    def copySource(self):
        img = cv2.imread(os.getcwd() + "\source.jpg")
        cv2.imwrite("pixelart.jpg", img)

    def Pixelate(self, factor, resize):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")

        height, width = img.shape[:2]

        pixelart = cv2.resize(img, (int(width/factor), int(height/factor)), interpolation = cv2.INTER_LINEAR)

        if resize == False:
            pixelart = cv2.resize(pixelart, (width, height), interpolation=cv2.INTER_NEAREST)

        cv2.imwrite("pixelart.jpg", pixelart)

    def colorReduce(self, count):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")
        imgf = np.float32(img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        pixelart = center[label.flatten()]

        pixelart = pixelart.reshape(img.shape)

        cv2.imwrite("pixelart.jpg", pixelart)

    def ChangeBrightness(self, brightness):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")
        brightness = brightness * 12.8

        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness

            alphaBrightness = (highlight - shadow)/255
            gammaBrightness = shadow

            img = cv2.addWeighted(img, alphaBrightness, img, 0, gammaBrightness)

        cv2.imwrite("pixelart.jpg", img)

    def ChangeContrast(self, contrast):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")
        contrast = contrast * 6.4

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alphaContrast = float(f)
            gammaContrast = float(127 * (1 - f))

            img = cv2.addWeighted(img, alphaContrast, img, 0, gammaContrast)

        cv2.imwrite("pixelart.jpg", img)

    def SmoothImage(self, factor):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")

        factor = 2 * factor - 1

        smoothed = cv2.medianBlur(img, int(factor))

        cv2.imwrite("pixelart.jpg", smoothed)

    def CreateOutline(self, thickness):

        img = cv2.imread(os.getcwd() + "\pixelart.jpg")

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(image = thresh, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)
                                      
        cv2.drawContours(image = img, contours = contours, contourIdx = -1, color = (0, 0, 0), thickness = thickness, lineType = cv2.LINE_AA)

        cv2.imwrite("pixelart.jpg", img)
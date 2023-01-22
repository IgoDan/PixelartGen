from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPixmap, QImage
import cv2, numpy as np
import imghdr
import os

class Viewer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.mainLayout = QVBoxLayout()

        self.source = QLabel()
        self.source.setGeometry(QRect(700, 50, 440, 330))
        self.source.setAlignment(Qt.AlignCenter)
        self.source.setText('\n\n Upuść zdjęcie \n\n')
        self.source.setStyleSheet('''QLabel{border: 4px dashed #aaa}''')

        self.preview = QLabel()
        self.preview.setGeometry(QRect(700, 380, 440, 330))
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setText('\n\n Tu wyświetli się podgląd \n\n')
        self.preview.setStyleSheet('''QLabel{border: 4px dashed #aaa}''')

        self.mainLayout.addWidget(self.source)
        self.mainLayout.addWidget(self.preview)
        self.setLayout(self.mainLayout)

        self.show()

        self.changes = 0
        self.maxChanges = 0
        self.previewHistory = [[0, 1, 0, 0, 0, 0, 0]]


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
            self.copySource()
            self.parent().ApplyEffects()

            event.accept()
        else:
            event.ignore()

    def setImage(self, file_path):

        if file_path == "":
            return
            
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
        cv2.imwrite("source.png", self.src)

    def setPreview(self):
        img = QPixmap(os.getcwd() + "\pixelart.png")

        w, h = img.width(), img.height()

        if w / h < self.source.width()/self.source.height():
            self.preview.setPixmap(img.scaledToHeight(self.source.height()- 10))
        else:
            self.preview.setPixmap(img.scaledToWidth(self.source.width() - 10))

    def copySource(self):
        img = cv2.imread(os.getcwd() + "\source.png")
        cv2.imwrite("pixelart.png", img)

    def Pixelate(self, factor, resize):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        height, width = img.shape[:2]

        pixelart = cv2.resize(img, (int(width/factor), int(height/factor)), interpolation = cv2.INTER_LINEAR)

        if resize == False:
            pixelart = cv2.resize(pixelart, (width, height), interpolation=cv2.INTER_NEAREST)

        cv2.imwrite("pixelart.png", pixelart)

    def colorReduce(self, count):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        imgf = np.float32(img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        pixelart = center[label.flatten()]

        pixelart = pixelart.reshape(img.shape)

        cv2.imwrite("pixelart.png", pixelart)

    def ChangeBrightness(self, brightness):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
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

        cv2.imwrite("pixelart.png", img)

    def ChangeContrast(self, contrast):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        contrast = contrast * 6.4

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alphaContrast = float(f)
            gammaContrast = float(127 * (1 - f))

            img = cv2.addWeighted(img, alphaContrast, img, 0, gammaContrast)

        cv2.imwrite("pixelart.png", img)

    def SmoothImage(self, factor):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        factor = 2 * factor - 1

        smoothed = cv2.medianBlur(img, int(factor))

        cv2.imwrite("pixelart.png", smoothed)

    def CreateOutline(self, thickness):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(image = thresh, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)
                                      
        cv2.drawContours(image = img, contours = contours, contourIdx = -1, color = (0, 0, 0), thickness = thickness, lineType = cv2.LINE_AA)

        cv2.imwrite("pixelart.png", img)

    def ChangeSaturation(self, value):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        s = hsv[:,:,1] * (1 + value / 10)
        s = np.clip(s, 0, 255)
        hsv[:,:,1] = s

        saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imwrite("pixelart.png", saturated)

    def ChangePalette(self, dir):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        pal_file = open(dir, "r")

        pal = []

        for line in pal_file:
            if line[0:2] != "FF":
                continue
            else:
                pal.append(line[2:-1])
            
        pal_rgb = []

        for hex in pal:
            pal_rgb.append([int("0x" + hex[0:2], 0), int("0x" + hex[2:4], 0), int("0x" + hex[4:6], 0)])


        h = img.shape[0]
        w = img.shape[1]

        for y in range(0, h):
            for x in range(0, w):
                r,g,b = img[y, x, 2], img[y, x, 1], img[y, x, 0]
                dif = []
                for clr in pal_rgb:
                    dif.append(sum([abs(r - clr[0]), abs(g - clr[1]), abs(b - clr[2])]))

                min_index = dif.index(min(dif))

                img[y, x, 2], img[y, x, 1], img[y, x, 0] = pal_rgb[min_index][0], pal_rgb[min_index][1], pal_rgb[min_index][2]

        cv2.imwrite("pixelart.png", img)

        self.setPreview()
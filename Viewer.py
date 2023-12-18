from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QRect, QRunnable
from PySide6.QtGui import QPixmap
import cv2, numpy as np
import imghdr
import os

class Viewer(QWidget, QRunnable):

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
        self.maxChanges = -1
        self.default_settings = [8, True, 0, 0, 0, 0, 0, 0, False, 1, 200]
        self.previewHistory = []

        self.rgb_pal = []


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:

            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasImage:

            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()

            self.parent().LoadImage(file_path)

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

    def ColorReduce(self, count):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        imgf = np.float32(img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)

        pal_rgb = center.tolist()

        pixelart = center[label.flatten()]

        pixelart = pixelart.reshape(img.shape)

        cv2.imwrite("pixelart.png", pixelart)

    def ColorReduceDither(self, count):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        imgf = np.float32(img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        pal_rgb = center.tolist()

        print(pal_rgb)

        counter = 0

        for color in pal_rgb:
            color[0], color[1], color[2] = color[2], color[1], color[0]

        h = img.shape[0]
        w = img.shape[1]

        for y in range(h):
            for x in range(w):

                r, g, b = img[y, x, 2], img[y, x, 1], img[y, x, 0]

                #Checking color palette for closest color
                new_color = self.FindClosestColor(r, g, b, pal_rgb)

                img[y, x, 2], img[y, x, 1], img[y, x, 0] = new_color

                #QUANT ERROR = old_color - new_color
                quant_error = np.array([r - new_color[0], g - new_color[1], b - new_color[2]])

                #Floyd–Steinberg dithering:
                #Multiplying (x+1;y) by 7/16
                if x + 1 < w:
                    img[y, x + 1, :] = np.clip(img[y, x + 1, :] + quant_error * (7 / 16), 0, 255)

                #Multiplying (x+1;y+1) by 1/16
                if x + 1 < w and y + 1 < h:
                    img[y + 1, x + 1, :] = np.clip(img[y + 1, x + 1, :] + quant_error * (1 / 16), 0, 255)

                #Multiplying (x;y+1) by 5/16
                if y + 1 < h:
                    img[y + 1, x, :] = np.clip(img[y + 1, x, :] + quant_error * (5 / 16), 0, 255)

                #Multiplying (x-1;y+1) by 3/16
                if x - 1 >= 0 and y + 1 < h:
                    img[y + 1, x - 1, :] = np.clip(img[y + 1, x - 1, :] + quant_error * (3 / 16), 0, 255)

                if counter == 20000:
                    counter = 0

                    cv2.imwrite("pixelart.png", img)
                    self.setPreview()

        cv2.imwrite("pixelart.png", img)


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

    def CreateOutline(self, thickness, threshold):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blurred = cv2.GaussianBlur(src=img_gray, ksize=(3, 3), sigmaX=0.5)
        edges = cv2.Canny(img_blurred, threshold, 255, L2gradient=False)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(img, contours, -1, (0, 0, 0), thickness)

        cv2.imwrite("pixelart.png", img)

    def ChangeSaturation(self, value):

        img = cv2.imread(os.getcwd() + "\pixelart.png")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        s = hsv[:,:,1] * (1 + value / 10)
        s = np.clip(s, 0, 255)
        hsv[:,:,1] = s

        saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imwrite("pixelart.png", saturated)

    def LoadPalette(self, dir):
        
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

        print("in loadpalette")

        return pal_rgb
    
    def FindClosestColor(self, r, g, b, color_palette):

        old_color = [r, g, b]
        new_color = color_palette[0]
        min_distance = np.linalg.norm(np.array(old_color) - np.array(color_palette[0]))

        for color in color_palette:
            new_distance = np.linalg.norm(np.array(color) - np.array(old_color))

            if new_distance < min_distance:
                new_color = color
                min_distance = new_distance

        return new_color


    def ChangePalette(self, dir):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        
        pal_rgb = self.LoadPalette(dir)

        h = img.shape[0]
        w = img.shape[1]

        for y in range(0, h):
            for x in range(0, w):
                r,g,b = img[y, x, 2], img[y, x, 1], img[y, x, 0]

                new_color = self.FindClosestColor(r, g, b, pal_rgb)

                img[y, x, 2], img[y, x, 1], img[y, x, 0] = new_color

        cv2.imwrite("pixelart.png", img)

        self.setPreview()

    def ChangePaletteDither(self, dir):

        img = cv2.imread(os.getcwd() + "\pixelart.png")
        
        pal_rgb = self.LoadPalette(dir)

        h = img.shape[0]
        w = img.shape[1]

        counter = 0

        for y in range(h):
            for x in range(w):

                r, g, b = img[y, x, 2], img[y, x, 1], img[y, x, 0]

                #Checking color palette for closest color
                new_color = self.FindClosestColor(r, g, b, pal_rgb)

                img[y, x, 2], img[y, x, 1], img[y, x, 0] = new_color

                #QUANT ERROR = old_color - new_color
                quant_error = np.array([r - new_color[0], g - new_color[1], b - new_color[2]])

                #Floyd–Steinberg dithering:
                #Multiplying (x+1;y) by 7/16
                if x + 1 < w:
                    img[y, x + 1, :] = np.clip(img[y, x + 1, :] + quant_error * (7 / 16), 0, 255)

                #Multiplying (x+1;y+1) by 1/16
                if x + 1 < w and y + 1 < h:
                    img[y + 1, x + 1, :] = np.clip(img[y + 1, x + 1, :] + quant_error * (1 / 16), 0, 255)

                #Multiplying (x;y+1) by 5/16
                if y + 1 < h:
                    img[y + 1, x, :] = np.clip(img[y + 1, x, :] + quant_error * (5 / 16), 0, 255)

                #Multiplying (x-1;y+1) by 3/16
                if x - 1 >= 0 and y + 1 < h:
                    img[y + 1, x - 1, :] = np.clip(img[y + 1, x - 1, :] + quant_error * (3 / 16), 0, 255)

                counter += 1

                if counter == 20000:
                    counter = 0

                    cv2.imwrite("pixelart.png", img)
                    self.setPreview()

        cv2.imwrite("pixelart.png", img)

        self.setPreview()
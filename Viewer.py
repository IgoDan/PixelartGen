import cv2, imghdr, os, numpy as np

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QRect, QRunnable
from PySide6.QtGui import QPixmap, QImage

class Viewer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()

        self.img = None

        self.source = QLabel()
        self.source.setGeometry(QRect(700, 50, 440, 330))
        self.source.setAlignment(Qt.AlignCenter)
        self.source.setText('\n\n Upuść zdjęcie \n\n')
        self.source.setStyleSheet('''QLabel{border: 3px dashed #666666}''')

        self.preview = QLabel()
        self.preview.setGeometry(QRect(700, 380, 440, 330))
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setText('\n\n Tu wyświetli się podgląd \n\n')
        self.preview.setStyleSheet('''QLabel{border: 3px dashed #666666}''')

        self.layout.addWidget(self.source)
        self.layout.addWidget(self.preview)
        self.setLayout(self.layout)

        self.show()

        self.changes = 0
        self.max_changes = -1
        self.default_settings = [8, True, 0, 0, 0, True, 0, 0, 0, False, 1, 180]
        self.preview_history = []

    def dragEnterEvent(self, event):

        if event.mimeData().hasImage:
            event.accept()

        else:
            event.ignore()


    def dropEvent(self, event):

        if event.mimeData().hasImage:

            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()

            self.parent().load_image(file_path)

            event.accept()

        else:
            event.ignore()

    def set_image(self, file_path):

        if file_path == "":
            return False

        file_format = imghdr.what(file_path)

        print(file_format)

        if file_format == None:
            self.parent().statusBar().showMessage("Wczytany plik nie jest obrazem")
            return False

        image = QPixmap(file_path, format = file_format)

        w, h = image.width(), image.height()

        if w / h < self.source.width()/self.source.height():
            self.source.setPixmap(image.scaledToHeight(self.source.height() - 10))
            self.preview.setPixmap(image.scaledToHeight(self.source.height()- 10))
        else:
            self.source.setPixmap(image.scaledToWidth(self.source.width() - 10))
            self.preview.setPixmap(image.scaledToWidth(self.source.width() - 10))

        self.src = cv2.imread(file_path)
        cv2.imwrite("source.png", self.src)

    def set_preview(self):

        print("start set_preview")

        cv2.imwrite("pixelart.png", self.img)

        pixmap = QPixmap(os.getcwd() + "\pixelart.png")

        w, h = pixmap.width(), pixmap.height()

        if w / h < self.source.width()/self.source.height():
            self.preview.setPixmap(pixmap.scaledToHeight(self.source.height()- 10))
        else:
            self.preview.setPixmap(pixmap.scaledToWidth(self.source.width() - 10))

        print("end set_preview")

    def update_preview(self):

        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        qimg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap(qimg)

        w, h = pixmap.width(), pixmap.height()

        if w / h < self.source.width()/self.source.height():
            self.preview.setPixmap(pixmap.scaledToHeight(self.source.height()- 10))
        else:
            self.preview.setPixmap(pixmap.scaledToWidth(self.source.width() - 10))

    def copy_source(self):

        self.img = cv2.imread(os.getcwd() + "\source.png")
        cv2.imwrite("pixelart.png", self.img)

        print("copy_source ok")

    def pixelate(self, factor, resize):

        height, width = self.img.shape[:2]

        self.img = cv2.resize(self.img, (int(width/factor), int(height/factor)), interpolation = cv2.INTER_LINEAR)

        if resize == False:
            self.img = cv2.resize(self.img, (width, height), interpolation=cv2.INTER_NEAREST)

        print("pixelate ok")

    def dither_algorithm(self, img, reduced_colors, h, w):

        counter = 0

        for y in range(h):
            for x in range(w):

                r, g, b = img[y, x, 2], img[y, x, 1], img[y, x, 0]

                #Checking color palette for closest color
                new_color = self.find_closest_color(r, g, b, reduced_colors)

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

                    self.img = img
                    self.update_preview()

        print("dither alg ok")

        return img

    def color_reduce(self, count):

        imgf = np.float32(self.img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)

        reduced_colors = center.tolist()
        self.parent().palette_reduced = reduced_colors

        for color in reduced_colors:
            color[0], color[1], color[2] = color[2], color[1], color[0]

        pixelart = center[label.flatten()]

        self.img = pixelart.reshape(self.img.shape)

        print("color_reduce ok")

    def color_reduce_dither(self, count):

        imgf = np.float32(self.img).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        compactness, label, center = cv2.kmeans(imgf, count, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)

        reduced_colors = center.tolist()
        self.parent().palette_reduced = reduced_colors

        print(reduced_colors)

        for color in reduced_colors:
            color[0], color[1], color[2] = color[2], color[1], color[0]

        h, w = self.img.shape[0], self.img.shape[1]

        self.img = self.dither_algorithm(self.img, reduced_colors, h, w)

    def change_brightness(self, brightness):

        brightness = brightness * (256 / self.parent().slider_brightness.slider.maximum())

        if brightness > 0:
            shadow = brightness
            highlight = 255
                
        else:
            shadow = 0
            highlight = 255 + brightness

        alphaBrightness = (highlight - shadow)/255
        gammaBrightness = shadow

        self.img = cv2.addWeighted(self.img, alphaBrightness, self.img, 0, gammaBrightness)

    def change_contrast(self, contrast):

        contrast = contrast * (128 / self.parent().slider_contrast.slider.maximum())

        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alphaContrast = float(f)
        gammaContrast = float(127 * (1 - f))

        self.img = cv2.addWeighted(self.img, alphaContrast, self.img, 0, gammaContrast)

    def change_saturation(self, value):

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        #SCALED SATURATION ADJUSTMENT
        """ len_y = len(hsv[:,:,1])
        len_x = len(hsv[:,:,1][0])  

        print(hsv[:,:,1][0, 0:10])

        if value > 0:
            slider_plus_ratio = (value / self.parent().slider_saturation.slider.maximum())
            for y in range(len_y):
                for x in range(len_x):
                    hsv[:,:,1][y, x] += (255- hsv[:,:,1][y, x]) * slider_plus_ratio

        else:
            slider_minus_ratio = (value / self.parent().slider_saturation.slider.minimum())
            for y in range(len_y):
                for x in range(len_x):
                    hsv[:,:,1][y, x] -= hsv[:,:,1][y, x] * slider_minus_ratio """

        #LINEAR SATURATION ADJUSTMENT

        if value > self.parent().slider_saturation.slider.minimum():
            s = hsv[:,:,1] * (1 + 2* value / 20)
            s = np.clip(s, 0, 255)

        else:
            len_y = len(hsv[:,:,1])
            len_x = len(hsv[:,:,1][0]) 

            s = hsv[:,:,1]

            for y in range(len_y):
                for x in range(len_x):
                    s[y, x] = 0

        hsv[:,:,1] = s

        self.img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def smooth_image(self, factor):

        factor = 2 * factor - 1

        self.img = cv2.medianBlur(self.img, int(factor))

    def create_outline(self, thickness, threshold):

        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        img_blurred = cv2.GaussianBlur(src=img_gray, ksize=(5, 5), sigmaX=0.5)

        edges = cv2.Canny(img_blurred, threshold, 255, L2gradient=False)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.img, contours, -1, (0, 0, 0), thickness)

    def load_palette(self, dir):
        
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

        return pal_rgb
    
    def find_closest_color(self, r, g, b, color_palette):

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
        
        reduced_colors = self.load_palette(dir)
        self.parent().palette_reduced = reduced_colors

        h = self.img.shape[0]
        w = self.img.shape[1]

        for y in range(0, h):
            for x in range(0, w):
                r,g,b = self.img[y, x, 2], self.img[y, x, 1], self.img[y, x, 0]

                new_color = self.find_closest_color(r, g, b, reduced_colors)

                self.img[y, x, 2], self.img[y, x, 1], self.img[y, x, 0] = new_color

    def ChangePaletteDither(self, dir):

        reduced_colors = self.load_palette(dir)
        self.parent().palette_reduced = reduced_colors

        print(reduced_colors)

        h = self.img.shape[0]
        w = self.img.shape[1]

        self.img = self.dither_algorithm(self.img, reduced_colors, h, w)
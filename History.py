from PySide6.QtCore import QObject

class History(QObject):

    def __init__(self, parent):

        super().__init__(parent)

        self.changes = 0
        self.maxChanges = -1
        self.default_settings = [8, False, 0, 0, 0, 0, 0, 0, False, 1]
        self.previewHistory = []

    def InitializeHistory(self):

        self.changes = 0
        self.maxChanges = -1

        self.previewHistory = [[
                self.parent().sliderPixelate.slider.value(),
                self.parent().checkboxResize.isChecked(),
                self.parent().sliderSmoothing.slider.value(),
                self.parent().modeComboBox.currentIndex(),
                self.parent().sliderColorcount.slider.value(),
                self.parent().sliderBrightness.slider.value(),
                self.parent().sliderContrast.slider.value(),
                self.parent().sliderSaturation.slider.value(),
                self.parent().checkboxOutline.isChecked(),
                self.parent().sliderOutline.slider.value()]]
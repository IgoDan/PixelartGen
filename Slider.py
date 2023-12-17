from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider
from PySide6.QtCore import Qt

class Slider(QWidget):

    def __init__(self, parent, min, max, base, name):
        super().__init__(parent)

        self.label = QLabel(name , alignment = Qt.AlignCenter)

        self.slider = QSlider(tickPosition = QSlider.TicksLeft, orientation = Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setValue(base)

        sliderVbox = QVBoxLayout()
        sliderVbox.setContentsMargins(0, 0, 0, 0)
        sliderVbox.setSpacing(0)

        sliderHbox = QHBoxLayout()
        sliderHbox.setContentsMargins(0, 0, 0, 0)

        labelMinimum = QLabel(str(min), alignment = Qt.AlignLeft)
        value = QLabel(str(base), alignment = Qt.AlignCenter)
        labelMaximum = QLabel(str(max), alignment = Qt.AlignRight)

        sliderVbox.addWidget(self.label)
        sliderVbox.addWidget(self.slider)
        sliderVbox.addLayout(sliderHbox)

        sliderHbox.addWidget(labelMinimum, Qt.AlignLeft)
        sliderHbox.addWidget(value, Qt.AlignCenter)
        sliderHbox.addWidget(labelMaximum, Qt.AlignRight)

        sliderVbox.addStretch()

        vbox = QVBoxLayout(self)
        vbox.addLayout(sliderVbox)

        self.setGeometry(100, 50, 300, 50)
        self.slider.valueChanged.connect(value.setNum)
        self.show()
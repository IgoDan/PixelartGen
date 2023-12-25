from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QSize

class ExportDialog(QDialog):
    
    def __init__(self, parent):

        super().__init__(parent)
        self.setWindowTitle("Custom Export")
        self.setFixedSize(200, 200)

        self.original_width = self.parent().parent().viewer.src.shape[1]
        self.original_height = self.parent().parent().viewer.src.shape[0]

        self.resolution_width = self.parent().parent().viewer.src.shape[1]
        self.resolution_height = self.parent().parent().viewer.src.shape[0]

        print(self.resolution_width, self.resolution_height)

        #RESOLUTION WIDTH LINE EDIT
        self.layout_edit_width = QHBoxLayout()

        self.label_resolution_width = QLabel("Szerokość [px]:", self)
        self.edit_resolution_width = QLineEdit(str(self.resolution_width), self)
        self.edit_resolution_width.setValidator(QIntValidator())

        self.label_resolution_width.setBuddy(self.edit_resolution_width)

        self.layout_edit_width.addWidget(self.label_resolution_width)
        self.layout_edit_width.addWidget(self.edit_resolution_width)   

        #RESOLUTION HEIGHT LINE EDIT
        self.layout_edit_height = QHBoxLayout()

        self.label_resolution_height = QLabel("Wysokość [px]:", self)
        self.edit_resolution_height = QLineEdit(str(self.resolution_height), self)
        self.edit_resolution_height.setValidator(QIntValidator())

        self.label_resolution_height.setBuddy(self.edit_resolution_height)

        self.layout_edit_height.addWidget(self.label_resolution_height)
        self.layout_edit_height.addWidget(self.edit_resolution_height)

        #KEEP ASPECT RATIO CHECKBOX
        self.checkbox_keep_aspect_ratio = QCheckBox(self,text = "Zachowaj proporcje")
        self.checkbox_keep_aspect_ratio.setFixedHeight(30)
        self.checkbox_keep_aspect_ratio.setChecked(True)
        self.checkbox_keep_aspect_ratio.show()

        self.checkbox_keep_aspect_ratio.stateChanged.connect(self.calculate_height_based_on_width)

        #SET ORIGINAL RESOLUTION BUTTON
        self.button_original_resolution = QPushButton("Oryginalna rozdzielczość", self)
        self.button_original_resolution.setFixedHeight(40)
        self.button_original_resolution.clicked.connect(self.set_original_resolution)

        #EXPORT BUTTON
        self.button_export = QPushButton("Eksportuj", self)
        self.button_export.setFixedHeight(40)
        self.button_export.clicked.connect(self.accept)

        #DIALOG LAYOUT
        layout = QVBoxLayout(self)
        layout.addLayout(self.layout_edit_width)
        layout.addLayout(self.layout_edit_height)
        layout.addWidget(self.checkbox_keep_aspect_ratio)
        layout.addWidget(self.button_original_resolution)
        layout.addWidget(self.button_export)

        self.setLayout(layout)

        #CONNECTED METHODS ON LINE EDIT TEXT CHANGE
        self.edit_resolution_width.textChanged.connect(self.calculate_height_based_on_width)
        self.edit_resolution_height.textChanged.connect(self.calculate_width_based_on_height)

    def set_original_resolution(self):

        self.edit_resolution_width.setText(str(self.original_width))
        self.edit_resolution_height.setText(str(self.original_height))

    def calculate_height_based_on_width(self):

        if self.edit_resolution_width.text() == "":
            self.resolution_width = 0
        else:
            self.resolution_width = int(self.edit_resolution_width.text())

        if self.resolution_width <= 0 or self.resolution_height <= 0:
            self.button_export.setEnabled(False)
        else:
            self.button_export.setEnabled(True)

        if self.checkbox_keep_aspect_ratio.isChecked():
            try:
                calculated_height = round((self.original_height / self.original_width) * self.resolution_width)
                self.edit_resolution_height.setText(str(calculated_height))

            except ValueError:
                pass

    def calculate_width_based_on_height(self):

        if self.edit_resolution_height.text() == "":
            self.resolution_height = 0
        else:
            self.resolution_height = int(self.edit_resolution_height.text())

        if self.resolution_width <= 0 or self.resolution_height <= 0:
            self.button_export.setEnabled(False)
        else:
            self.button_export.setEnabled(True)

        if self.checkbox_keep_aspect_ratio.isChecked():
            try:
                calculated_width = round((self.original_width / self.original_height) * self.resolution_height)
                self.edit_resolution_width.setText(str(calculated_width))

            except ValueError:
                pass

    def get_resolution(self):
        return (self.resolution_width, self.resolution_height)

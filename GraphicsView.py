from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter, QWheelEvent

class GraphicsView(QGraphicsView):

    def __init__(self, scene, parent=None):

        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)

    def wheelEvent(self, event: QWheelEvent):

        factor = 1.25

        if event.angleDelta().y() < 0:
            self.scale(1 / factor, 1 / factor)
        else:
            self.scale(factor, factor)
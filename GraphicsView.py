from PySide6.QtWidgets import QGraphicsView

from PySide6.QtGui import QPainter, QWheelEvent

class GraphicsView(QGraphicsView):

    def __init__(self, scene, parent=None):

        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)

        self.scale(self.parent().initial_zoom, self.parent().initial_zoom)
        
        self.offset = 0

    def wheelEvent(self, event: QWheelEvent):

        factor = 1.25

        if event.angleDelta().y() < 0 and self.offset > -8:
            self.scale(1 / factor, 1 / factor)
            self.offset -= 1

        elif event.angleDelta().y() > 0 and self.offset < 16:
            self.scale(factor, factor)
            self.offset += 1
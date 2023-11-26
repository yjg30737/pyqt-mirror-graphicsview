from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QImage, QPainterPath
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem


class ClippablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, side, parent=None):
        super().__init__(pixmap, parent)
        self.pixmap = pixmap
        self.side = side  # 'left' or 'right'
        self.__v = 0

    def updateClip(self, v):
        self.__v = v

    def paint(self, painter, option, widget):
        # Create a path that represents the visible area of this pixmap
        clip_path = QPainterPath()
        scene_rect = self.scene().sceneRect()

        if self.side == 'left':
            clip_rect = QRectF(QPointF(0, scene_rect.top()), QPointF(self.pixmap.width()-self.__v, scene_rect.bottom()))
            clip_path.addRect(clip_rect)
        elif self.side == 'right':
            right_left = self.pixmap.width() - self.__v
            if right_left == self.pixmap.width():
                right_left = 0
            clip_rect = QRectF(QPointF(right_left, scene_rect.top()), QPointF(self.pixmap.width(), scene_rect.bottom()))
            clip_path.addRect(clip_rect)

        painter.setClipPath(clip_path)
        super().paint(painter, option, widget)

class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__gradient_enabled = False
        self.__initVal()

    def __initVal(self):
        self._scene = QGraphicsScene()
        self._p = QPixmap()
        self._item = ''
        self.__v = 0

    def __setMirrorImage(self):
        self._p_left = QPixmap.fromImage(self._i_left)
        self._item_left = ClippablePixmapItem(self._p_left, 'left')
        self._item_left.setTransformationMode(Qt.SmoothTransformation)

        self._i_right = self._i_right.mirrored(horizontal=True, vertical=False)
        self._p_right = QPixmap.fromImage(self._i_right)
        self._item_right = ClippablePixmapItem(self._p_right, 'right')
        self._item_right.setTransformationMode(Qt.SmoothTransformation)
        self._item_right.setPos(self._item_left.x() + self._i_left.width(), 0)

        self._scene.addItem(self._item_left)
        self._scene.addItem(self._item_right)
        self.setScene(self._scene)
        self.setValue(self.__v)

    def setFilename(self, filename: str):
        self._scene = QGraphicsScene()
        self._i_left = QImage(filename)
        self._i_right = QImage(filename)
        self.__setMirrorImage()

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def hflip(self):
        self._scene.clear()
        self._i_left = self._i_left.mirrored(horizontal=True, vertical=False)
        self.__setMirrorImage()

    def setValue(self, v):
        self.__v = 0 if v / 100 == 0 else v
        left_pos = self._i_left.width() * (self.__v / 100)
        right_pos = self._i_left.width()-(self._i_left.width() * (self.__v / 100))
        self._item_left.setPos(left_pos, 0)
        self._item_right.setPos(right_pos, 0)
        self._item_left.updateClip(left_pos)
        self._item_right.updateClip(right_pos)

    def wheelEvent(self, event):
        factor = 1.1  # Zoom factor
        if event.modifiers() == Qt.ControlModifier:
            # Check if Ctrl key is pressed
            if event.angleDelta().y() > 0:
                # Ctrl + wheel up, zoom in
                self.scale(factor, factor)
            else:
                # Ctrl + wheel down, zoom out
                self.scale(1 / factor, 1 / factor)
            event.accept()  # Accept the event if Ctrl is pressed
        else:
            super().wheelEvent(event)  # Default behavior for other cases
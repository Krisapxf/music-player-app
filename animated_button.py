
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QRect, QEasingCurve


class AnimatedButton(QPushButton):
    def __init__(self, *args, animation_type=None, **kwargs):
        self.animation_type = animation_type or []
        if 'animation_type' in kwargs:
            del kwargs['animation_type']
        super().__init__(*args, **kwargs)

        if 'scale' in self.animation_type:
            self.scale_animation = QPropertyAnimation(self, b"geometry")
            self.scale_animation.setDuration(300)
            self.scale_animation.setEasingCurve(QEasingCurve.InOutQuad)
        if 'rotate' in self.animation_type:
            self.rotate_animation = QPropertyAnimation(self, b'rotation')
            self.rotate_animation.setDuration(300)
            self.rotate_animation.setEasingCurve(QEasingCurve.InOutQuad)
        if 'move' in self.animation_type:
            self.move_animation = QPropertyAnimation(self, b'geometry')
            self.move_animation.setDuration(300)
            self.move_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        if 'scale' in self.animation_type:
            self.scale_animation.stop()

            start_geometry = self.geometry()


            width_increase = int(start_geometry.width() * 0.2)
            height_increase = int(start_geometry.height() * 0.2)

            end_geometry = QRect(
                start_geometry.x() - width_increase // 2,
                start_geometry.y() - height_increase // 2,
                start_geometry.width() + width_increase,
                start_geometry.height() + height_increase
            )

            self.scale_animation.setStartValue(start_geometry)
            self.scale_animation.setEndValue(end_geometry)
            self.scale_animation.start()

        if 'rotate' in self.animation_type:
            self.rotate_animation.stop()
            start_geometry = self.geometry()
            end_geometry = start_geometry
            self.rotate_animation.setStartValue(start_geometry)
            self.rotate_animation.setEndValue(end_geometry)
            self.rotate_animation.start()
        if 'move' in self.animation_type:
            self.move_animation.stop()
            start_geometry = self.geometry()
            offset = 10
            end_geometry = start_geometry
            self.move_animation.setStartValue(start_geometry)
            self.move_animation.setEndValue(QRect(
                start_geometry.x() + offset, start_geometry.y(),
                start_geometry.width(), start_geometry.height()
            ))
            self.move_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if 'scale' in self.animation_type:
            self.scale_animation.stop()

            end_geometry = self.geometry()

            width_decrease = int(end_geometry.width() * 0.2 / 1.2)
            height_decrease = int(end_geometry.height() * 0.2 / 1.2)

            start_geometry = QRect(
                end_geometry.x() + width_decrease // 2,
                end_geometry.y() + height_decrease // 2,
                end_geometry.width() - width_decrease,
                end_geometry.height() - height_decrease
            )

            self.scale_animation.setStartValue(end_geometry)
            self.scale_animation.setEndValue(start_geometry)
            self.scale_animation.start()
        if 'rotate' in self.animation_type:
            self.rotate_animation.stop()
            start_geometry = self.geometry()
            end_geometry = start_geometry
            self.rotate_animation.setStartValue(start_geometry)
            self.rotate_animation.setEndValue(end_geometry)
            self.rotate_animation.start()
        if 'move' in self.animation_type:
            self.move_animation.stop()
            start_geometry = self.geometry()
            offset = 10
            end_geometry = start_geometry
            self.move_animation.setStartValue(start_geometry)
            self.move_animation.setEndValue(QRect(
                start_geometry.x() - offset, start_geometry.y(),
                start_geometry.width(), start_geometry.height()
            ))
            self.move_animation.start()
        super().leaveEvent(event)

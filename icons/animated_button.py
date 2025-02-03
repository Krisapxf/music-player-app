from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize

class AnimatedButton(QPushButton):
    def __init__(self, *args, animation_type=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.animation_type = animation_type or []
        if 'scale' in self.animation_type:
            self.scale_animation=QPropertyAnimation(self, b'size')
            self.scale_animation.setDuration(300)
            self.scale_animation.setEasingCurve(Qt.EaseInOutQuad)

    def enterEvent(self, event):
        if 'scale' in self.animation_type:
            self.scale_animation.stop()
            self.scale_animation.setStartValue(self.size()) 
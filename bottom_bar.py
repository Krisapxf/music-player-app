from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class BottomBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.now_playing = QLabel("Aktualnie odtwarzany utwór: Utwór 1")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")

        layout.addWidget(self.now_playing)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
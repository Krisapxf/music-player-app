from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QListWidget, QVBoxLayout


class MainSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.playlist_details = QLabel("Szczegóły playlisty")
        self.song_list = QListWidget()
        self.song_list.addItems(["Utwór 1", "Utwór 2", "Utwór 3"])

        layout.addWidget(self.playlist_details)
        layout.addWidget(self.song_list)
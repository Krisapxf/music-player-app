
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal


class LeftNav(QWidget):
    navigate = Signal(int)
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            LeftNav {
                background-color: #1e1e2f;
                border-right: 2px solid #FFC3EA;
            }
            QLabel#title_label {
                font-size: 22px;
                font-weight: bold;
                color: #FFC3EA;
                margin-bottom: 15px;
                text-align: center;
            }
            QLabel#separator {
                background-color: #FFC3EA;
                height: 2px;
                margin: 20px 0;
            }
            QPushButton {
                background-color: #2e2e3f;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                text-align: left;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #FFC3EA;
                color: #1e1e2f;
            }
            QPushButton:pressed {
                background-color: #ff9ecb;
                color: white;
            }
        """)


        layout = QVBoxLayout()
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(15)
        self.setLayout(layout)

        title_label = QLabel("Navigation")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.favourites_button = self.create_nav_button("Favourites")
        self.favourites_button.setIcon(QIcon("icons/lover.png"))
        self.library_button = self.create_nav_button("Library")
        self.library_button.setIcon(QIcon("icons/bookshelf.png"))
        self.history_button = self.create_nav_button("History")
        self.history_button.setIcon(QIcon("icons/history.png"))
        self.uploadfile_button = self.create_nav_button("Upload File")
        self.uploadfile_button.setIcon(QIcon("icons/music-2.png"))
        self.user_button = self.create_nav_button("User")
        self.user_button.setIcon(QIcon("icons/log-out.png"))

        separator = QLabel()
        separator.setObjectName("separator")
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #FFC3EA;")

        layout.addWidget(self.favourites_button)
        layout.addWidget(self.library_button)
        layout.addWidget(self.history_button)
        layout.addWidget(separator)
        layout.addWidget(self.uploadfile_button)
        layout.addWidget(self.user_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        
        self.favourites_button.clicked.connect(lambda: self.navigate.emit(0))
        self.library_button.clicked.connect(lambda: self.navigate.emit(1))
        self.history_button.clicked.connect(lambda: self.navigate.emit(2))
        self.uploadfile_button.clicked.connect(lambda: self.navigate.emit(3))
        self.user_button.clicked.connect(lambda: self.navigate.emit(4))
        
    def create_nav_button(self, text):
        button = QPushButton(text)
        button.setFixedSize(200, 50)
        button.setCursor(Qt.PointingHandCursor)
        return button

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from database_manager import DatabaseManager
from globals import globals

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()
        self.setWindowTitle("Playback History")
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFC3EA;
                padding: 10px;
                border-bottom: 2px solid #FFC3EA;
                text-align: center;
            }

            QListWidget {
                background-color: #2b2b3b;
                border: 1px solid #444;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                margin: 10px;
            }

            QListWidget::item {
                padding: 12px 10px;
                margin: 5px;
                border-radius: 8px;
            }

            QListWidget::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #444, stop: 1 #555);
                color: #FFC3EA;
            }

            QListWidget::item:selected {
                background-color: #FFC3EA;
                color: #2b2b3b;
                border: 1px solid #FFC3EA;
            }
        """)


        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        header = QLabel("Playback History")
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)

        self.load_history()

    def load_history(self):
        self.history_list.clear()
        
        history = self.db_manager.get_all_songs()
        
        if history:
            for record in history:
                item_text = f"Song: {record[1]} - {record[2]} (Last played: {record[4]})"
                icon = QIcon("icons/music-4.png")
                item = QListWidgetItem(icon, item_text)
                self.history_list.addItem(item)
        else:
            empty_item = QListWidgetItem("No playback history available.")
            self.history_list.addItem(empty_item)


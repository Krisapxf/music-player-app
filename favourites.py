from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from database_manager import DatabaseManager
from globals import globals

class Favourites(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)
        header = QLabel("Favourite Songs")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #FFC3EA;
        """)
        layout.addWidget(header, alignment=Qt.AlignCenter)

        self.favourites_list = QListWidget()
        layout.addWidget(self.favourites_list)

        self.favourites_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b3b;
                border: 2px solid #FFC3EA;
                border-radius: 12px;
                color: white;
                font-size: 15px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px;
                margin: 5px 0;
                border-radius: 8px;
                background-color: #3b3b4f;
                border: 1px solid #444;
                color: white;
            }
            QListWidget::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #444, stop: 1 #555);
                border: 1px solid #FFC3EA;
                color: #FFC3EA;
            }
            QListWidget::item:selected {
                background-color: #FFC3EA;
                color: #2b2b3b;
                border: 1px solid #FFC3EA;
            }
        """)

        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFC3EA;
                margin-bottom: 15px;
                text-align: center;
            }
        """)


        self.setLayout(layout)
        self.load_favourites()


        

    def load_favourites(self):
        if not globals.logged_in or not globals.user_email:
            print("User not logged in. Cannot load favourites.")
            item = QListWidgetItem("Please log in to see your favourite songs.")
            self.favourites_list.addItem(item)
            return
        self.favourites_list.clear()
        useremail = globals.user_email
        userid = globals.user_id
        print(userid, useremail)
        if userid:
            print("try to get favourites")
            favourites = self.db_manager.get_favourite_songs(userid)
            print(f"Favourites fetched: {favourites}")

            if favourites:
                for song in favourites:
                    title = song[2] 
                    item = QListWidgetItem(title)
                    item.setIcon(QIcon("icons/heart-2.png")) 
                    self.favourites_list.addItem(item)
            else:
                item = QListWidgetItem("No favourite songs yet")
                self.favourites_list.addItem(item)
            self.favourites_list.repaint()
        else:
            print("User not logged in. Cannot load favourites.")
            item = QListWidgetItem("Please log in to see your favourite songs.")
            self.favourites_list.addItem(item)

    


            
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from database_manager import DatabaseManager
from globals import globals


class PlaylistManager(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()
        self.setWindowTitle("Playlist Manager")
        self.playlist_id = None  
        self.playlist_title = "" 

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            QLineEdit {
                padding: 8px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #2c2c3e;
                color: white;
            }

            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: #3b3b4f;
            }

            QPushButton:hover {
                background-color: #4b4b6f;
            }

            QListWidget {
                background-color: #2c2c3e;
                border: 1px solid #555;
                border-radius: 5px;
                color: white;
            }

            QListWidget::item {
                padding: 10px;
            }

            QListWidget::item:selected {
                background-color: #444;
                color: #FFC3EA;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        header = QLabel("Playlists")
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

        self.playlist_name_input = QLineEdit()
        self.playlist_name_input.setPlaceholderText("Enter playlist name")

        create_playlist_button = QPushButton("Create Playlist")
        create_playlist_button.clicked.connect(self.create_playlist)

        create_layout = QHBoxLayout()
        create_layout.addWidget(self.playlist_name_input)
        create_layout.addWidget(create_playlist_button)

        self.layout.addLayout(create_layout)

        self.playlist_list = QListWidget()
        self.playlist_list.itemClicked.connect(self.view_playlist)

        self.layout.addWidget(self.playlist_list)
        self.load_playlists()

        self.songs_list = QListWidget()
        self.layout.addWidget(self.songs_list)


        available_songs_label = QLabel("Available Songs")
        self.layout.addWidget(available_songs_label)

        self.available_songs_list = QListWidget()
        self.layout.addWidget(self.available_songs_list)


        add_button = QPushButton("Add to Playlist")
        add_button.clicked.connect(self.add_to_playlist)
        self.layout.addWidget(add_button)

        self.load_songs()
        self.load_available_songs()

    def load_playlists(self):
        print("Loading playlists...")  
        self.playlist_list.clear()
        if not globals.logged_in or not globals.user_id:
            print("User not logged in. Cannot load playlists.")
            return
        
        playlists = self.db_manager.get_playlist(globals.user_id)
        print(f"Playlists fetched from DB: {playlists}")  

        if playlists:
            for playlist in playlists:
                print(f"Adding playlist: {playlist}")  
                item = QListWidgetItem(playlist[1]) 
                item.setData(Qt.UserRole, playlist[0]) 
                item.setIcon(QIcon("icons/music-3.png"))
                self.playlist_list.addItem(item)
        else:
            print("No playlists available.")  
            empty_item = QListWidgetItem("No playlists available.")
            self.playlist_list.addItem(empty_item)


    def create_playlist(self):
        title = self.playlist_name_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Error", "Playlist name cannot be empty.")
            return
        try:
            self.db_manager.create_playlist(title, globals.user_id)
            QMessageBox.information("created successfully.")
            self.load_playlists()
            self.playlist_name_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create playlist: {e}")

    def view_playlist(self, item):
        self.playlist_id = item.data(Qt.UserRole)  
        self.playlist_title = item.text()         

        print(f"Selected playlist: {self.playlist_title} (ID: {self.playlist_id})")  
        self.load_songs()  


    def load_available_songs(self):
        self.available_songs_list.clear()
        songs = self.db_manager.get_all_songs()  
        if songs:
            for song in songs:
                print(f"Adding song to available list: {song}") 
                if isinstance(song[1], str):
                    item = QListWidgetItem(song[1]) 
                    item.setData(Qt.UserRole, song[0])  
                    item.setIcon(QIcon("icons/music-3.png"))
                    self.available_songs_list.addItem(item)
                else:
                    print(f"Invalid song title type: {type(song[1])}")  
        else:
            empty_item = QListWidgetItem("No songs available.")
            self.available_songs_list.addItem(empty_item)


    def load_songs(self):
        self.songs_list.clear()
        songs = self.db_manager.get_playlist_songs(self.playlist_id)  
        print(f"Songs fetched for playlist {self.playlist_id}: {songs}")  

        if songs:
            for song in songs:
                print(f"Adding song: {song}")  
                item = QListWidgetItem(song[2])  
                item.setIcon(QIcon("icons/music-3.png"))  
                self.songs_list.addItem(item)
        else:
            empty_item = QListWidgetItem("No songs in this playlist.")
            self.songs_list.addItem(empty_item)


    def add_to_playlist(self):
        selected_items = self.available_songs_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No song selected to add.")
            return

        try:
            for item in selected_items:
                song_id = item.data(Qt.UserRole)
                self.db_manager.add_song_to_playlist(self.playlist_id, song_id)

            QMessageBox.information(self, "Success", "Selected songs added to the playlist.")
            self.load_songs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add songs to the playlist: {e}")

# class PlaylistDetails(QWidget):
#     def __init__(self, playlist_id, playlist_title):
#         super().__init__()

#         self.playlist_id = playlist_id
#         self.playlist_title = playlist_title
#         self.db_manager = DatabaseManager()

#         self.setWindowTitle(f"Playlist: {playlist_title}")
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #1e1e2f;
#                 color: white;
#                 font-family: Arial, sans-serif;
#                 font-size: 14px;
#             }
#         """)

#         self.layout = QVBoxLayout()

#         self.init_ui()
#         self.setLayout(self.layout)

#     def init_ui(self):
#         header = QLabel(f"Songs in '{self.playlist_title}'")
#         header.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(header)

#         self.songs_list = QListWidget()
#         self.layout.addWidget(self.songs_list)

#         self.load_songs()

#     def load_songs(self):
#         self.songs_list.clear()
#         songs = self.db_manager.get_playlist_songs(self.playlist_id)
#         if songs:
#             for song in songs:
#                 item = QListWidgetItem(song[2])  
#                 item.setIcon(QIcon("icons/music.png"))
#                 self.songs_list.addItem(item)
#         else:
#             empty_item = QListWidgetItem("No songs in this playlist.")
#             self.songs_list.addItem(empty_item)

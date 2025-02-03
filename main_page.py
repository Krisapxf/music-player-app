from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from database_manager import DatabaseManager
from globals import globals
from PySide6.QtGui import QPixmap

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()
        self.setWindowTitle("Main Page")
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
                text-align: center;
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

            /* Styl kafelków */
            QWidget#tile {
                background-color: #282a36;
                border: 1px solid #3b3b4f;
                border-radius: 10px;
                padding: 10px;
            }

            QWidget#tile:hover {
                background-color: #343746;
                border: 1px solid #4b4b6f;
            }

            QLabel#title_label {
                font-size: 18px;
                font-weight: bold;
                color: #FFC3EA;
            }

            QPushButton#play_button {
                background-color: #3b3b4f;
                border-radius: 5px;
                font-size: 14px;
                color: white;
            }

            QPushButton#play_button:hover {
                background-color: #4b4b6f;
            }
            """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.add_logo()

        header = QLabel("Your Playlists")
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.load_playlists()
        self.add_favourites_tile()

    def add_logo(self):
        logo_label = QLabel()
        pixmap = QPixmap("icons/fff.png")  
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(logo_label)

    def load_playlists(self):
        print("Loading playlists... in MainPage")
        playlists = self.db_manager.get_playlist(globals.user_id)
        if playlists:
            row, col = 0, 0
            for playlist in playlists:
                print(playlist)
                playlist_id, title = playlist[0], playlist[1]
                self.add_playlist_tile(title, playlist_id, row, col)

                col += 1
                if col > 2:  # 3 kafelki w wierszu
                    col = 0
                    row += 1
        else:
            print("No playlists found")

    def add_playlist_tile(self, title, playlist_id, row, col):
        tile = QWidget()
        tile.setObjectName("tile")
        tile_layout = QVBoxLayout()
        tile.setLayout(tile_layout)

        title_label = QLabel(title)
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)

        play_button = QPushButton("Play")
        play_button.setObjectName("play_button")
        play_button.setIcon(QIcon("icons/play-4.png"))
        play_button.clicked.connect(lambda: self.play_playlist(playlist_id, title))

        tile_layout.addWidget(title_label)
        tile_layout.addWidget(play_button)

        self.grid_layout.addWidget(tile, row, col)

    def add_favourites_tile(self):
        tile = QWidget()
        tile.setObjectName("tile")
        tile_layout = QVBoxLayout()
        tile.setLayout(tile_layout)

        title_label = QLabel("Favourites")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)

        play_button = QPushButton("Play")
        play_button.setObjectName("play_button")
        play_button.setIcon(QIcon("icons/play-3.png"))
        play_button.clicked.connect(self.play_favourites)

        tile_layout.addWidget(title_label)
        tile_layout.addWidget(play_button)

        self.grid_layout.addWidget(tile, 0, 0)  

    # def play_playlist(self, playlist_id, title):
    #     print(f"Playing playlist: {title} (ID: {playlist_id})")
    #     songs = self.db_manager.get_playlist_songs(playlist_id)
    #     globals.playing_playlist_id=playlist_id
    #     info=self.db_manager.get_playlist_info_by_id(playlist_id)
    #     globals.playing_playlist_name=info[1]
    #     globals.playing_playlist_songs=songs
    #     print(f"Loaded songs: {songs}")
    #     if songs:
    #         for song in songs:
    #             print(song)
    #     else:
    #         print("No songs in playlist")
        
    # def play_selected_song(self, item):
    #     print("Playing selected song...")
    #     selected_song=item.text()
    #     selected_song=selected_song.split(" - ")
    #     for i in range(len(selected_song)):
    #         selected_song[i]=selected_song[i].strip()
    #     globals.playing=True
    #     globals.playing_track=selected_song[0]
    #     globals.playing_artist=selected_song[1]
    #     db=DatabaseManager()
    #     selected_song=db.get_song_by_title_artist(selected_song[0], selected_song[1])
    #     globals.playing_track_id=selected_song[0]
    #     globals.playing_file_path=selected_song[3]
    #     print(globals.playing_track, globals.playing_track_id, globals.playing_file_path)


    def play_favourites(self):
        print("Playing favourites")


    # def load_playlist(self , playlist_id):
    #     print(f"Loading playlist: {playlist_id}")
    #     songs = self.db_manager.get_playlist_songs(playlist_id)
    #     globals.playing_playlist_id=playlist_id
    #     info=self.db_manager.get_playlist_info_by_id(playlist_id)
    #     globals.playing_playlist_name=info[1]
    #     globals.playing_playlist_songs=songs
    #     print(f"Loaded songs: {songs}")
    #     if songs:
    #         self.playlist_widget.clear()
    #         for song in songs:
    #             self.playlist_widget.addItem(f"{song[1]} - {song[2]}")
    #     else:
    #         print("No songs in playlist")
    
    def play_track(self, track):
        globals.playing_track = track["title"]
        # globals.playing=True
        # globals.playing_track=selected_song[0]
        # globals.playing_artist=selected_song[1]
        # db=DatabaseManager()
        # selected_song=db.get_song_by_title_artist(selected_song[0], selected_song[1])
        # globals.playing_track_id=selected_song[0]
        # globals.playing_file_path=selected_song[3]
        # print(globals.playing_track, globals.playing_track_id, globals.playing_file_path)

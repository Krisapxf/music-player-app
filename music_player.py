
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QFileDialog, QHBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, QSize, Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QMediaDevices
from globals import globals
from database_manager import DatabaseManager
from PySide6.QtCore import QTimer
from favourites import Favourites
from User import User
from playlist_manager import PlaylistManager
from main_page import MainPage
from history import HistoryPage
from user_interface import UserInterface

# dostępne urządzenia audio
devices = QMediaDevices.audioOutputs()
print("Available audio devices:")
for device in devices:
    print(device.description())





class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 1000, 100)
        self.db_manager = DatabaseManager()
        self.favourites_widget = Favourites()
        self.playlist_widget = PlaylistManager()
        self.main_page_widget = MainPage()
        self.history_widget = HistoryPage()
        self.user_interface= UserInterface()
        self.user_widget = User(self.favourites_widget, self.playlist_widget, self.main_page_widget, self.history_widget, self.user_interface)
        self.current_track = None
        self.is_playing = False
        self.current_playlist = []

        self.listener_timer = QTimer()
        self.listener_timer.setInterval(500)
        self.listener_timer.timeout.connect(self.check_globals)
        self.listener_timer.start()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QPushButton {
                border: none;
                border-radius: 20px;
                padding: 10px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }

            QSlider::groove:horizontal {
                border: 1px solid #4c4c6f;
                background-color: #3c3c4f;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background-color: #ffa7c4;
                border: 1px solid #7e7e9d;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }

            QSlider::handle:horizontal:hover {
                background-color: #ffc4e0;
            }

            QLabel {
                color: #ffffff;
                font-size: 12px;
            }

            QLabel#track_label {
                font-size: 18px;
                font-weight: bold;
                color: #ffa726;
                padding: 5px;
                border-bottom: 2px solid #3b3b4f;
            }

            QLabel#track_artist {
                font-size: 14px;
                color: gray;        
            }

            QLabel#track_title {
                font-size: 18px;
                font-weight: bold;         
            }
        """)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.smooth_update_position)
        self.duration = 0
        self.playing = False

        self.track_cover = QLabel()
        self.track_cover.setPixmap(QPixmap("icons/woman.png").scaled(60, 60, Qt.KeepAspectRatio))
        self.track_title = QLabel("Dance Monkey")
        self.track_artist = QLabel("The Neighbourhood")

        self.play_button = HoverButton()
        self.play_button.setIcon(QIcon("icons/play-3.png"))
        self.open_button = HoverButton()
        self.open_button.setIcon(QIcon("icons/music-4.png"))
        self.volume_icon = HoverButton()
        self.volume_icon.setIcon(QIcon("icons/volume.png"))
        self.prev_button = HoverButton()
        self.prev_button.setIcon(QIcon("icons/previous-2.png"))
        self.next_button = HoverButton()
        self.next_button.setIcon(QIcon("icons/next-button-2.png"))
        self.shuffle_button = HoverButton()
        self.shuffle_button.setIcon(QIcon("icons/shuffle.png"))
        self.repeat_button = HoverButton()
        self.repeat_button.setIcon(QIcon("icons/reuse.png"))
        self.heart_button = HoverButton()
        self.heart_button.setIcon(QIcon("icons/heart.png"))
        self.liked = False
        self.volume_slider = QSlider(Qt.Horizontal)

        icon_size = QSize(32, 32)
        for button in [self.play_button, self.open_button, self.volume_icon, self.prev_button,
                       self.next_button, self.shuffle_button, self.repeat_button, self.heart_button]:
            button.setIconSize(icon_size)
            button.setFlat(True)
            button.setText("")

        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.time_slider = CustomSlider(Qt.Horizontal)
        self.time_slider.setRange(0, 10000)
        self.time_slider.sliderMoved.connect(self.set_scaled_position)
        self.time_label_current = QLabel("00:00")
        self.time_label_duration = QLabel("00:00")

        self.create_layout()

    def create_layout(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)

        left_layout = QVBoxLayout()
        picture_layout = QHBoxLayout()
        picture_layout.addWidget(self.track_cover, alignment=Qt.AlignCenter)
        picture_layout.addWidget(self.heart_button, alignment=Qt.AlignCenter)
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.track_title)
        info_layout.addWidget(self.track_artist)
        left_layout.addLayout(picture_layout)
        left_layout.addLayout(info_layout)
        left_layout.setSpacing(5)

        center_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)
        button_layout.addWidget(self.open_button)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_label_current)
        time_layout.addWidget(self.time_slider, stretch=1)
        time_layout.addWidget(self.time_label_duration)

        center_layout.addLayout(button_layout)
        center_layout.addLayout(time_layout)

        right_layout = QHBoxLayout()
        right_layout.addWidget(self.volume_icon)
        right_layout.addWidget(self.volume_slider)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout, stretch=2)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.open_button.clicked.connect(self.open_file1)
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.player.errorOccurred.connect(self.handle_error)

        self.heart_button.clicked.connect(self.toggle_liked)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        self.timer.start()

    def open_file(self):
        file_path=globals.playing_file_path
        if file_path:
            self.player.setSource(QUrl.fromLocalFile(file_path))  
            self.track_title.setText(globals.playing_track)
            self.track_artist.setText(globals.playing_artist)
            self.db_manager.update_playback_history( globals.playing_track_id)
            print(f"Opening file: {file_path}")
        else:
            print("No file path specified")
        if self.is_favourite_song(globals.user_id, self.track_title.text()):
            self.heart_button.setIcon(QIcon("icons/heart-2.png"))
            self.liked = True
            print("Song is liked")
        else:
            self.heart_button.setIcon(QIcon("icons/heart.png"))
            self.liked = False
            print("Song is not liked")
    
    def open_file1(self):
        file_path, _=QFileDialog.getOpenFileName(self, "Open file", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.track_title.setText(file_path.split("/")[-1])
            globals.playing_file_path = file_path
            globals.playing=True



    def set_volume(self, value):
        print(f"Setting volume: {value}")
        self.player.audioOutput().setVolume(value / 100)

    def update_position(self, position):
        if self.duration > 0:
            scaled_position = (position / self.duration) * 10000
            self.time_slider.blockSignals(True)
            self.time_slider.setValue(int(scaled_position))
            self.time_slider.blockSignals(False)
            self.time_label_current.setText(self.format_time(position))

    def update_duration(self, duration):
        self.duration = duration
        self.time_slider.setRange(0, 10000)
        self.time_label_duration.setText(self.format_time(duration))

    def set_scaled_position(self, relative_position):
        if self.duration > 0:
            position = (relative_position / 10000) * self.duration
            self.player.setPosition(int(position))

    def toggle_play_pause(self):
        if globals.playing:
            globals.playing = False
            self.player.pause()
            self.play_button.setIcon(QIcon("icons/play-3.png"))
            print("pasuing")
        else:
            self.play_button.setIcon(QIcon("icons/stop-2.png"))
            print("playing in toogle-playing")
            self.player.play()
            globals.playing = True
        self.playing = not self.playing

    def check_globals(self):
        if globals.playing_track != self.current_track:
            self.current_track = globals.playing_track
            if globals.playing:
                print(f"Now playing new track: {self.current_track}")
                self.open_file()  
                self.player.play()  
                self.play_button.setIcon(QIcon("icons/stop-2.png"))
                self.is_playing = True
            else:
                print("No track specified in globals")

        elif globals.playing != self.is_playing:
            if globals.playing:
                print("Resuming playback")
                self.player.play()
                self.play_button.setIcon(QIcon("icons/stop-2.png"))
            else:
                print("Pausing playback")
                self.player.pause()
                self.play_button.setIcon(QIcon("icons/play-3.png"))
            self.is_playing = globals.playing


    def is_favourite_song(self, user_id, song_title):
        favourite_songs = self.db_manager.get_favourite_songs(user_id)
        for song in favourite_songs:
            if song[2] == song_title:
                return True
        return False


    def toggle_liked(self):
        print("Toggling liked")
        if globals.user_id:
            try:
                if self.liked:
                    self.db_manager.remove_favourite_song(globals.user_id, globals.playing_track)
                    self.heart_button.setIcon(QIcon("icons/heart.png"))  
                    print("Removed from favourites")
                    if self.favourites_widget:
                        self.favourites_widget.load_favourites()
                else:
                    self.db_manager.add_favourite_song(globals.user_id, globals.playing_track)
                    self.heart_button.setIcon(QIcon("icons/heart-2.png"))  
                    print(f"Added to favourites: {globals.playing_track}")
                    if self.favourites_widget:
                        self.favourites_widget.load_favourites()
                self.liked = not self.liked
            except Exception as e:
                print(f"Error toggling favourite status: {e}")

    @staticmethod
    def format_time(milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def smooth_update_position(self):
        position = self.player.position()
        self.update_position(position)

    def handle_error(self, error, error_string):
        print(f"Error: {error} - {error_string}")

    # playing_playlist_id=None
    # playing_playlist_name=None
    # playing_playlist_songs=[]
    # playing_playlist_index_of_song=None

    def load_playlist(self , playlist_id):
        print(f"Loading playlist: {playlist_id}")
        songs = self.db_manager.get_playlist_songs(playlist_id)
        globals.playing_playlist_id=playlist_id
        info=self.db_manager.get_playlist_info_by_id(playlist_id)
        globals.playing_playlist_name=info[1]
        globals.playing_playlist_songs=songs
        print(f"Loaded songs: {songs}")
        if songs:
            self.playlist_widget.clear()
            for song in songs:
                self.playlist_widget.addItem(f"{song[1]} - {song[2]}")
        else:
            print("No songs in playlist")
    
    def play_track(self, track):
        globals.playing_track = track["title"]


class CustomSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            new_position = event.pos().x() / self.width()
            value = int(new_position * (self.maximum() - self.minimum()))
            self.setValue(value)
            self.sliderMoved.emit(value)
        super().mousePressEvent(event)


class HoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_size = QSize(32, 32)
        self.max_size = QSize(40, 40)
        self.setMinimumSize(self.default_size)
        self.setMaximumSize(self.max_size)
        self.hover_increase = 10
        self.setIconSize(QSize(32, 32))
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(100)
        self.setFlat(True)

    def enterEvent(self, event):
        self.animate_button(self.default_size.width() + self.hover_increase,
                            self.default_size.height() + self.hover_increase)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_button(self.default_size.width(),
                            self.default_size.height())
        super().leaveEvent(event)

    def animate_button(self, new_width, new_height):
        self.animation.stop()
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(QSize(new_width, new_height))
        self.animation.start()




if __name__ == "__main__":
    app = QApplication([])
    window = MusicPlayer()
    window.show()
    app.exec()


        
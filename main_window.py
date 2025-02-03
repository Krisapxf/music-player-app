
from top_bar import TopBar
from left_nav import LeftNav
# from right_nav import RightNav
from main_section import MainSection
from bottom_bar import BottomBar
from music_player import MusicPlayer
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QGridLayout, QStackedLayout, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from user_interface import UserInterface
from favourites import Favourites
from User import User
from FileUploader import FileUploader
from playlist_manager import PlaylistManager
from main_page import MainPage
from history import HistoryPage



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.navigation_history = []


        self.setStyleSheet("""QMainWindow {
            background-color: #1e1e2f; 
            color: #ffffff;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }

        #TopBar {
            background-color: #2c2c3e;
            border-bottom: 1px solid #3b3b4f;
            padding: 10px;
        }

        #TopBar QPushButton {
            background-color: transparent;
            border: none;
            color: #ffa7c4;
            font-size: 16px;
            font-weight: bold;
        }

        #TopBar QPushButton:hover {
            color: #ffc4e0;
        }

        #TopBar QLineEdit {
            background-color: #3b3b4f;
            border: 1px solid #5e5e7d;
            border-radius: 5px;
            padding: 5px;
            color: #ffffff;
        }

        #LeftNav {
            background-color: #2c2c3e;
            border-right: 1px solid #3b3b4f;
            padding: 10px;
        }

        #LeftNav QPushButton {
            background-color: #3c3c4f;
            border: none;
            border-radius: 5px;
            padding: 10px;
            color: #ffffff;
            font-size: 14px;
            text-align: left;
        }

        #LeftNav QPushButton:hover {
            background-color: #4c4c6f;
        }

        #LeftNav QPushButton:pressed {
            background-color: #5e5e7d;
        }

        #MainSection {
            background-color: #2e2e40;
            border-radius: 5px;
            padding: 10px;
        }

        #MainSection QLabel {
            color: #ffffff;
            font-size: 14px;
        }

        #MainSection QListWidget {
            background-color: #3c3c4f;
            border: 1px solid #5e5e7d;
            border-radius: 5px;
            color: #ffffff;
            font-size: 14px;
            padding: 5px;
        }

        #MainSection QListWidget::item {
            padding: 10px;
        }

        #MainSection QListWidget::item:hover {
            background-color: #4c4c6f;
        }

        #MainSection QListWidget::item:selected {
            background-color: #5e5e7d;
            color: #ffffff;
        }

        #BottomBar {
            background-color: #2c2c3e;
            border-top: 1px solid #3b3b4f;
            padding: 10px;
        }

        #BottomBar QPushButton {
            background-color: transparent;
            border: none;
            color: #ffa7c4;
            font-size: 16px;
            font-weight: bold;
        }

        #BottomBar QPushButton:hover {
            color: #ffc4e0;
        }

        #BottomBar QSlider::groove:horizontal {
            border: 1px solid #3b3b4f;
            background-color: #3c3c4f;
            height: 8px;
            border-radius: 4px;
        }

        #BottomBar QSlider::handle:horizontal {
            background-color: #ffa7c4;
            border: 1px solid #7e7e9d;
            width: 16px;
            height: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }

        #BottomBar QSlider::handle:horizontal:hover {
            background-color: #ffc4e0;
        }

        #BottomBar QLabel {
            color: #ffffff;
            font-size: 12px;
        }

        QPushButton {
            border-radius: 20px;
            padding: 5px;
        }

        """)

        self.setWindowTitle("Better Spotify")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)

        self.top_bar = TopBar(self)
        self.left_nav = LeftNav()
        self.pages = QStackedWidget()
        self.main_section = MainSection()
        self.bottom_bar = MusicPlayer()

        main_layout.addWidget(self.top_bar, 0, 0, 1, 3)
        main_layout.addWidget(self.left_nav, 1, 0, 1, 1)
        main_layout.addWidget(self.pages, 1, 1, 1, 2)
        main_layout.addWidget(self.bottom_bar, 2, 0, 1, 3)

        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 6)

        # PODSTRONY
        self.favourite_page = Favourites()
        self.library_page = PlaylistManager()
        self.history_page = HistoryPage()
        self.upload_file_page = FileUploader()
        self.user_page= UserInterface()
        self.home=MainPage()
        self.login_page=User(self.favourite_page, self.library_page, self.home, self.history_page, self.user_page)


        self.pages.addWidget(self.favourite_page) # Index 0
        self.pages.addWidget(self.library_page)  # 1
        self.pages.addWidget(self.history_page)#2
        self.pages.addWidget(self.upload_file_page)#3
        self.pages.addWidget(self.user_page)#4
        self.pages.addWidget(self.login_page)#5
        self.pages.addWidget(self.home) #6



        main_layout.replaceWidget(self.main_section, self.pages)
        self.left_nav.navigate.connect(self.switch_page)
        self.top_bar.navigate.connect(self.switch_page)
        self.login_page.navigate.connect(self.switch_page)


    def create_home_page(self):
        home_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your Home"))
        home_page.setLayout(layout)
        return home_page

    def create_favourite_page(self):
        favourite_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your Favouriteeee Songs"))
        favourite_page.setLayout(layout)
        return favourite_page

    def create_playlist_page(self):
        playlist_page = QWidget()
        layout = QVBoxLayout()
        playlist_page.setLayout(layout)
        return playlist_page
    def create_library_page(self):
        library_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your Library"))
        library_page.setLayout(layout)
        return library_page
    
    def create_history_page(self):
        history_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your History"))
        history_page.setLayout(layout)
        return history_page
    
    def create_uploadfile_page(self):
        settings_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("uploadign file"))
        settings_page.setLayout(layout)
        return settings_page
    
    def create_user_page(self):
        user_page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your User"))
        user_page.setLayout(layout)
        return user_page
    
    def switch_page(self, index):
        self.navigation_history.append(self.pages.currentIndex())
        self.pages.setCurrentIndex(index)

    def go_back(self):
        print("Going back...")
        if len(self.navigation_history) > 1:
            self.navigation_history.pop()  
            previous_page = self.navigation_history[-1] 
            self.pages.setCurrentIndex(previous_page)  
        else:
            print("No previous")

    def go_forward(self):
        current_index = self.pages.currentIndex()
        if current_index < self.pages.count() - 1:
            self.pages.setCurrentIndex(current_index + 1)
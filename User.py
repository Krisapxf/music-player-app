import sqlite3
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QListWidget, QVBoxLayout, QMainWindow, QLineEdit
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from database_manager import DatabaseManager
from globals import globals
from favourites import Favourites
from playlist_manager import PlaylistManager
from main_page import MainPage
from history import HistoryPage
from PySide6.QtCore import Signal

class User(QMainWindow):
    navigate = Signal(int)
    def __init__(self, favourites_widget, playlist_manager, main_pagger, history_page, user_page):
        super().__init__()
        self.setWindowTitle("logowanie")
        self.setGeometry(100, 100, 800, 600)
        self.db_manager=DatabaseManager()
        self.favourites_widget = favourites_widget 
        self.playlist_manager = playlist_manager
        self.main_pagger=main_pagger
        self.history_page=history_page
        self.user_page=user_page

        self.login_screen()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QLabel {
                color: #ffa7c4;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }

            QLineEdit {
                background-color: #2e2e3f;
                border: 1px solid #ffa7c4;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #820940;
                background-color: #3c3c4f;
            }

            QPushButton {
                background-color: #1e1e2f;
                color: black;
                border: none;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                margin-top: 10px;
                width:250px;
            }
            QPushButton:hover {
                background-color:  #820940;
            }
            QPushButton:pressed {
                background-color:  #820940;
            }


            QListWidget {
                background-color: #2e2e3f;
                border: none;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QListWidget::item {
                padding: 10px;
                margin: 5px 0;
                background-color: #3c3c4f;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #444455;
                color: #FFA726;
            }
        """)



    def login_screen(self):
        self.clear_layout()
        login_widget=QWidget()
        layout=QVBoxLayout(login_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        layout.setSpacing(5)
        self.setCentralWidget(login_widget)


        layout_login=QHBoxLayout()
        layout_login.setContentsMargins(0,0,0,0)
        layout_login.setSpacing(5)
        layout_login.setAlignment(Qt.AlignLeft)
        icon_label_login = QLabel()
        icon_label_login.setPixmap(QPixmap("icons/user.png").scaled(40, 40)) 
        text_label_login = QLabel("Email")
        self.login_input=QLineEdit()
        self.login_input.setPlaceholderText("Login")
        layout_login.addWidget(icon_label_login)
        layout_login.addWidget(text_label_login)
        layout.addLayout(layout_login)
        layout.addWidget(self.login_input)
        layout.setSpacing(5)
        
        layout_password=QHBoxLayout()
        layout_password.setContentsMargins(0,0,0,0)
        layout_password.setSpacing(5)
        layout_password.setAlignment(Qt.AlignLeft)
        icon_label_password = QLabel()
        icon_label_password.setPixmap(QPixmap("icons/padlock.png").scaled(40, 40)) 
        text_label_password = QLabel("Hasło")
        self.password_input=QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Hasło")
        layout_password.addWidget(icon_label_password)
        layout_password.addWidget(text_label_password)
        layout.addLayout(layout_password)
        layout.addWidget(self.password_input)
        layout.setSpacing(5)


        login_button=QPushButton("Zaloguj")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        login_button.setIcon(QIcon(QPixmap("icons/enter.png")))

        additional_button1=QPushButton("Zarejestruj")
        additional_button1.clicked.connect(self.register_screen)
        layout.addWidget(additional_button1)
        additional_button1.setIcon(QIcon(QPixmap("icons/register.png")))

        login_button.setFixedSize(200, 50)
        additional_button1.setFixedSize(200, 50)
        self.login_input.setFixedSize(200, 40)
        self.password_input.setFixedSize(200, 40)

        self.setCentralWidget(login_widget)

    def register_screen(self):
        self.clear_layout()
        register_widget=QWidget()
        layout=QVBoxLayout(register_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        layout.setSpacing(5)
        self.setCentralWidget(register_widget)


        layout_login=QHBoxLayout()
        layout_login.setContentsMargins(0,0,0,0)
        layout_login.setSpacing(5)
        layout_login.setAlignment(Qt.AlignLeft)
        icon_label_login = QLabel()
        icon_label_login.setPixmap(QPixmap("icons/user.png").scaled(40, 40)) 
        text_label_login = QLabel("User name")
        self.register_username_input=QLineEdit()
        self.register_username_input.setPlaceholderText("User name")
        layout_login.addWidget(icon_label_login)
        layout_login.addWidget(text_label_login)
        layout.addLayout(layout_login)
        layout.addWidget(self.register_username_input)
        layout.setSpacing(5)
        
        layout_email=QHBoxLayout()
        layout_email.setContentsMargins(0,0,0,0)
        layout_email.setSpacing(5)
        layout_email.setAlignment(Qt.AlignLeft)
        icon_label_email = QLabel()
        icon_label_email.setPixmap(QPixmap("icons/message.png").scaled(40, 40)) 
        text_label_email = QLabel("Email")
        self.register_email_input=QLineEdit()
        self.register_email_input.setPlaceholderText("Email")
        layout_email.addWidget(icon_label_email)
        layout_email.addWidget(text_label_email)
        layout.addLayout(layout_email)
        layout.addWidget(self.register_email_input)
        layout.setSpacing(5)


        layout_password=QHBoxLayout()
        layout_password.setContentsMargins(0,0,0,0)
        layout_password.setSpacing(5)
        layout_password.setAlignment(Qt.AlignLeft)
        icon_label_password = QLabel()
        icon_label_password.setPixmap(QPixmap("icons/padlock.png").scaled(40, 40)) 
        text_label_password = QLabel("Hasło")
        self.register_password_input=QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_input.setPlaceholderText("Hasło")
        layout_password.addWidget(icon_label_password)
        layout_password.addWidget(text_label_password)
        layout.addLayout(layout_password)
        layout.addWidget(self.register_password_input)
        layout.setSpacing(5)


        login_button=QPushButton("Zaloguj")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        login_button.setIcon(QIcon(QPixmap("icons/enter.png")))

        register_button=QPushButton("Zarejestruj")
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)
        register_button.setIcon(QIcon(QPixmap("icons/register.png")))

        back_button = QPushButton("Powrót")
        back_button.setIcon(QIcon("icons/back2.png"))
        back_button.clicked.connect(self.login_screen)
        layout.addWidget(back_button)

        login_button.setFixedSize(200, 50)
        register_button.setFixedSize(200, 50)
        back_button.setFixedSize(200, 50)
        self.register_username_input.setFixedSize(200, 40)
        self.register_password_input.setFixedSize(200, 40)
        self.register_email_input.setFixedSize(200, 40)

        self.setCentralWidget(register_widget)

    def register_user(self):
        print("rejestracja")
        username=self.register_username_input.text().strip()
        email=self.register_email_input.text().strip()
        password=self.register_password_input.text().strip()
        print(username, email, password)
        if username=="" or email=="" or password=="":
            print("Wszystkie pola muszą być wypełnione")
            return 
        try:
            print("Dodawanie użytkownika")
            self.db_manager.add_user(username, email, password)
            print("Użytkownik dodany")
            self.login_screen()
        except sqlite3.IntegrityError:
            print("Użytkownik już istnieje")
        
    def login(self):
        print("logowanie")
        useremail=self.login_input.text().strip()
        password=self.password_input.text().strip()
        if useremail=="" or password=="":
            print("Wszystkie pola muszą być wypełnione")
            return
        user=self.db_manager.get_user(useremail, password)
        if user:
            globals.user_id=user[0]
            globals.user_name=user[1]
            globals.user_email=user[2]
            globals.user_password=user[3]
            globals.logged_in=True
            print("Zalogowano")
            if self.favourites_widget:
                self.favourites_widget.load_favourites()
            if self.playlist_manager:
                self.playlist_manager.load_playlists()
            if self.main_pagger:
                self.main_pagger.load_playlists()
            if self.history_page:
                self.history_page.load_history()
            if self.user_page:
                self.user_page.update_user_info()
            print(globals.user_id, globals.user_name, globals.user_email, globals.user_password)
            print('przelacz sie na ekran glowny')
            self.navigate.emit(6)

        else:
            print("Niepoprawne dane logowania")

    def logout(self):
        globals.user_id=None
        globals.user_name=None
        globals.user_email=None
        globals.user_password=None
        globals.logged_in=False
        print(globals.user_id, globals.user_name, globals.user_email, globals.user_password)
        print("Wylogowano")
        self.login_screen()

    def clear_layout(self):
        central_widget = self.centralWidget()
        if central_widget is not None:
            central_widget.deleteLater()

        





if __name__=="__main__":
    app=QApplication([])
    window=User()
    window.show()
    app.exec()

from PySide6.QtWidgets import QWidget, QHBoxLayout,QVBoxLayout, QListWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QIcon, QMovie
from PySide6.QtCore import QSize
from animated_button import AnimatedButton
from database_manager import DatabaseManager
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from globals import globals


class TopBar(QWidget):
    navigate = Signal(int)
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)

        self.setStyleSheet("""
            QPushButton {
                background-color: #333; 
                border: none;           
                border-radius: 5px;     
            }
            QPushButton:hover {
                background-color: #444; 
            }
            QPushButton:pressed {
                background-color: #555;
            }
            QLineEdit {
                background-color: #222; 
                color: #FFC3EA;           
                border: 1px solid #FFC3EA; 
                border-radius: 15px;    
                padding: 5px;           
            }
                           
            QListWidget {
                background-color: #2c2c2c; 
                border: 1px solid #FFC3EA; 
                border-radius: 10px;       
                color: white;              
                font-size: 14px;           
            }
            QListWidget::item {
                padding: 10px;             
                border-bottom: 1px solid #444; 
            }
            QListWidget::item:hover {
                background-color: #444;    
                color: #FFC3EA; 
                border-radius: 10px;            
            }
            QListWidget::item:selected {
                            
                color: #FFC3EA;           
            }
                """)

        # self.back_button = AnimatedButton(animation_type=['scale'])
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("icons/left.png"))
        self.back_button.setIconSize(QSize(40, 40))
        self.back_button.setFixedSize(50, 50)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon("icons/right.png"))
        self.forward_button.setIconSize(QSize(40, 40))
        self.forward_button.setFixedSize(50, 50)

        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon("icons/home.png"))
        self.home_button.setIconSize(QSize(40, 40))
        self.home_button.setFixedSize(50, 50)

        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search songs...")
        self.search_input.textChanged.connect(self.search_songs)
        search_layout.addWidget(self.search_input)

        self.results_list = QListWidget()
        self.results_list.hide()



        self.search_container = QWidget(self)
        self.search_container.setLayout(search_layout)
        self.search_container.setFixedWidth(300)
        self.search_container.move(200, 0) 

        self.results_list.setParent(self) 
        self.results_list.setFixedWidth(300)
        self.results_list.setWindowFlags(Qt.ToolTip) 
        self.results_list.raise_()  
        self.results_list.setFocusPolicy(Qt.NoFocus) 


        self.notification_button = QPushButton()
        self.notification_button.setIcon(QIcon("icons/notification.png"))
        self.notification_button.setIconSize(QSize(40, 40))
        self.notification_button.setFixedSize(50, 50)

        self.profile_button = QPushButton()
        self.profile_button.setIcon(QIcon("icons/woman.png"))
        self.profile_button.setIconSize(QSize(40, 40))
        self.profile_button.setFixedSize(50, 50)

        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.home_button)
        layout.addWidget(self.search_container) 
        layout.addWidget(self.notification_button)
        layout.addWidget(self.profile_button)

        self.profile_button.clicked.connect(lambda: self.navigate.emit(5))
        self.home_button.clicked.connect(lambda: self.navigate.emit(6))
        
        self.results_list.itemClicked.connect(self.play_selected_song)
        self.forward_button.clicked.connect(self.go_forward)
        self.back_button.clicked.connect(self.go_back)




    def focusOutEvent(self, event):
        if self.results_list.isVisible():
            self.results_list.hide()
        super().focusOutEvent(event)

    def search_songs(self):
        print("Searching songs...")
        search_text = self.search_input.text()
        if search_text:
            db=DatabaseManager()
            songs=db.search_songs(search_text)
            print(songs)
        else:
            print("No search text")
            songs=[]
        self.results_list.clear()
        if songs:
            self.results_list.show()
            self.results_list.setFixedHeight( min(len(songs)*40, 200))
            self.results_list.move(self.search_container.x()+115, self.search_container.y() + 150)
            for song in songs:
                item=QListWidgetItem(f"{song[1]} - {song[2]}")
                self.results_list.addItem(item)
        else:
            self.results_list.hide()

    def play_selected_song(self, item):
        print("Playing selected song...")
        selected_song=item.text()
        selected_song=selected_song.split(" - ")
        for i in range(len(selected_song)):
            selected_song[i]=selected_song[i].strip()
        globals.playing=True
        globals.playing_track=selected_song[0]
        globals.playing_artist=selected_song[1]
        db=DatabaseManager()
        selected_song=db.get_song_by_title_artist(selected_song[0], selected_song[1])
        globals.playing_track_id=selected_song[0]
        globals.playing_file_path=selected_song[3]
        print(globals.playing_track, globals.playing_track_id, globals.playing_file_path)

    def go_back(self):
        print("Going back")
        self.parent_window.go_back()

    def go_forward(self):
        print("Going forward")
        self.parent_window.go_forward()


        

        





import os
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QPushButton, QFileDialog, QLineEdit, QLabel, QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from database_manager import DatabaseManager


class FileUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Uploader")
        self.setGeometry(100, 100, 400, 200)
        self.db_manager=DatabaseManager()

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        layout.setSpacing(5)
        self.setCentralWidget(main_widget)
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
                color: #ffa7c4;
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


        layout_filename=QHBoxLayout()
        layout_filename.setContentsMargins(0,0,0,0)
        layout_filename.setSpacing(5)
        layout_filename.setAlignment(Qt.AlignLeft)
        icon_label_filename = QLabel()
        icon_label_filename.setPixmap(QPixmap("icons/label.png").scaled(40, 40)) 
        text_label_filename = QLabel("Title of song")
        self.filename_input=QLineEdit()
        self.filename_input.setPlaceholderText("title of song")
        layout_filename.addWidget(icon_label_filename)
        layout_filename.addWidget(text_label_filename)
        layout.addLayout(layout_filename)
        layout.addWidget(self.filename_input)
        layout.setSpacing(5)


        layout_artist=QHBoxLayout()
        layout_artist.setContentsMargins(0,0,0,0)
        layout_artist.setSpacing(5)
        layout_artist.setAlignment(Qt.AlignLeft)
        icon_label_artist = QLabel()
        icon_label_artist.setPixmap(QPixmap("icons/singer.png").scaled(40, 40)) 
        text_label_artist = QLabel("Name of artist")
        self.artist_input=QLineEdit()
        self.artist_input.setPlaceholderText("Artist")
        layout_artist.addWidget(icon_label_artist)
        layout_artist.addWidget(text_label_artist)
        layout.addLayout(layout_artist)
        layout.addWidget(self.artist_input)
        layout.setSpacing(5)

        layout_file=QHBoxLayout()
        layout_file.setContentsMargins(0,0,0,0)
        layout_file.setSpacing(5)
        layout_file.setAlignment(Qt.AlignLeft)
        icon_label_file= QLabel()
        icon_label_file.setPixmap(QPixmap("icons/folder.png").scaled(40, 40)) 
        text_label_file = QLabel("Choose file")
        self.file_input=QLineEdit()
        self.file_input.setPlaceholderText("File")
        self.file_input.setReadOnly(True)
        self.file_button=QPushButton("Select file")
        self.file_button.setIcon(QIcon("icons/folder.png"))
        self.file_button2=QPushButton("uplaod file")
        self.file_button2.setIcon(QIcon("icons/file.png"))
        self.file_button.setFixedSize(150,50)
        self.file_button2.setFixedSize(150,50)
        layout_file.addWidget(icon_label_file)
        layout_file.addWidget(text_label_file)
        layout_file.addWidget(self.file_button)
        layout_file.addWidget(self.file_button2)
        layout.addLayout(layout_file)
        layout.addWidget(self.file_input)
        layout.setSpacing(5)



        self.file_button.clicked.connect(self.select_file)
        self.file_button2.clicked.connect(self.upload_file)



    def select_file(self):
        file_path, _=QFileDialog.getOpenFileName(self, "Select file", "", "Audio files (*.mp3 *.wav)")
        if file_path:
            self.file_input.setText(file_path)
            QMessageBox.information(self, "File selected", f"Selected file: {os.path.basename(file_path)}")


    def upload_file(self):
        title=self.filename_input.text().strip().capitalize()
        artist=self.artist_input.text().strip().capitalize()
        file_path=self.file_input.text().strip()
        if not title or not artist or not file_path:
            QMessageBox.critical(self, "Error", "Fill all fields")
            return
        print(title, artist, file_path)
        upload_directory=os.path.join("music", artist if artist else "Unknown")
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)
        file_name=os.path.basename(file_path)
        final_path=os.path.join(upload_directory, file_name)
        try:
            os.rename(file_path, final_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        
        try:
            self.db_manager.add_song(title, artist, final_path)
            QMessageBox.information(self, "Success", "Song uploaded")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            os.remove(final_path)

        self.filename_input.clear()
        self.artist_input.clear()
        self.file_input.clear()
        self.file_input.setPlaceholderText("File")




        


if __name__=="__main__":
    app=QApplication([])
    window=FileUploader()
    window.show()
    app.exec()
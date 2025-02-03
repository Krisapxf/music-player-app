from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from globals import globals
from database_manager import DatabaseManager
from globals import globals


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Viewer")
        self.setWindowIcon(QIcon("icon.png"))


        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QLabel {
                color: #ffffff;
                font-size: 16px;
            }

            QLabel#header {
                font-size: 24px;
                font-weight: bold;
                color: #FFC3EA;
                margin-bottom: 10px;
            }

            QLabel#edit_section {
                font-size: 18px;
                font-weight: bold;
                color: #FFC3EA;
                margin-top: 20px;
            }

            QLineEdit {
                background-color: #2c2c3e;
                color: #ffffff;
                border: 1px solid #FFC3EA;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton {
                background-color: #FFC3EA;
                color: black;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            }

            QPushButton:hover {
                background-color: #ff96d4;
            }

            QPushButton#cancel {
                background-color: #2c2c3e;
                color: white;
                border: 1px solid #FFC3EA;
            }

            QPushButton#cancel:hover {
                background-color: #444;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        header = QLabel("User Profile")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        profile_layout=QHBoxLayout()
        profile_picture=QLabel()
        profile_picture.setPixmap(QPixmap("icons/woman.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_layout.addWidget(profile_picture, alignment=Qt.AlignLeft)

        self.username_label = QLabel(f"Username:{globals.user_name}")
        self.email_label = QLabel(f"Email: {globals.user_email}")
        
        user_info_layout = QVBoxLayout()
        user_info_layout.addWidget(self.username_label)
        user_info_layout.addWidget(self.email_label)
        profile_layout.addLayout(user_info_layout)

        layout.addLayout(profile_layout)
        edit_section = QLabel("Edit Profile")

        layout.addWidget(edit_section, alignment=Qt.AlignLeft)

        form_layout = QVBoxLayout()
        self.edit_username_input = QLineEdit()
        self.edit_username_input.setPlaceholderText("Change Username")
        self.edit_password_input = QLineEdit()
        self.edit_password_input.setPlaceholderText("Change Password")

        form_layout.addWidget(self.edit_username_input)
        form_layout.addWidget(self.edit_password_input)

        layout.addLayout(form_layout)

        action_layout = QHBoxLayout()
        save_button = QPushButton("Save Changes")
        cancel_button = QPushButton("Cancel")
        save_button.setIcon(QIcon("icons/check.png"))
        cancel_button.setIcon(QIcon("icons/cancel.png"))

        save_button.clicked.connect(self.save_changes)
        cancel_button.clicked.connect(self.cancel_changes)

        action_layout.addWidget(save_button)
        action_layout.addWidget(cancel_button)
        layout.addLayout(action_layout)
        self.setLayout(layout)
        
    def update_user_info(self):
        self.username_label.setText(f"Username: {globals.user_name}")
        self.email_label.setText(f"Email: {globals.user_email}")


    def save_changes(self):
        new_username = self.edit_username_input.text()
        new_email = self.edit_password_input.text()
        if new_username:
            self.username_label.setText(f"Username:{new_username}")
        if new_email:
            self.email_label.setText(f"Email:{new_email}")
        self.edit_username_input.clear()
        self.edit_email_input.clear()
        globals.user_name = new_username
        globals.user_email = new_email
        DatabaseManager.update_user(new_username, new_email)


    def cancel_changes(self):
        self.edit_username_input.clear()
        self.edit_email_input.clear()
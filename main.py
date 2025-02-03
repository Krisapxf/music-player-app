from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QApplication
from main_window import MainWindow
from PySide6.QtGui import QIcon



if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("icons/spotify.png"))
    window = MainWindow()
    window.show()
    app.exec()
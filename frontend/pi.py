from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtGui import QIcon, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
AssistantName = env_vars.get("AssistantName", "Assistant")

current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

old_chat_messages = ""

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)

def SetMicrophoneStatus(status):
    with open(TempDirectoryPath("Mic.data"), "w", encoding="utf-8") as file:
        file.write(status)

def GetMicrophoneStatus():
    try:
        with open(TempDirectoryPath("Mic.data"), "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Unmuted"

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        home_button = QPushButton("  Home  ")
        home_button.setStyleSheet("height:40px; background-color:white; color: black")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        chat_button = QPushButton("  Chat  ")
        chat_button.setStyleSheet("height:40px; background-color:white; color: black")
        chat_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.mic_button = QPushButton("Mute")
        self.mic_button.setStyleSheet("height:40px; background-color:white; color: black")
        self.mic_button.clicked.connect(self.toggleMic)
        self.updateMicButton()

        close_button = QPushButton("X")
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.parent().close)

        title_label = QLabel(f"{AssistantName.capitalize()} AI")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white")

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(chat_button)
        layout.addWidget(self.mic_button)
        layout.addWidget(close_button)

    def toggleMic(self):
        current_status = GetMicrophoneStatus()
        new_status = "Muted" if current_status == "Unmuted" else "Unmuted"
        SetMicrophoneStatus(new_status)
        self.updateMicButton()

    def updateMicButton(self):
        self.mic_button.setText("Unmute" if GetMicrophoneStatus() == "Muted" else "Mute")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        screen_size = QApplication.primaryScreen().geometry()
        stacked_widget = QStackedWidget(self)
        stacked_widget.addWidget(QWidget())  # Placeholder for InitialScreen
        stacked_widget.addWidget(QWidget())  # Placeholder for MessageScreen

        self.setMenuWidget(CustomTopBar(self, stacked_widget))
        self.setCentralWidget(stacked_widget)
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()

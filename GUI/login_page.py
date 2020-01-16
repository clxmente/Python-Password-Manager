import sys

from PyQt5 import QtCore, QtWidgets, QtGui # pylint: disable=unused-import
from PyQt5.QtCore import QSize # pylint: disable=unused-import
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon # pylint: disable=unused-import
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit, QTabWidget, QErrorMessage # pylint: disable=unused-import
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication # pylint: disable=unused-import
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem # pylint: disable=unused-import
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QProgressBar # pylint: disable=unused-import

from modules.encryption import DataManip

class LoginWindow(QWidget):
    """Login Window Shown when DB is initialized"""

    def __init__(self, obj: DataManip):
        self.obj = obj
        QWidget.__init__(self)
        self.eye_path = "./icons/eye.png"
        self.lock_path = "./icons/locked.png"
        self.logo = QImage(self.lock_path)

        # General Window Setup
        self.setFixedSize(QSize(300, 425))
        self.setWindowTitle("SeveralPasswords")
        self.setWindowIcon(QIcon(self.lock_path))
        self.setStyleSheet("background-color: #77b3d4")
        self.setStyle(QApplication.setStyle("Fusion"))

        # Logo
        self.label = QLabel(self)
        self.label.setGeometry(50, 20, 200, 200) # (x, y, w, h)
        self.label.setStyleSheet("background-color: #77b3d4") #77b3d4
        self.label.setPixmap(QPixmap.fromImage(self.logo))
        self.label.setScaledContents(True)

        # "Please Log In" text
        self.text_label = QLabel(self)
        self.text_label.setGeometry(92, 220, 115, 40) #77b3d4
        self.text_label.setStyleSheet(
            """
            background-color: #77b3d4;
            color: #fff;
            font-size: 20px;
            font-family: "Segoe UI";
            font-weight: light
            """
        )
        self.text_label.setText("Please Log In")

        # Password Entry
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Your Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setGeometry(25, 275, 250, 40)
        self.password_field.setStyleSheet(
            """
            background-color: #fff;
            color: #000;
            border: 0px;
            font-family: "Segoe UI";
            padding-left: 10px;
            border-radius: 5px
            """
        )

        # Log In button
        self.log_in_btn = QPushButton(self)
        self.log_in_btn.setText("Log In")
        self.log_in_btn.setGeometry(25, 335, 250, 40)
        self.log_in_btn.setStyleSheet(
            """
            background-color: #4f5d73;
            color: #fafafa;
            font-size: 17px;
            font-family: "Segoe UI";
            """
        )
        self.log_in_btn.clicked.connect(self.verify_password)

    def show_error_box(self, message, informative_text="Try Again!"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setWindowIcon(QIcon(self.lock_path))
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setInformativeText(informative_text)
        msg_box.exec_()

    def verify_password(self):
        """Grants Log in if password is correct"""

        access = self.obj.authenticate(self.password_field.text())
        if access: # Log in correct
            self.show_error_box("CORRECT")
        else:
            self.show_error_box("Incorrect Password")

if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)
    MAIN_WINDOW = LoginWindow()
    MAIN_WINDOW.show()
    sys.exit(APP.exec_())

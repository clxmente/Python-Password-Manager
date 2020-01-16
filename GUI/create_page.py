from PyQt5 import QtCore, QtWidgets, QtGui # pylint: disable=unused-import
from PyQt5.QtCore import QSize # pylint: disable=unused-import
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon # pylint: disable=unused-import
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit, QTabWidget, QErrorMessage # pylint: disable=unused-import
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication # pylint: disable=unused-import
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem # pylint: disable=unused-import
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QProgressBar # pylint: disable=unused-import

from modules.encryption import DataManip
from GUI.login_page import LoginWindow

class CreateWindow(QMainWindow):
    """Create Page shown when user has not created a master password"""

    def __init__(self, obj: DataManip):
        QMainWindow.__init__(self)
        self.obj = obj
        self.login_window = None
        self.lock_path = "./icons/locked.png"
        self.logo = QImage(self.lock_path)

        # General Window Setup
        self.setFixedSize(QSize(300, 500))
        self.setWindowTitle("SeveralPasswords")
        self.setWindowIcon(QIcon(self.lock_path))
        self.setStyleSheet("background-color: #77b3d4")
        self.setStyle(QApplication.setStyle("Fusion"))

        # Logo
        label = QLabel(self)
        label.setGeometry(50, 20, 200, 200) # (x, y, w, h)
        label.setStyleSheet("background-color: #77b3d4")
        label.setPixmap(QPixmap.fromImage(self.logo))
        label.setScaledContents(True)

        # "Create your master password" text
        text_label = QLabel(self)
        text_label.setGeometry(25, 225, 250, 40)
        text_label.setStyleSheet(
            """
            background-color: #77b3d4;
            color: #fff;
            font-size: 20px;
            font-family: "Segoe UI";
            font-weight: light
            """
        )
        text_label.setText("Create Your Master Password")

        # First password entry
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Enter Your Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setGeometry(25, 290, 250, 40)
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

        # Second password entry
        self.cnfrm_password = QLineEdit(self)
        self.cnfrm_password.setPlaceholderText("Confirm Your Password")
        self.cnfrm_password.setEchoMode(QLineEdit.Password)
        self.cnfrm_password.setGeometry(25, 350, 250, 40)
        self.cnfrm_password.setStyleSheet(
            """
            background-color: #fff;
            color: #000;
            border: 0px;
            font-family: "Segoe UI";
            padding-left: 10px;
            border-radius: 5px
            """
        )

        # Create a profile button
        create_btn = QPushButton(self)
        create_btn.setText("Create Profile")
        create_btn.setGeometry(25, 410, 250, 40)
        create_btn.setStyleSheet(
            """
            background-color: #4f5d73;
            color: #fafafa;
            font-size: 17px;
            font-family: "Segoe UI";
            """
        )
        create_btn.clicked.connect(self.validate_passwords)

    def load_login_window(self):
        self.login_window = LoginWindow(self.obj)
        self.login_window.show()

    def validate_passwords(self):
        message = ""
        password_one = self.password_field.text()
        password_two = self.cnfrm_password.text()

        if password_one == password_two:
            if self.obj.password_valid(password_one)[0]:
                self.obj.init_db(password_one)
                self.load_login_window()
            else:
                message = "Password Contains Invalid Characters"
                informative_text = "Invalid Characters: "
                for i in self.obj.password_valid(password_one)[1]:
                    informative_text += f"{i} "
                print(message)
                self.show_error_box(message, informative_text)
        else:
            message = "Passwords Do Not Match"
            print(message)
            self.show_error_box(message)

    def show_error_box(self, message, informative_text="Try Again!"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setWindowIcon(QIcon(self.lock_path))
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setInformativeText(informative_text)
        msg_box.exec_()

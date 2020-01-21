from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QLabel, QWidget

from modules.encryption import DataManip

class LoginWindow(QWidget):
    """Login Window Shown when DB is initialized"""

    def __init__(self, obj: DataManip):
        QWidget.__init__(self)
        self.obj = obj
        self.lock_path = "./icons/locked.png"
        self.logo = QImage(self.lock_path)

        # General Window Setup
        self.setFixedSize(QSize(300, 425))
        self.setWindowTitle("SeveralPasswords")
        self.setWindowIcon(QIcon(self.lock_path))
        self.setStyleSheet("background-color: #77b3d4")

        # Logo
        label = QLabel(self)
        label.setGeometry(50, 20, 200, 200) # (x, y, w, h)
        label.setStyleSheet("background-color: #77b3d4") #77b3d4
        label.setPixmap(QPixmap.fromImage(self.logo))
        label.setScaledContents(True)

        # "Please Log In" text
        text_label = QLabel(self)
        text_label.setGeometry(92, 220, 115, 40) #77b3d4
        text_label.setStyleSheet(
            """
            background-color: #77b3d4;
            color: #fff;
            font-size: 20px;
            font-family: "Segoe UI";
            font-weight: light
            """
        )
        text_label.setText("Please Log In")

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
        log_in_btn = QPushButton(self)
        log_in_btn.setText("Log In")
        log_in_btn.setGeometry(25, 335, 250, 40)
        log_in_btn.setStyleSheet(
            """
            background-color: #4f5d73;
            color: #fafafa;
            font-size: 17px;
            font-family: "Segoe UI";
            """
        )
        log_in_btn.clicked.connect(self.verify_password)

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

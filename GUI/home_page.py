from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QLabel, QWidget, QListWidget, QListWidgetItem

from modules.encryption import DataManip

class HomeWindow(QWidget):
    def __init__(self, obj: DataManip):
        QWidget.__init__(self)
        self.obj = obj
        self.lock_path = "./icons/locked.png"
        self.logo = QImage(self.lock_path)
        self.selected_item = None

        self.passwords_list = PasswordsList(self, self.obj)
        self.passwords_list.resize(250, 300)
        self.passwords_list.move(50, 50)

        self.setFixedSize(600, 400)
        self.setWindowTitle("SeveralPasswords")
        self.setWindowIcon(QIcon(self.lock_path))

        add_btn = QPushButton("Add a Password", self)
        add_btn.setGeometry(400, 113, 100, 25)

class PasswordsList(QListWidget):
    def __init__(self, parent=None, obj=None):
        QListWidget.__init__(self, parent)
        self.obj = obj
        self.parent = parent
        passwords = self.obj.get_passwords_list("db/passwords.json")
        for password in passwords:
            self.addItem(QListWidgetItem(password))

        self.show()

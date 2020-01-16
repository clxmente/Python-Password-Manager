import sys

from PyQt5 import QtWidgets

from GUI.create_page import CreateWindow
from GUI.login_page import LoginWindow
from modules.encryption import DataManip

if __name__ == "__main__":
    OBJ = DataManip()
    APP = QtWidgets.QApplication(sys.argv)
    #MAIN_WINDOW = LoginWindow(OBJ)
    MAIN_WINDOW = CreateWindow(OBJ)
    MAIN_WINDOW.show()
    sys.exit(APP.exec_())

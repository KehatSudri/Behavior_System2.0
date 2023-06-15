from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QLineEdit, QPushButton

from Views.utils import error_warning, get_ui_path


class ManagerLoginUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.password_lineEdit = None
        self.main_window = None

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('manager_login.ui'), main_window)
        back_pushButton = main_window.findChild(QPushButton, 'Back_btn')
        back_pushButton.clicked.connect(self.on_back_click)
        login_pushButton = main_window.findChild(QPushButton, 'login_pushButton')
        login_pushButton.clicked.connect(self.on_login_click)
        self.password_lineEdit = main_window.findChild(QLineEdit, 'password_textEdit')

    def on_back_click(self):
        self.setupUi(self.main_window)
        self.main_window.close()

    def on_login_click(self):
        password = self.password_lineEdit.text()
        # check login password
        if password == "1234":
            self.parent.is_manager = True
            self.parent.main_window.show()
            self.parent.manager_show()
            self.main_window.close()
        else:
            error_warning("Wrong password")

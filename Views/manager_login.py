from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QLineEdit, QPushButton

from Views.utils import error_warning, get_ui_path


class ManagerLoginUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None
        self.central_widget = None
        self.gridLayout_window = None
        self.gridLayout_main = None
        self.headline_label = None
        self.password_label = None
        self.password_lineEdit = None
        self.back_pushButton = None
        self.login_pushButton = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('manager_login.ui'), main_window)

        self.back_pushButton = main_window.findChild(QPushButton, 'Back_btn')
        self.back_pushButton.clicked.connect(self.on_back_click)

        self.login_pushButton = main_window.findChild(QPushButton, 'login_pushButton')
        self.login_pushButton.clicked.connect(self.on_login_click)

        self.password_lineEdit = main_window.findChild(QLineEdit, 'password_textEdit')


    def on_back_click(self):
        self.setupUi(self.main_window)
        #self.parent.main_window.show()
        self.main_window.close()
        #self.parent.main_window.show()
        #self.main_window.close()

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


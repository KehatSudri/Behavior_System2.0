from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QLineEdit, QPushButton

from Views.utils import error_warning, get_ui_path


class NotesUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None
        self.back_pushButton = None
        self.login_pushButton = None

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('notes.ui'), main_window)
        self.commentsWindow=self.main_window.findChild(QtWidgets.QTextEdit, "textEdit")
        self.save=self.main_window.findChild(QtWidgets.QPushButton, "save_pushButton")
        self.save.clicked.connect(self.save_click)
        self.commentsWindow.setText(self.parent.notes)
    def save_click(self):
        comments=self.commentsWindow.toPlainText()
        self.parent.notes=comments
        self.main_window.close()








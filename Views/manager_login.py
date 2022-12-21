from PyQt6 import QtCore,QtGui, QtWidgets
from PyQt6.QtWidgets import QLineEdit

from Views.utils import error_warning


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
        self.parent.main_window.hide()
        main_window.setObjectName("main_window")
        main_window.resize(522, 361)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        # set layout
        self.gridLayout_window = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_window.setObjectName("gridLayout_window")
        self.gridLayout_main = QtWidgets.QGridLayout()
        self.gridLayout_main.setContentsMargins(20, -1, 30, -1)
        self.gridLayout_main.setObjectName("gridLayout_main")
        # set headline label
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Gabriola\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.gridLayout_main.addWidget(self.headline_label, 0, 0, 1, 3)
        # set a label for password
        self.password_label = QtWidgets.QLabel(self.central_widget)
        self.password_label.setStyleSheet("font: 20pt \"Gabriola\";")
        self.password_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password_label.setObjectName("password_label")
        self.gridLayout_main.addWidget(self.password_label, 1, 0, 1, 1)
        # set a line edit button to insert password
        self.password_lineEdit = QtWidgets.QLineEdit(self.central_widget)
        self.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_lineEdit.setStyleSheet("font: 20pt \"David\";")
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.gridLayout_main.addWidget(self.password_lineEdit, 1, 1, 1, 2)
        # set vertical spacer
        #vertical_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.gridLayout_main.addItem(vertical_spacer_item, 3, 2, 1, 1)
        # set a button to login
        #horizontal_spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.gridLayout_main.addItem(horizontal_spacer_item1, 3, 0, 1, 1)
        # add a back button
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setStyleSheet("font: 15pt \"Gabriola\";")
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        # self.gridLayout_main.addWidget(self.login_pushButton, 3, 1, 1, 1)
        # add a login button
        self.login_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.login_pushButton.setStyleSheet("font: 15pt \"Gabriola\";")
        self.login_pushButton.setObjectName("login_pushButton")
        self.login_pushButton.clicked.connect(self.on_login_click)
        # self.gridLayout_main.addWidget(self.login_pushButton, 3, 1, 1, 1)


        # self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        # self.choose_template_horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.navigation_horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.navigation_horizontalLayout.setSpacing(2)
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        # self.gridLayout_main.addWidget(self.login_pushButton, 3, 1, 1, 1)

        #spacer_item5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        self.navigation_horizontalLayout.addWidget(self.login_pushButton)
        self.gridLayout_main.addLayout(self.navigation_horizontalLayout, 3, 1, 1, 1)

        #horizontal_spacer_item2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.gridLayout_main.addItem(horizontal_spacer_item2, 2, 1, 1, 1)

        self.gridLayout_main.setColumnStretch(0, 1)
        self.gridLayout_main.setColumnStretch(1, 1)
        self.gridLayout_main.setColumnStretch(2, 1)
        # self.gridLayout_main.setRowStretch(0, 20)
        # self.gridLayout_main.setRowStretch(1, 1)
        # self.gridLayout_main.setRowStretch(2, 20)
        # self.gridLayout_main.setRowStretch(3, 20)
        self.gridLayout_window.addLayout(self.gridLayout_main, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def on_back_click(self):
        self.parent.main_window.show()
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

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Manager Login"))
        self.password_label.setText(_translate("main", "Password:"))
        self.back_pushButton.setText(_translate("main", "Back"))
        self.login_pushButton.setText(_translate("main", "Login"))
        self.headline_label.setText(_translate("main", "Manager Login"))


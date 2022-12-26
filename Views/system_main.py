import sys

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QPushButton

from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.create_new_event import CreateEventUi
from Views.create_session import CreateSessionUi
from Views.create_trial_type import CreateTrialTypeUi
from Views.delete_session_template import DeleteSessionTemplate
from Views.delete_trial_type import DeleteTrialTypeUi
from Views.edit_trial_type import EditTrialTypeUi
from Views.manager_login import ManagerLoginUi
from Views.settings import SettingsUi
from Views.utils import get_ui_path


class SystemMainUi(object):
    def __init__(self):
        self.vm = None
        self.central_widget = None
        self.verticalLayout_1 = None
        self.gridLayout = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.verticalLayout = None
        self.headline_label = None
        self.explanation_label = None
        self.manager_login_pushButton = None
        self.settings_pushButton = None
        self.create_trial_type_pushButton = None
        self.create_event_pushButton = None
        self.create_session_pushButton = None
        self.present_session_data_pushButton = None
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = None
        self.is_manager = False
        self.main_window = None
        # with manager permissions
        self.edit_trial_type_pushButton = None
        self.delete_template_pushButton = None
        self.delete_trial_type_pushButton = None
        self.delete_templates_pushButton = None
        self.is_session_running = False
        self.control_session_board = None

    # def setupUi(self, main_window, sysVM):
    def setupUi(self, main_window, systemVM):
        self.main_window = main_window
        self.vm = systemVM
        self.vm.property_changed += self.EventHandler
        uic.loadUi(get_ui_path('system_main.ui'), main_window)
        self.create_session_pushButton = main_window.findChild(QPushButton, 'create_session_btn')
        self.create_session_pushButton.clicked.connect(self.on_create_session_click)
        #ses_btn.clicked.connect(lambda: print("hello world"))
        #ses_btn.clicked.connect(lambda: print("hello world"))


        # self.central_widget = QtWidgets.QWidget(main_window)
        # self.central_widget.setObjectName("central_widget")
        # self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.central_widget)
        # self.verticalLayout_1.setObjectName("verticalLayout_1")
        # self.gridLayout = QtWidgets.QGridLayout()
        # self.gridLayout.setObjectName("gridLayout")
        # set headline
        # self.headline_label = QtWidgets.QLabel(self.central_widget)
        # self.headline_label.setStyleSheet("font: 55pt \"Gabriela\";")
        # self.headline_label.setObjectName("headline_label")
        # self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.gridLayout.addWidget(self.headline_label, 0, 0, 1, 3)
        # set an explanation label
        # self.explanation_label = QtWidgets.QLabel(self.central_widget)
        # self.explanation_label.setMinimumSize(QtCore.QSize(400, 80))
        # self.explanation_label.setMaximumSize(QtCore.QSize(16777215, 134))
        # self.explanation_label.setBaseSize(QtCore.QSize(0, 0))
        # self.explanation_label.setStyleSheet("font: 30pt \"Gabriela\";")
        # self.explanation_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.explanation_label.setObjectName("explanation_label")
        # self.gridLayout.addWidget(self.explanation_label, 1, 0, 1, 3)
        # set a scrollArea to present all the options available
        # self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        # font = QtGui.QFont()
        # font.setFamily("Gabriela")
        # font.setPointSize(15)
        # self.scrollArea.setFont(font)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 382, 325))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        # self.verticalLayout.setObjectName("verticalLayout")
        # set a button to login as a manager
        # self.manager_login_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.manager_login_pushButton.setObjectName("manager_login_pushButton")
        # self.manager_login_pushButton.clicked.connect(self.on_manager_login_click)
        # self.verticalLayout.addWidget(self.manager_login_pushButton)
        # set a button for settings
        # self.settings_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.settings_pushButton.setObjectName("settings_pushButton")
        # self.settings_pushButton.clicked.connect(self.on_settings_click)
        # self.verticalLayout.addWidget(self.settings_pushButton)
        # self.create_trial_type_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.create_trial_type_pushButton.setObjectName("create_trial_type_pushButton")
        # self.create_trial_type_pushButton.clicked.connect(self.on_create_trial_type)
        # self.verticalLayout.addWidget(self.create_trial_type_pushButton)
        # set a button to create a new event
        # self.create_event_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.create_event_pushButton.setObjectName("create_event_pushButton")
        # self.create_event_pushButton.clicked.connect(self.on_create_event_click)
        # self.verticalLayout.addWidget(self.create_event_pushButton)
        # set a button to create a new session
        # self.create_session_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.create_session_pushButton.setObjectName("create_session_pushButton")
        # self.create_session_pushButton.clicked.connect(self.on_create_session_click)
        # self.verticalLayout.addWidget(self.create_session_pushButton)
        # set a button to present current running session's data
        # self.present_session_data_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.present_session_data_pushButton.setObjectName("present_session_data_pushButton")
        # self.present_session_data_pushButton.setEnabled(False)
        # self.present_session_data_pushButton.clicked.connect(self.on_present_ctrl_sess_board_click)
        # self.verticalLayout.addWidget(self.present_session_data_pushButton)

        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.gridLayout.addWidget(self.scrollArea, 2, 1, 1, 1)
        # spacer_item = QtWidgets.QSpacerItem(20, 40, QtGui.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout.addItem(spacer_item, 2, 2, 1, 1)

        # spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtGui.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout.addItem(spacer_item1, 2, 0, 1, 1)
        # self.gridLayout.setColumnStretch(0, 1)
        # self.gridLayout.setColumnStretch(1, 2)
        # self.gridLayout.setColumnStretch(2, 1)
        # self.verticalLayout_1.addLayout(self.gridLayout)
        # main_window.setCentralWidget(self.central_widget)

        # self.retranslateUi(main_window)
        # QtCore.QMetaObject.connectSlotsByName(main_window)

    def on_manager_login_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = ManagerLoginUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def manager_show(self):
        if self.is_manager:
            self.edit_trial_type_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.edit_trial_type_pushButton.setObjectName("edit_trial_types_pushButton")
            self.edit_trial_type_pushButton.setText("Edit trial type")
            self.verticalLayout.addWidget(self.edit_trial_type_pushButton)
            self.edit_trial_type_pushButton.clicked.connect(self.on_edit_trial_type_click)

            self.delete_trial_type_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.delete_trial_type_pushButton.setObjectName("delete_trial_types_pushButton")
            self.delete_trial_type_pushButton.setText("Delete trial type")
            self.verticalLayout.addWidget(self.delete_trial_type_pushButton)
            self.delete_trial_type_pushButton.clicked.connect(self.on_delete_trial_type_click)

            self.delete_templates_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.delete_templates_pushButton.setObjectName("delete_templates_pushButton")
            self.delete_templates_pushButton.setText("Delete session templates")
            self.verticalLayout.addWidget(self.delete_templates_pushButton)
            self.delete_templates_pushButton.clicked.connect(self.on_delete_templates_click)

    def on_settings_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = SettingsUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_trial_type(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = CreateTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_event_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = CreateEventUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_session_click(self):
        chosen_window = QtWidgets.QMainWindow()
        uic.loadUi(get_ui_path('Create_session.ui'), chosen_window)

        # self.chosen_window_ui = CreateSessionUi(self)
        # self.chosen_window_ui.setupUi(self.chosen_window)
        chosen_window.show()
        # self.main_window.hide()

    def on_edit_trial_type_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = EditTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_delete_trial_type_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = DeleteTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_delete_templates_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = DeleteSessionTemplate(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_present_ctrl_sess_board_click(self):
        self.control_session_board.show()

    def retranslateUi(self, main):
        return
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Behavioral System"))
        self.explanation_label.setText(_translate("main", "Welcome, please choose the option you desire"))
        self.manager_login_pushButton.setText(_translate("main", "Login as a manager"))
        self.settings_pushButton.setText(_translate("main", "Settings"))
        self.create_trial_type_pushButton.setText(_translate("main", "Create a new trial type"))
        self.create_event_pushButton.setText(_translate("main", "Create a new event"))
        self.create_session_pushButton.setText(_translate("main", "Create a new session"))
        self.present_session_data_pushButton.setText(_translate("main", "Open running session controller"))
        self.headline_label.setText(_translate("main", "Behavioral System"))

    def EventHandler(self, sender, *event_args):
        if type(sender) != BehaviorSystemViewModel:
            pass
        if event_args[0][0] == "VM_is_running_session":
            self.is_session_running = self.vm.is_running_session
            self.is_session_running_changed()

    def is_session_running_changed(self):
        if self.is_session_running:  # session is running
            self.manager_login_pushButton.setEnabled(False)
            self.settings_pushButton.setEnabled(False)
            self.create_trial_type_pushButton.setEnabled(False)
            self.create_event_pushButton.setEnabled(False)
            self.create_session_pushButton.setEnabled(False)
            self.present_session_data_pushButton.setEnabled(True)
            if self.is_manager:
                self.edit_trial_type_pushButton.setEnabled(False)
                self.delete_template_pushButton.setEnabled(False)
                self.delete_trial_type_pushButton.setEnabled(False)
        else:  # session is stopped
            self.manager_login_pushButton.setEnabled(True)
            self.settings_pushButton.setEnabled(True)
            self.create_trial_type_pushButton.setEnabled(True)
            self.create_event_pushButton.setEnabled(True)
            self.create_session_pushButton.setEnabled(True)
            self.present_session_data_pushButton.setEnabled(False)
            # if self.chosen_window is not None:
            #     self.chosen_window.close()
            # if self.control_session_board is not None:
            #     self.control_session_board.close()
            if self.is_manager:
                self.edit_trial_type_pushButton.setEnabled(True)
                self.delete_template_pushButton.setEnabled(True)
                self.delete_trial_type_pushButton.setEnabled(True)

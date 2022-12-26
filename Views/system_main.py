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
    def setupUi(self, main_window, system_vm):
        self.main_window = main_window
        self.vm = system_vm
        self.vm.property_changed += self.EventHandler
        uic.loadUi(get_ui_path('system_main.ui'), self.main_window)
        self.create_session_pushButton = main_window.findChild(QPushButton, 'create_session_btn')
        self.create_session_pushButton.clicked.connect(self.on_create_session_click)

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
        self.chosen_window_ui = SettingsUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_trial_type(self):
        self.chosen_window_ui = CreateTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_event_click(self):
        self.chosen_window_ui = CreateEventUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_create_session_click(self):
        self.chosen_window_ui = CreateSessionUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()
        #self.main_window.hide()

    def on_edit_trial_type_click(self):
        self.chosen_window_ui = EditTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_delete_trial_type_click(self):
        self.chosen_window_ui = DeleteTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_delete_templates_click(self):
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

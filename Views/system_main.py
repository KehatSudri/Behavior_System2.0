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
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.verticalLayout = None
        self.headline_label = None
        self.explanation_label = None
        self.create_session_pushButton = None
        self.present_session_data_pushButton = None
        self.chosen_window = None
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
    def setupUi(self, main_window, system_vm, isManager=False):
        self.vm = system_vm
        if isManager:
            temp = self.main_window
            self.main_window = main_window
            self.main_window.show()
            temp.close()

        else:
            self.main_window = main_window
            self.vm.property_changed += self.EventHandler
            uic.loadUi(get_ui_path('system_main.ui'), self.main_window)
            manager_login_push_button = self.main_window.findChild(QPushButton, 'manager_login_pushButton')
            manager_login_push_button.clicked.connect(self.on_manager_login_click)

        create_trial_type_push_button = self.main_window.findChild(QPushButton, 'create_trial_type_pushButton')
        create_trial_type_push_button.clicked.connect(self.on_create_trial_type)

        create_event_push_button = self.main_window.findChild(QPushButton, 'create_event_pushButton')
        create_event_push_button.clicked.connect(self.on_create_event_click)

        create_session_push_button = self.main_window.findChild(QPushButton, 'create_session_btn')
        create_session_push_button.clicked.connect(self.on_create_session_click)

        settings_pushButton = self.main_window.findChild(QPushButton, 'settings_pushButton')
        settings_pushButton.clicked.connect(self.on_settings_click)

    def on_manager_login_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = ManagerLoginUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def manager_show(self):
        if self.is_manager:
            manager_window = QtWidgets.QMainWindow()
            uic.loadUi(get_ui_path('system_main_plus.ui'), manager_window)
            self.edit_trial_type_pushButton = manager_window.findChild(QPushButton, 'edit_trial_types_pushButton')
            self.edit_trial_type_pushButton.clicked.connect(self.on_edit_trial_type_click)
            self.delete_trial_type_pushButton = manager_window.findChild(QPushButton, 'delete_trial_types_pushButton')
            self.delete_trial_type_pushButton.clicked.connect(self.on_delete_trial_type_click)
            self.delete_templates_pushButton = manager_window.findChild(QPushButton, 'delete_templates_pushButton')
            self.delete_templates_pushButton.clicked.connect(self.on_delete_templates_click)
            self.setupUi(manager_window, self.vm, True)

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
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = CreateSessionUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()
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

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QPushButton
from Views.create_new_event import CreateEventUi
from Views.create_session import CreateSessionUi
from Views.create_trial_type import CreateTrialTypeUi
from Views.delete_trial_type import DeleteTrialTypeUi
from Views.remove_event import removeEventUi
from Views.manager_login import ManagerLoginUi
from Views.settings import SettingsUi
from Views.utils import get_ui_path


class SystemMainUi(object):
    def __init__(self):
        self.vm = None
        self.chosen_window = None
        self.chosen_window_ui = None
        self.is_manager = False
        self.main_window = None

    def setupUi(self, main_window, system_vm, isManager=False):
        self.vm = system_vm
        if isManager:
            temp = self.main_window
            self.main_window = main_window
            self.main_window.show()
            temp.close()
            create_event_push_button = self.main_window.findChild(QPushButton, 'create_event_pushButton')
            create_event_push_button.clicked.connect(self.on_create_event_click)
            settings_pushButton = self.main_window.findChild(QPushButton, 'settings_pushButton')
            settings_pushButton.clicked.connect(self.on_settings_click)
            back_pushButton = self.main_window.findChild(QPushButton, 'back_pushButton')
            back_pushButton.clicked.connect(self.on_back_click)
        else:
            self.main_window = main_window
            uic.loadUi(get_ui_path("system_main.ui"), self.main_window)
            manager_login_push_button = self.main_window.findChild(QPushButton, 'manager_login_pushButton')
            manager_login_push_button.clicked.connect(self.on_manager_login_click)
            create_trial_type_push_button = self.main_window.findChild(QPushButton, 'create_trial_type_pushButton')
            create_trial_type_push_button.clicked.connect(self.on_create_trial_type)
            create_session_push_button = self.main_window.findChild(QPushButton, 'create_session_btn')
            create_session_push_button.clicked.connect(self.on_create_session_click)

    def on_manager_login_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = ManagerLoginUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def manager_show(self):
        if self.is_manager:
            manager_window = QtWidgets.QMainWindow()
            uic.loadUi(get_ui_path('system_main_plus.ui'), manager_window)
            delete_trial_type_pushButton = manager_window.findChild(QPushButton, 'delete_trial_types_pushButton')
            delete_trial_type_pushButton.clicked.connect(self.on_delete_trial_type_click)
            removeEvent_pushButton = manager_window.findChild(QPushButton, 'removeEvent')
            removeEvent_pushButton.clicked.connect(self.on_removeEvent_click)
            self.setupUi(manager_window, self.vm, True)

    def on_settings_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = SettingsUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_back_click(self):
        self.setupUi(self.main_window, self.vm)

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

    def on_delete_trial_type_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = DeleteTrialTypeUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_removeEvent_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = removeEventUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

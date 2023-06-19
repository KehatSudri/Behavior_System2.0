import os
from PyQt6 import QtWidgets, uic
from Views.utils import error_warning, get_ui_path


class SettingsUi(object):
    def __init__(self, parent):
        self.log_file_path_text_edit = None
        self.new_folder_path = None
        self.parent = parent
        self.vm = parent.vm
        self.main_window = None
        self.insert_log_file_path_radioButton = None
        self.choose_log_file_path_radioButton = None
        self.log_file_path_lineEdit = None
        self.insert_db_file_path_radioButton = None
        self.choose_db_file_radioButton = None
        self.db_path_textEdit = None
        self.max_identical_consecutive_trials_spinBox = None
        self.file_db_file_path = self.vm.db_config_file_path
        # self.db_section = self.vm.db_section
        self.max_identical_consecutive_trial = self.vm.max_successive_trials
        self.max_time_duration = self.vm.max_trial_length
        self.input_events = self.vm.input_events_names
        self.input_ports = self.vm.input_ports
        self.output_events = self.vm.output_events_names
        self.output_ports = self.vm.output_ports
        self.event_config = self.vm.event_config

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('settings.ui'), main_window)
        choose_folder_btn = main_window.findChild(QtWidgets.QPushButton, "choose_folder_btn")
        choose_folder_btn.clicked.connect(self.on_log_folder_click)
        settings_ok_back_btn = main_window.findChild(QtWidgets.QPushButton, "settings_ok_back_btn")
        settings_ok_back_btn.clicked.connect(self.on_settings_ok_click)
        choose_folder_radio_btn = main_window.findChild(QtWidgets.QRadioButton, "choose_folder_radio_btn")
        choose_folder_radio_btn.toggled.connect(
            lambda: choose_folder_btn.setEnabled(choose_folder_radio_btn.isChecked()))
        self.log_file_path_text_edit = main_window.findChild(QtWidgets.QTextEdit, "log_file_path_text_edit")
        insert_path_radio_btn = main_window.findChild(QtWidgets.QRadioButton, "insert_path_radio_btn")
        insert_path_radio_btn.toggled.connect(
            lambda: self.log_file_path_text_edit.setEnabled(insert_path_radio_btn.isChecked()))

    def on_log_folder_click(self):
        dialog = QtWidgets.QFileDialog()
        self.new_folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.log_file_path_text_edit.setText(self.new_folder_path)

    def on_settings_ok_click(self):
        with open(self.vm.model.settings_file, 'r') as f:
            lines = f.readlines()
        lines[0] = f'log file location={self.new_folder_path}\n'
        with open(self.vm.model.settings_file, 'w') as f:
            for line in lines:
                f.write(line)
        self.main_window.close()

    def get_max_identical_consecutive_trial(self):
        self.max_identical_consecutive_trial = self.max_identical_consecutive_trials_spinBox.value()

    def get_max_time_duration(self):
        self.max_time_duration = self.max_time_duration_spinBox.value()

    def accept(self):
        from os import path
        if self.folder_log_file_path == "":
            self.folder_log_file_path = os.getcwd()
        if not path.exists(self.folder_log_file_path):
            # path is invalid
            error_warning("Folder path for logging is invalid")
            return
        if not path.exists(self.file_db_file_path):
            error_warning("DB file path is invalid")
            return
        # parse table
        e_config_list = []
        for i in range(self.event_port_tableWidget.rowCount()):
            l = []
            for j in range(self.event_port_tableWidget.columnCount()):
                l.append(self.event_port_tableWidget.item(i, j).text())
            e_config_list.append(l)
        self.vm.set_settings(self.folder_log_file_path, self.file_db_file_path, self.db_section,
                             self.max_identical_consecutive_trials_spinBox.value(),
                             self.max_time_duration_spinBox.value(), e_config_list)

        self.parent.main_window.show()
        self.main_window.close()

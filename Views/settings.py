import os

from PyQt6 import QtCore, QtWidgets, uic
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
        # data for each: name, port, input/output, digital/analog, is reward
        # for i in range(5):
        #     column_position = self.event_port_tableWidget.columnCount()
        #     self.event_port_tableWidget.insertColumn(column_position)
        # for i in range(len(self.event_config)):
        #     row_position = self.event_port_tableWidget.rowCount()
        #     self.event_port_tableWidget.insertRow(row_position)
        #     for j in range(1, len(self.event_config[i])):
        #         self.event_port_tableWidget.setItem(row_position, j - 1, QTableWidgetItem(self.event_config[i][j]))
        # for i in range(len(self.input_ports)):
        #     row_position = self.event_port_tableWidget.rowCount()
        #     self.event_port_tableWidget.insertRow(row_position)
        #     self.event_port_tableWidget.setItem(row_position, 0, QTableWidgetItem(self.input_events[i]))
        #     self.event_port_tableWidget.setItem(row_position, 1, QTableWidgetItem(self.input_ports[i]))
        #     self.event_port_tableWidget.setItem(row_position, 2, QTableWidgetItem('Input'))
        #     self.event_port_tableWidget.setItem(row_position, 3, QTableWidgetItem('Analog'))
        #     self.event_port_tableWidget.setItem(row_position, 4, QTableWidgetItem('False'))
        #
        # for i in range(len(self.output_ports)):
        #     row_position = self.event_port_tableWidget.rowCount()
        #     self.event_port_tableWidget.insertRow(row_position)
        #     self.event_port_tableWidget.setItem(row_position, 0, QTableWidgetItem(self.output_events[i]))
        #     self.event_port_tableWidget.setItem(row_position, 1, QTableWidgetItem(self.output_ports[i]))
        #     self.event_port_tableWidget.setItem(row_position, 2, QTableWidgetItem('Output'))
        #     self.event_port_tableWidget.setItem(row_position, 3, QTableWidgetItem('Digital'))
        #     self.event_port_tableWidget.setItem(row_position, 4, QTableWidgetItem('False'))
        # set success rate
        # self.success_rate_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # self.success_rate_label.setStyleSheet("font: 15pt \"Gabriola\";")
        # self.success_rate_label.setObjectName("success_rate_label")
        # self.verticalLayout.addWidget(self.success_rate_label)
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        # ##spacer_item = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # ##self.window_gridLayout.addItem(spacer_item, 2, 0, 1, 1)
        # self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        # self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        # ##spacer_item1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #
        # ##self.navigation_horizontalLayout.addItem(spacer_item1)
        # # set back button
        # self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        # self.back_pushButton.setObjectName("back_pushButton")
        # self.back_pushButton.clicked.connect(self.on_back_click)
        # self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        # # set ok button
        # self.ok_pushButton = QtWidgets.QPushButton(self.central_widget)
        # self.ok_pushButton.setObjectName("ok_pushButton")
        # self.ok_pushButton.clicked.connect(self.accept)
        # self.navigation_horizontalLayout.addWidget(self.ok_pushButton)
        # ##spacer_item2 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # ##self.navigation_horizontalLayout.addItem(spacer_item2)
        # self.navigation_horizontalLayout.setStretch(0, 1)
        # self.navigation_horizontalLayout.setStretch(1, 1)
        # self.navigation_horizontalLayout.setStretch(2, 1)
        # self.navigation_horizontalLayout.setStretch(3, 1)
        # self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 3, 0, 1, 1)
        # main_window.setCentralWidget(self.central_widget)
        #
        # self.retranslateUi(main_window)
        # QtCore.QMetaObject.connectSlotsByName(main_window)
        #
        # # define a connection for each option to set a path for log file and db file
        # self.log_file_path_cfg()
        # self.db_file_path_cfg()
        # # set vm current data to display
        # self.log_file_path_lineEdit.setText(self.folder_log_file_path)
        # self.db_path_textEdit.setText(self.file_db_file_path)
        # self.db_section_lineEdit.setText(self.db_section)
        # self.max_identical_consecutive_trials_spinBox.setValue(self.vm.max_successive_trials)
        # self.max_time_duration_spinBox.setValue(self.vm.max_trial_length)

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
        e_2_p_str = None  # need to make string from table
        self.vm.set_settings(self.folder_log_file_path, self.file_db_file_path, self.db_section,
                             self.max_identical_consecutive_trials_spinBox.value(),
                             self.max_time_duration_spinBox.value(), e_config_list)

        self.parent.main_window.show()
        self.main_window.close()

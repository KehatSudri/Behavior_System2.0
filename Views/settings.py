import os

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from Views.utils import error_warning


class SettingsUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = parent.vm
        self.main_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.main_gridLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.verticalLayout = None
        self.log_file_path_label = None
        self.log_file_path_horizontalLayout = None
        self.insert_log_file_path_radioButton = None
        self.choose_log_file_path_radioButton = None
        self.log_file_horizontalLayout = None
        self.log_file_path_lineEdit = None
        self.choose_log_file_folder_pushButton = None
        # self.choose_log_file_folder_pushButton = None
        self.db_file_path_label = None
        self.db_file_path_horizontalLayout = QtWidgets.QHBoxLayout()
        self.insert_db_file_path_radioButton = None
        self.choose_db_file_radioButton = None
        self.db_file_horizontalLayout = QtWidgets.QHBoxLayout()
        self.db_path_textEdit = None
        self.choose_db_file_pushButton = None
        self.db_section_horizontalLayout = QtWidgets.QHBoxLayout()
        self.db_section_label = None
        self.db_section_lineEdit = None
        self.max_identical_consecutive_trials_horizontalLayout = QtWidgets.QHBoxLayout()
        self.max_identical_consecutive_trials_label = None
        self.max_identical_consecutive_trials_spinBox = None
        self.max_trial_duration_horizontalLayout = QtWidgets.QHBoxLayout()
        self.max_time_duration_label = None
        self.max_time_duration_spinBox = None
        self.events_label = None
        self.event_port_tableWidget = None
        self.success_rate_label = None
        self.navigation_horizontalLayout = None
        self.ok_pushButton = None
        self.back_pushButton = None

        self.folder_log_file_path = self.vm.log_file_path
        self.file_db_file_path = self.vm.db_config_file_path
        self.db_section = self.vm.db_section
        self.max_identical_consecutive_trial = self.vm.max_successive_trials
        self.max_time_duration = self.vm.max_trial_length
        self.input_events = self.vm.input_events_names
        self.input_ports = self.vm.input_ports
        self.output_events = self.vm.output_events_names
        self.output_ports = self.vm.output_ports
        self.event_config = self.vm.event_config

    def setupUi(self, main_window):
        self.main_window = main_window
        self.parent.main_window.hide()
        main_window.setObjectName("main_window")
        main_window.resize(500, 576)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        # set main layout
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        self.main_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.setObjectName("main_gridLayout")
        # set headline label
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setMinimumSize(QtCore.QSize(400, 80))
        self.headline_label.setMaximumSize(QtCore.QSize(16777215, 134))
        self.headline_label.setBaseSize(QtCore.QSize(0, 0))
        self.headline_label.setStyleSheet("font: 55pt \"Gabriola\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.main_gridLayout.addWidget(self.headline_label, 0, 0, 1, 1)
        self.window_gridLayout.addLayout(self.main_gridLayout, 0, 0, 1, 1)
        # set scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 463, 686))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        # set definition of log file path
        self.log_file_path_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.log_file_path_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.log_file_path_label.setObjectName("log_file_path_label")
        self.verticalLayout.addWidget(self.log_file_path_label)
        self.log_file_path_horizontalLayout = QtWidgets.QHBoxLayout()
        self.log_file_path_horizontalLayout.setObjectName("log_file_path_horizontalLayout")
        self.insert_log_file_path_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Gabriola")
        font.setPointSize(15)
        self.insert_log_file_path_radioButton.setFont(font)
        self.insert_log_file_path_radioButton.setObjectName("insert_log_file_path_radioButton")
        self.log_file_path_horizontalLayout.addWidget(self.insert_log_file_path_radioButton)
        self.choose_log_file_path_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.choose_log_file_path_radioButton.setFont(font)
        self.choose_log_file_path_radioButton.setObjectName("choose_log_file_path_radioButton")
        self.log_file_path_horizontalLayout.addWidget(self.choose_log_file_path_radioButton)
        self.log_file_path_horizontalLayout.setStretch(0, 1)
        self.log_file_path_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.log_file_path_horizontalLayout)

        self.log_file_horizontalLayout = QtWidgets.QHBoxLayout()
        self.log_file_horizontalLayout.setObjectName("log_file_horizontalLayout")
        self.log_file_path_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.log_file_path_lineEdit.setFont(font)
        self.log_file_path_lineEdit.setObjectName("log_file_path_textEdit")
        self.log_file_path_lineEdit.setEnabled(False)
        self.log_file_horizontalLayout.addWidget(self.log_file_path_lineEdit)
        self.choose_log_file_folder_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.choose_log_file_folder_pushButton.setObjectName("choose_log_file_folder_pushButton")
        self.choose_log_file_folder_pushButton.clicked.connect(self.on_folder_click)
        self.choose_log_file_folder_pushButton.setEnabled(False)
        self.log_file_horizontalLayout.addWidget(self.choose_log_file_folder_pushButton)
        self.log_file_horizontalLayout.setStretch(0, 3)
        self.log_file_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.log_file_horizontalLayout)
        # set definition of db file path
        self.db_file_path_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.db_file_path_label.setFont(font)
        self.db_file_path_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.db_file_path_label.setObjectName("db_file_path_label")
        self.verticalLayout.addWidget(self.db_file_path_label)

        self.db_file_path_horizontalLayout.setObjectName("db_file_path_horizontalLayout")
        self.insert_db_file_path_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.insert_db_file_path_radioButton.setFont(font)
        self.insert_db_file_path_radioButton.setObjectName("insert_db_file_path_radioButton")
        self.db_file_path_horizontalLayout.addWidget(self.insert_db_file_path_radioButton)
        self.choose_db_file_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.choose_db_file_radioButton.setFont(font)
        self.choose_db_file_radioButton.setObjectName("choose_db_file_radioButton")
        self.db_file_path_horizontalLayout.addWidget(self.choose_db_file_radioButton)
        self.db_file_path_horizontalLayout.setStretch(0, 1)
        self.db_file_path_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.db_file_path_horizontalLayout)

        self.db_file_horizontalLayout.setObjectName("db_file_horizontalLayout")
        self.db_path_textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("David")
        font.setPointSize(15)
        self.db_path_textEdit.setFont(font)
        self.db_path_textEdit.setObjectName("db_path_textEdit")
        self.db_path_textEdit.setEnabled(False)
        self.db_file_horizontalLayout.addWidget(self.db_path_textEdit)
        self.choose_db_file_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.choose_db_file_pushButton.setObjectName("choose_db_file_pushButton")
        self.choose_db_file_pushButton.clicked.connect(self.on_file_click)
        self.choose_db_file_pushButton.setEnabled(False)
        self.db_file_horizontalLayout.addWidget(self.choose_db_file_pushButton)
        self.db_file_horizontalLayout.setStretch(0, 3)
        self.db_file_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.db_file_horizontalLayout)
        # set db section
        self.db_section_horizontalLayout.setObjectName("db_section_horizontalLayout")
        self.db_section_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.db_section_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.db_section_label.setObjectName("db_section_label")
        self.db_section_horizontalLayout.addWidget(self.db_section_label)
        self.db_section_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.db_section_lineEdit.setStyleSheet("font: 15pt \"David\";")
        self.db_section_lineEdit.setObjectName("db_section_textEdit")
        self.db_section_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
        self.db_section_lineEdit.editingFinished.connect(self.on_db_section_changed)
        self.db_section_horizontalLayout.addWidget(self.db_section_lineEdit)
        self.db_section_horizontalLayout.setStretch(0, 1)
        self.db_section_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.db_section_horizontalLayout)
        # set max identical consecutive trials
        self.max_identical_consecutive_trials_horizontalLayout \
            .setObjectName("max_identical_consecutive_trials_horizontalLayout")
        self.max_identical_consecutive_trials_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.max_identical_consecutive_trials_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.max_identical_consecutive_trials_label.setObjectName("max_identical_consecutive_trials_label")
        self.max_identical_consecutive_trials_horizontalLayout.addWidget(self.max_identical_consecutive_trials_label)
        self.max_identical_consecutive_trials_spinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.max_identical_consecutive_trials_spinBox.setObjectName("max_identical_consecutive_trials_spinBox")
        self.max_identical_consecutive_trials_spinBox.setMaximum(100000)
        self.max_identical_consecutive_trials_spinBox.valueChanged.connect(self.get_max_identical_consecutive_trial)
        self.max_identical_consecutive_trials_horizontalLayout.addWidget(self.max_identical_consecutive_trials_spinBox)
        self.max_identical_consecutive_trials_horizontalLayout.setStretch(0, 1)
        self.max_identical_consecutive_trials_horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.max_identical_consecutive_trials_horizontalLayout)
        # set max trial duration
        self.max_trial_duration_horizontalLayout.setObjectName("max_trial_duration_horizontalLayout")
        self.max_time_duration_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.max_time_duration_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.max_time_duration_label.setObjectName("max_time_duration_label")
        self.max_trial_duration_horizontalLayout.addWidget(self.max_time_duration_label)
        self.max_time_duration_spinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.max_time_duration_spinBox.setObjectName("max_time_duration_spinBox")
        self.max_time_duration_spinBox.setMaximum(100000000)
        self.max_time_duration_spinBox.valueChanged.connect(self.get_max_time_duration)
        self.max_trial_duration_horizontalLayout.addWidget(self.max_time_duration_spinBox)
        self.max_trial_duration_horizontalLayout.setStretch(0, 1)
        self.max_trial_duration_horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.max_trial_duration_horizontalLayout)
        # set events-ports map
        self.events_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.events_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.events_label.setObjectName("events_label")
        self.verticalLayout.addWidget(self.events_label)
        self.event_port_tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.event_port_tableWidget.setStyleSheet("font: 12pt \"David\";")
        self.event_port_tableWidget.setObjectName("event_port_tableWidget")
        self.event_port_tableWidget.setColumnCount(0)
        self.event_port_tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.event_port_tableWidget)
        # set data in table

        # data for each: name, port, input/output, digital/analog, is reward
        for i in range(5):
            column_position = self.event_port_tableWidget.columnCount()
            self.event_port_tableWidget.insertColumn(column_position)
        for i in range(len(self.event_config)):
            row_position = self.event_port_tableWidget.rowCount()
            self.event_port_tableWidget.insertRow(row_position)
            for j in range(1, len(self.event_config[i])):
                self.event_port_tableWidget.setItem(row_position, j - 1, QTableWidgetItem(self.event_config[i][j]))
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
        self.success_rate_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.success_rate_label.setStyleSheet("font: 15pt \"Gabriola\";")
        self.success_rate_label.setObjectName("success_rate_label")
        self.verticalLayout.addWidget(self.success_rate_label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        spacer_item = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.window_gridLayout.addItem(spacer_item, 2, 0, 1, 1)
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        spacer_item1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.navigation_horizontalLayout.addItem(spacer_item1)
        # set back button
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        # set ok button
        self.ok_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.ok_pushButton.clicked.connect(self.accept)
        self.navigation_horizontalLayout.addWidget(self.ok_pushButton)
        spacer_item2 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(spacer_item2)
        self.navigation_horizontalLayout.setStretch(0, 1)
        self.navigation_horizontalLayout.setStretch(1, 1)
        self.navigation_horizontalLayout.setStretch(2, 1)
        self.navigation_horizontalLayout.setStretch(3, 1)
        self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 3, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        # define a connection for each option to set a path for log file and db file
        self.log_file_path_cfg()
        self.db_file_path_cfg()
        # set vm current data to display
        self.log_file_path_lineEdit.setText(self.folder_log_file_path)
        self.db_path_textEdit.setText(self.file_db_file_path)
        self.db_section_lineEdit.setText(self.db_section)
        self.max_identical_consecutive_trials_spinBox.setValue(self.vm.max_successive_trials)
        self.max_time_duration_spinBox.setValue(self.vm.max_trial_length)

    def log_file_path_cfg(self):
        self.insert_log_file_path_radioButton.toggled \
            .connect(lambda: self.log_file_path_state(self.insert_log_file_path_radioButton))
        self.choose_log_file_path_radioButton.toggled \
            .connect(lambda: self.log_file_path_state(self.choose_log_file_path_radioButton))

    def log_file_path_state(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "Insert path":
                self.choose_log_file_folder_pushButton.setEnabled(False)
                self.log_file_path_lineEdit.setEnabled(True)
                self.log_file_path_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
                self.log_file_path_lineEdit.editingFinished.connect(self.on_log_file_path_changed)
            if btn.text() == "Choose folder":
                self.choose_log_file_folder_pushButton.setEnabled(True)
                self.log_file_path_lineEdit.setEnabled(False)

    def on_log_file_path_changed(self):
        self.folder_log_file_path = self.log_file_path_lineEdit.text()

    def on_folder_click(self):
        dialog = QtWidgets.QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.folder_log_file_path = folder_path
        self.log_file_path_lineEdit.setText(self.folder_log_file_path)

    def db_file_path_cfg(self):
        self.insert_db_file_path_radioButton.toggled \
            .connect(lambda: self.db_file_path_state(self.insert_db_file_path_radioButton))
        self.choose_db_file_radioButton.toggled \
            .connect(lambda: self.db_file_path_state(self.choose_db_file_radioButton))

    def db_file_path_state(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "Insert path":
                self.choose_db_file_pushButton.setEnabled(False)
                self.db_path_textEdit.setEnabled(True)
            if btn.text() == "Choose file":
                self.choose_db_file_pushButton.setEnabled(True)
                self.db_path_textEdit.setEnabled(False)

    def on_file_click(self):
        dialog = QtWidgets.QFileDialog()
        file_path = dialog.getOpenFileName(None, "Select File")
        self.file_db_file_path = file_path[0]
        self.db_path_textEdit.setText(self.file_db_file_path)

    def get_max_identical_consecutive_trial(self):
        self.max_identical_consecutive_trial = self.max_identical_consecutive_trials_spinBox.value()

    def get_max_time_duration(self):
        self.max_time_duration = self.max_time_duration_spinBox.value()

    def on_db_section_changed(self):
        self.db_section = self.db_section_lineEdit.text()

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close

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

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Settings"))
        self.headline_label.setText(_translate("main", "Settings"))
        self.log_file_path_label.setText(_translate("main", "Log file path:"))
        self.insert_log_file_path_radioButton.setText(_translate("main", "Insert path"))
        self.choose_log_file_path_radioButton.setText(_translate("main", "Choose folder"))
        self.choose_log_file_folder_pushButton.setText(_translate("main", "Folder"))
        self.db_file_path_label.setText(_translate("main", "Database file path:"))
        self.insert_db_file_path_radioButton.setText(_translate("main", "Insert path"))
        self.choose_db_file_radioButton.setText(_translate("main", "Choose file"))
        self.choose_db_file_pushButton.setText(_translate("main", "File"))
        self.db_section_label.setText(_translate("main", "Database section: "))
        self.max_identical_consecutive_trials_label.setText(_translate("main", "Max identical consecutive trials:"))
        self.max_time_duration_label.setText(_translate("main", "Max trial duration:"))
        self.events_label.setText(_translate("main", "Events to port:"))
        self.success_rate_label.setText(_translate("main", "Success definition:"))
        self.back_pushButton.setText(_translate("main", "Back"))
        self.ok_pushButton.setText(_translate("main", "Ok"))

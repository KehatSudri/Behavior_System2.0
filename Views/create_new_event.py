from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QPushButton

from Views.utils import error_warning, notification, get_ui_path, get_qss_path


class CreateEventUi(object):
    def __init__(self, parent):
        self.digital_radio_btn = None
        self.analog_radio_btn = None
        self.output_radio_btn = None
        self.input_radio_btn = None
        self.vm = parent.vm
        self.main_window = None
        self.event_name_lineEdit = None
        self.event_port_lineEdit = None
        self.is_reward_comboBox = None
        self.digital_description_label = None
        self.analog_description_label = None
        self.add_pushButton = None
        self.back_pushButton = None

    def setupUi(self, main_window):
        uic.loadUi(get_ui_path('create_new_event.ui'), main_window)

        qss = get_qss_path('create_new_event')
        with open(qss, "r") as fh:
            main_window.setStyleSheet(fh.read())

        self.main_window = main_window
        self.event_name_lineEdit = main_window.findChild(QtWidgets.QLineEdit, 'event_name_lineEdit')
        self.event_port_lineEdit = main_window.findChild(QtWidgets.QLineEdit, 'event_port_lineEdit')
        self.input_radio_btn = main_window.findChild(QtWidgets.QRadioButton, 'input_radio_btn')

        self.output_radio_btn = main_window.findChild(QtWidgets.QRadioButton, 'output_radio_btn')
        self.is_reward_comboBox = main_window.findChild(QtWidgets.QComboBox, 'is_reward_comboBox')
        self.is_reward_comboBox.setEnabled(False)
        self.output_radio_btn.toggled.connect(
            lambda:self.input_event_conf())
        self.analog_radio_btn = main_window.findChild(QtWidgets.QRadioButton, 'analog_radio_btn')
        self.digital_radio_btn = main_window.findChild(QtWidgets.QRadioButton, 'digital_radio_btn')
        digital_description_label = main_window.findChild(QtWidgets.QLabel, 'digital_description_label')
        digital_description_label.setEnabled(False)
        analog_description_label = main_window.findChild(QtWidgets.QLabel, 'analog_description_label')
        analog_description_label.setEnabled(False)
        self.digital_radio_btn.toggled.connect(
            lambda: digital_description_label.setEnabled(self.digital_radio_btn.isChecked()))
        self.analog_radio_btn.toggled.connect(
            lambda: analog_description_label.setEnabled(self.analog_radio_btn.isChecked()))
        back_pushButton = main_window.findChild(QPushButton, 'back_btn')
        back_pushButton.clicked.connect(self.on_back_click)
        add_pushButton = main_window.findChild(QPushButton, 'add_event_btn')
        add_pushButton.clicked.connect(self.cretae_event)

    def input_event_conf(self):
        self.is_reward_comboBox.setEnabled(not self.input_radio_btn.isChecked())
        self.analog_radio_btn.setEnabled(not self.input_radio_btn.isChecked())
        self.digital_radio_btn.setEnabled(not self.input_radio_btn.isChecked())
    def cretae_event(self):
        io_btn_val = ""
        if self.input_radio_btn.isChecked():
            io_btn_val = self.input_radio_btn.text()
        elif self.output_radio_btn.isChecked():
            io_btn_val = self.output_radio_btn.text()

        analog_digital_val = None
        if self.analog_radio_btn.isChecked():
            analog_digital_val = self.analog_radio_btn.text()
        elif self.digital_radio_btn.isChecked():
            analog_digital_val = self.digital_radio_btn.text()

        if self.event_name_lineEdit.text() == "" or self.event_port_lineEdit.text() == "" or io_btn_val == "":
            error_warning("not all data is filled")
            return
        error_value = self.vm.verify_insert_hardware_event(self.event_name_lineEdit.text(), self.event_port_lineEdit.text(),
                                             io_btn_val,
                                             analog_digital_val,
                                             str(self.is_reward_comboBox.currentText() == "Yes"))
        if error_value == -1:
            error_warning("Event name already exist")
            return
        elif not error_value == 0:
            error_warning(f'There is already event with these parameters called "{error_value}"')
            return
        self.vm.insert_hardware_event_to_DB(self.event_name_lineEdit.text(), self.event_port_lineEdit.text(),
                                            io_btn_val,
                                            analog_digital_val,
                                            str(self.is_reward_comboBox.currentText() == "Yes" and not self.input_radio_btn.isChecked() ) )
        notification("Event was created")

    def on_back_click(self):
        self.main_window.close()

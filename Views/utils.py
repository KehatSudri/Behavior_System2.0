from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QComboBox
import yaml


def error_warning(massage):
    error_msg_box = QMessageBox()
    error_msg_box.setIcon(QMessageBox.Information)
    error_msg_box.setText(massage)
    # error_msg_box.setText("An error accrued, please try again.")
    error_msg_box.setWindowTitle("Error Warning")
    error_msg_box.exec()

def notification(massage):
    notification_msg_box = QMessageBox()
    notification_msg_box.setIcon(QMessageBox.Information)
    notification_msg_box.setText(massage)
    # error_msg_box.setText("An error accrued, please try again.")
    notification_msg_box.setWindowTitle("Notification")
    notification_msg_box.exec()


def dict_yaml_style(d):
    result = yaml.dump(dict(d), sort_keys=False, default_flow_style=False, default_style='')
    return result


def dict_one_line_style(d):
    result = ""
    # for trial in d:
    for event, params in d.items():
        result += event + " - "
        for param, value in params.items():
            result += param + ':' + str(value) + ", "
    return result[:-2]


def get_string_dict(d):
    cast_str = lambda x: int(x) if x.isnumeric() else x
    d_casting_int = {}
    for outer_k, outer_v in d.items():
        d_casting_int[outer_k] = {}
        for event, params in outer_v.items():
            d_casting_int[outer_k][event] = {}
            for param, value in params.items():
                d_casting_int[outer_k][event][param] = cast_str(value)
    return d_casting_int


def list_to_str(my_list):
    result = ""
    for element in my_list:
        result += str(element) + ", "
    return result[:-2]
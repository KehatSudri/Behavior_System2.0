import os
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox


def error_warning(massage):
    error_msg_box = QMessageBox()
    error_msg_box.setIcon(QMessageBox.Icon.Information)
    error_msg_box.setText(massage)
    error_msg_box.setWindowTitle("Error Warning")
    error_msg_box.exec()


def notification(massage):
    notification_msg_box = QMessageBox()
    notification_msg_box.setIcon(QMessageBox.Icon.Information)
    notification_msg_box.setText(massage)
    notification_msg_box.setWindowTitle("Notification")
    notification_msg_box.exec()


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


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ui_path(name):
    return get_resource_path(os.path.join('UI', name))

def get_qss_path(name):
    return str(Path(__file__).parent.parent / 'QSS' / name)

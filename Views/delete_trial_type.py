from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from Views.utils import error_warning, get_ui_path


class WarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning")
        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to remove this trial type?")
        self.layout.addWidget(message)
        self.setLayout(self.layout)


class DeleteTrialTypeUi(object):
    def __init__(self, parent):
        self.table = None
        self.parent = parent
        self.vm = self.parent.vm
        self.main_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.gridLayout = None
        self.scroll_verticalLayout = QtWidgets.QVBoxLayout()
        self.remove_horizontalLayout = QtWidgets.QHBoxLayout()
        self.remove_pushButton = None
        self.trial_types_label = None
        self.trial_types_tableWidget = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None
        self.trial_types = self.vm.get_list_trials_types_def()
        self.selected_trial_type = None
        self.trials_names = self.vm.get_trial_names()
        self.is_error = False

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('delete_trial_type.ui'), main_window)

        self.back_pushButton = main_window.findChild(QPushButton, 'back_pushButton')
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.table = main_window.findChild(QtWidgets.QTableWidget, 'trial_types_tableWidget')
        for row, data in enumerate(self.trial_types):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(data))
        self.remove_pushButton = main_window.findChild(QPushButton, 'remove_pushButton')
        self.remove_pushButton.clicked.connect(self.on_remove_click)

    def on_remove_click(self):
        is_not_empty = len(self.trial_types) > 0
        chosen_row = self.table.currentRow()
        is_row_selected = chosen_row != -1
        if is_not_empty and is_row_selected:
            # get the chosen block's row and remove it
            item = self.table.item(chosen_row, 0)
            self.vm.delete_trial_type(item.text())
            del self.trial_types[chosen_row]
            self.table.removeRow(chosen_row)
        elif is_not_empty:
            error_warning("Please select a trial.")
        else:
            error_warning("There are no trial types in the system.")

    def on_back_click(self):
        if not self.is_error:
            self.parent.main_window.show()
            self.main_window.close()

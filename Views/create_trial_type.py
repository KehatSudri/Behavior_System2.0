from PyQt6 import QtWidgets, uic
from Views.utils import error_warning, get_ui_path


class CreateTrialTypeUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None
        self.scrollArea = None
        self.trial_type_name_lineEdit = None
        self.simple_radioButton = None
        self.add_event_pushButton = None
        self.events = self.parent.vm.model.get_all_events_by_name()
        self.events_comboBox = None
        self.remove_event_pushButton = None
        self.events_tableWidget = None
        self.accept_pushButton = None
        self.chosen_is_contingent = False
        self.contingent_comboBox = None
        self.events_order = []
        self.is_contingent_order = []

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('create_trial_type.ui'), main_window)
        back_btn = main_window.findChild(QtWidgets.QPushButton, 'back_pushButton')
        back_btn.clicked.connect(self.on_back_click)
        self.contingent_comboBox = main_window.findChild(QtWidgets.QComboBox, 'comboBox_3')
        self.contingent_comboBox.setEnabled(False)
        self.simple_radioButton = main_window.findChild(QtWidgets.QRadioButton, 'simple_radioButton')
        self.simple_radioButton.setChecked(True)
        self.conti_radioButton = main_window.findChild(QtWidgets.QRadioButton, 'contigent_radioButton')
        self.conti_radioButton.toggled.connect(lambda: self.contingent_comboBox.setEnabled(True))
        self.simple_radioButton.toggled.connect(lambda: self.contingent_comboBox.setEnabled(False))
        self.events_comboBox = main_window.findChild(QtWidgets.QComboBox, 'comboBox')
        self.events_comboBox.addItems([event[0] for event in self.events])
        self.events_tableWidget = main_window.findChild(QtWidgets.QTableWidget, 'events_tableWidget')
        self.events_tableWidget.setColumnWidth(0, int(self.events_tableWidget.width() / 2))
        self.add_event_pushButton = main_window.findChild(QtWidgets.QPushButton, 'Add_event_pushButton')
        self.add_event_pushButton.clicked.connect(self.on_add_click)
        self.remove_event_pushButton = main_window.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.remove_event_pushButton.clicked.connect(self.on_remove_click)
        self.accept_pushButton = main_window.findChild(QtWidgets.QPushButton, 'create_trial_btn')
        self.accept_pushButton.clicked.connect(self.create_trial)
        self.trial_type_name_lineEdit = main_window.findChild(QtWidgets.QLineEdit, 'lineEdit')

    def on_add_click(self):
        # add an event to the current trial type
        row_position = self.events_tableWidget.rowCount()
        current_event = self.events_comboBox.currentText()
        self.events_tableWidget.setRowCount(row_position + 1)
        self.events_tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(current_event))
        if self.simple_radioButton.isChecked():
            self.events_tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem("Simple"))
        else:
            self.events_tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem("Contingent"))
            self.events_tableWidget.setItem(row_position, 2,
                                            QtWidgets.QTableWidgetItem(self.contingent_comboBox.currentText()))
        self.events_order.append(current_event)
        self.is_contingent_order.append(self.chosen_is_contingent)
        self.contingent_comboBox.addItems([current_event])
        self.events_tableWidget.setColumnWidth(0, int(self.events_tableWidget.width() / 2))

    def on_remove_click(self):
        is_not_empty = len(self.events_order) > 0
        chosen_row = self.events_tableWidget.currentRow()
        is_col_selected = chosen_row != -1
        # check if there are events and an event was selected
        if is_not_empty and is_col_selected:
            del self.events_order[chosen_row]
            del self.is_contingent_order[chosen_row]
            index = self.contingent_comboBox.findText(self.events_tableWidget.item(chosen_row, 0).text())
            if index >= 0:
                self.contingent_comboBox.removeItem(index)
            self.contingent_comboBox.addItems
            self.events_tableWidget.removeRow(chosen_row)
            # set current column to be unselected
            self.events_tableWidget.setCurrentCell(-1, self.events_tableWidget.currentRow())
        # error cases
        elif is_not_empty:
            error_warning("An event is not selected.")
        else:
            error_warning("There are no events in the current trial.")

    def create_trial(self):
        msgBox = QtWidgets.QMessageBox()
        name = self.trial_type_name_lineEdit.text()
        events = self.events_order
        if len(events) == 0:
            error_warning("There are no events in the current trial.")
            return
        if len(name) == 0 or name.isspace():
            error_warning("Please enter name for this trial.")
            return

        verify_ans = self.parent.vm.verify_trial_insert(name, events)
        if verify_ans == -1:
            msgBox.setText("Trial name is already in use.")
            msgBox.exec()
            return
        elif verify_ans is not None:
            verify_ans = verify_ans[0]
            msgBox.setText(f'A Trial with this events order already exist with name "{verify_ans}".')
            msgBox.exec()
            return

        self.parent.vm.add_trial_type(name, events)
        for row in range(self.events_tableWidget.rowCount()):
            row_items = []
            for col in range(self.events_tableWidget.columnCount()):
                item = self.events_tableWidget.item(row, col)
                if item is not None:
                    row_items.append(item.text())
            if len(row_items) == 3:
                self.parent.vm.events_to_trials(name, row_items[0], True, row_items[2])
            else:
                self.parent.vm.events_to_trials(name, row_items[0], False, None)
        msgBox.setText("The trial was created successfully.")
        msgBox.exec()
        self.trial_type_name_lineEdit.clear()
        self.events_order = []
        while self.events_tableWidget.rowCount() > 0:
            self.events_tableWidget.removeRow(0)

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

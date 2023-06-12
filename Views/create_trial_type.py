from PyQt6 import QtWidgets, uic
from Views.utils import error_warning, get_ui_path


class CreateTrialTypeUi(object):
    def __init__(self, parent):
        self.conti_radioButton = None
        self.frequency_line_edit = None
        self.conti_label = None
        self.random_comboBox = None
        self.parent = parent
        self.main_window = None
        self.trial_type_name_lineEdit = None
        self.simple_radioButton = None
        self.events = self.parent.vm.model.get_all_events_by_name()
        self.events_comboBox = None
        self.events_tableWidget = None
        self.chosen_is_contingent = False
        self.contingent_comboBox = None
        self.events_order = []
        self.is_contingent_order = []
        self.vm = parent.vm

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('create_trial_type.ui'), main_window)
        back_btn = main_window.findChild(QtWidgets.QPushButton, 'back_pushButton')
        back_btn.clicked.connect(self.on_back_click)
        random_label = main_window.findChild(QtWidgets.QLabel, 'label_4')
        accept_pushButton = main_window.findChild(QtWidgets.QPushButton, 'create_trial_btn')
        remove_event_pushButton = main_window.findChild(QtWidgets.QPushButton, 'pushButton_2')
        add_event_pushButton = main_window.findChild(QtWidgets.QPushButton, 'Add_event_pushButton')
        self.isEndCondition = main_window.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.simple_radioButton = main_window.findChild(QtWidgets.QRadioButton, 'simple_radioButton')
        self.random_comboBox = main_window.findChild(QtWidgets.QComboBox, 'ranom_pred_comboBox')
        self.events_comboBox = main_window.findChild(QtWidgets.QComboBox, 'comboBox')
        self.conti_label = main_window.findChild(QtWidgets.QLabel, 'label_2')
        self.contingent_comboBox = main_window.findChild(QtWidgets.QComboBox, 'comboBox_3')
        self.trial_type_name_lineEdit = main_window.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.events_tableWidget = main_window.findChild(QtWidgets.QTableWidget, 'events_tableWidget')
        self.frequency_line_edit = main_window.findChild(QtWidgets.QLineEdit, 'frequency_lineEdit')
        self.conti_radioButton = main_window.findChild(QtWidgets.QRadioButton, 'contigent_radioButton')
        self.contingent_comboBox.setEnabled(False)
        self.conti_label.setEnabled(False)
        self.events_comboBox.currentTextChanged.connect(self.name_comboBox_handler)
        self.events_comboBox.addItems([event[0] for event in self.events])
        self.simple_radioButton.toggled.connect(self.simple_event_handler)
        self.simple_radioButton.setChecked(True)
        self.random_comboBox.addItems(["Random", "Fixed"])
        self.random_comboBox.setEnabled(False)
        self.conti_radioButton.setEnabled(False)
        self.conti_radioButton.toggled.connect(lambda: (
            self.contingent_comboBox.setEnabled(True), self.conti_label.setEnabled(True)))
        self.events_tableWidget.setColumnWidth(0, int(self.events_tableWidget.width() / 2))
        add_event_pushButton.clicked.connect(self.on_add_click)
        remove_event_pushButton.clicked.connect(self.on_remove_click)
        accept_pushButton.clicked.connect(self.create_trial)
        self.simple_event_handler()
        header = self.events_tableWidget.horizontalHeader()

        # Set the size for each section
        header.resizeSection(0, 150)  # Set the size of the first section to 100 pixels
        header.resizeSection(1, 200)  # Set the size of the second section to 200 pixels
        header.resizeSection(2, 150)
        header.resizeSection(3, 150)
        header.resizeSection(4, 150)  #
        header.resizeSection(5, 100)  #

    def on_add_click(self):
        current_event = self.events_comboBox.currentText()
        if current_event=="":
            error_warning("There are no events, please create one first.")
            return
        for row in range(self.events_tableWidget.rowCount()):
            item = self.events_tableWidget.item(row, 0)  # Get item at row, column 0
            if item is not None:
                if current_event == item.text():
                    error_warning("The event already in this trial.")
                    return

        # add an event to the current trial type
        row_position = self.events_tableWidget.rowCount()
        self.events_tableWidget.setRowCount(row_position + 1)
        self.events_tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(current_event))
        if self.simple_radioButton.isChecked():
            self.events_tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem("Simple"))
        else:
            self.events_tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem("Contingent"))
            self.events_tableWidget.setItem(row_position, 2,
                                            QtWidgets.QTableWidgetItem(self.contingent_comboBox.currentText()))
        if self.vm.is_input_event(current_event):
            self.events_tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem("Input"))
        else:
            self.events_tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem("Output"))
        if self.random_comboBox.isEnabled():
            self.events_tableWidget.setItem(row_position, 4,
                                            QtWidgets.QTableWidgetItem(self.random_comboBox.currentText()))
        self.events_tableWidget.setItem(row_position, 5,
                                        QtWidgets.QTableWidgetItem(str(self.isEndCondition.isChecked())))
        self.events_order.append(current_event)
        self.is_contingent_order.append(self.chosen_is_contingent)
        # validate that combo not have duplicates
        flag = 0
        for i in range(self.contingent_comboBox.count()):
            if self.contingent_comboBox.itemText(i) == current_event:
                flag = 1
        if not flag:
            self.contingent_comboBox.addItems([current_event])
        if self.contingent_comboBox.count() >= 1 :
            self.name_comboBox_handler()
            # self.conti_radioButton.setEnabled(True)

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
            self.events_tableWidget.removeRow(chosen_row)
            # set current column to be unselected
            self.events_tableWidget.setCurrentCell(-1, self.events_tableWidget.currentRow())
            if len(self.events_order) == 0:
                self.contingent_comboBox.setEnabled(False)
                self.conti_label.setEnabled(False)
                self.conti_radioButton.setEnabled(False)
                self.simple_radioButton.setChecked(True)

        # error cases
        elif is_not_empty:
            error_warning("An event is not selected.")
        else:
            error_warning("There are no events in the current trial.")

    def create_trial(self):
        msgBox = QtWidgets.QMessageBox()
        name = self.trial_type_name_lineEdit.text()
        events = self.events_order
        if len(name) == 0 or name.isspace():
            error_warning("Please enter name for this trial.")
            return
        if len(events) == 0:
            error_warning("There are no events in the current trial.")
            return

        try:
            self.parent.vm.insert_new_trial(name)
        except Exception as e:
            msg=str(e)
            if "name" in msg:
                error_warning("Error: Trial name already exists.")
            return
        for row in range(self.events_tableWidget.rowCount()):
            row_items = []
            for col in range(self.events_tableWidget.columnCount()):
                item = self.events_tableWidget.item(row, col)
                if item is not None:
                    row_items.append(item.text())
                else: row_items.append(None)

            if row_items[1] == "Contingent":
                    self.parent.vm.insert_new_events_to_trials(name, row_items[0], True, row_items[2],row_items[4]=="Random",False)
            else:
                if self.vm.is_input_event(row_items[0]):
                    self.parent.vm.insert_new_events_to_trials(name, row_items[0], False, None,None,row_items[5]=="True")
                else:
                    self.parent.vm.insert_new_events_to_trials(name, row_items[0], False, None,row_items[4]=="Random",row_items[5]=="True")

        msgBox.setText("The trial was created successfully!")
        msgBox.exec()
        self.trial_type_name_lineEdit.clear()
        self.events_order = []
        while self.events_tableWidget.rowCount() > 0:
            self.events_tableWidget.removeRow(0)
        self.contingent_comboBox.clear()

    def simple_event_handler(self):
        self.contingent_comboBox.setEnabled(False)
        self.conti_label.setEnabled(False)
        if not self.vm.is_input_event(self.events_comboBox.currentText()):
            self.random_comboBox.setEnabled(True)

    def name_comboBox_handler(self):
        if self.vm.is_input_event(self.events_comboBox.currentText()):
            self.random_comboBox.setEnabled(False)
            self.contingent_comboBox.setEnabled(False)
            self.conti_label.setEnabled(False)
            self.conti_radioButton.setEnabled(False)
            self.simple_radioButton.setChecked(True)
            self.isEndCondition.setEnabled(True)
        else:
            self.isEndCondition.setChecked(False)
            self.isEndCondition.setEnabled(False)

            self.random_comboBox.setEnabled(True)
            self.random_comboBox.setEnabled(True)
            # self.contingent_comboBox.setEnabled(True)
            # self.conti_label.setEnabled(True)
            if self.contingent_comboBox.count() >= 1:
                self.conti_radioButton.setEnabled(True)



    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

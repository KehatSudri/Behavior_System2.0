from collections import defaultdict
from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QLabel, QLineEdit, QFormLayout
from Views.utils import get_ui_path
from Models.DB_INIT import DB


class EditSessionUi(object):
    def __init__(self, parent):
        self.db = DB()
        self.index = 0
        self.parent = parent
        self.vm = parent.vm
        self.background_gridLayout = None
        self.main_verticalLayout = None
        self.add_trial_label = None
        self.trial_types_label = None
        self.trial_types_comboBox = None
        self.ok_btn = None
        self.verticalScrollBar = None
        self.set_trials_table_pointer = None
        self.trial_params_labels = []
        self.trial_params_widgets = defaultdict(list)
        self.are_contingents = []
        self.formLayout = parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')
        self.db = DB()

    def setupUi(self, dialog, session_id):
        uic.loadUi(get_ui_path('edit_session_template.ui'), dialog)
        self.trial_types_comboBox = dialog.findChild(QtWidgets.QComboBox, 'trial_types_comboBox')
        trials = self.db.get_trial_name_by_session(session_id)
        self.trial_types_comboBox.addItems([name[0] for name in trials])
        self.trial_types_comboBox.activated.connect(self.trial_types_click)
        self.trial_types_click(0)
        self.ok_btn = dialog.findChild(QtWidgets.QDialogButtonBox, 'ok_btn')
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(dialog.reject)

    def delete_params(self):

        for i in range(len(self.trial_params_labels)):
            label = self.trial_params_labels.pop()
            self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').removeRow(label)
        # init the lists tha holds the widgets for each row
        self.trial_params_labels = []
        self.trial_params_widgets = defaultdict(list)
        self.are_contingents.clear()

        for i in range(self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').rowCount() - 1, -1, -1):
            # Get the widget in the current row
            widget = self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').itemAt(i).widget()
            if widget is not None:
                # Remove the current row from the layout
                self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').removeRow(i)

    def set_trial_form(self, events_name: list, chosenTrial):
        # add row for each event and it's parameters
        for i, event_name in enumerate(events_name):
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            label = QLabel(event_name + "")
            label.setFont(bold_font)
            self.trial_params_labels.append(label)
            formLayout = self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')
            if not self.vm.is_input_event(event_name):
                formLayout.addRow(label)
                self.set_trial_form_handler(event_name, chosenTrial)

    def set_trial_form_handler(self, event_name: str, chosenTrial):
        if self.db.is_random_event_in_a_given_trial(chosenTrial, event_name)[0]:
            params = ["min delay (ms)", "max delay (ms)"]
        else:
            params = ["delay (ms)"]
        if event_name.find("Tone") != -1:
            params = params + ['duration (ms)', 'frequency (Hz)', 'amplitude (db)']
        elif event_name == 'Reward':
            params = params + ['duration (ms)']
        else:
            params = params + ["duration (ms)"]

        for param in params:
            label = QLabel(param)
            line_edit = QLineEdit()
            line_edit.setText("0")
            self.trial_params_labels.append(label)
            self.trial_params_widgets[event_name].append(line_edit)
            self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').addRow(label, line_edit)

    def trial_types_click(self, index):
        self.parent.trial_index = index
        if len(self.parent.trials_names) == 0:
            return
        chosen = self.parent.chosen_trial_type_name = [name[0] for name in self.parent.trials_names][index]
        chosen = self.trial_types_comboBox.currentText()
        events_name = self.vm.get_events_by_trial_name(chosen)
        events_name = [item[0] for item in events_name]
        self.clear_form()
        self.set_trial_form(events_name, chosen)

    def clear_form(self):
        if len(self.trial_params_labels) != 0:
            self.delete_params()

    def accept(self):
        # new_trial = self.parent.chosen_trial_type_name
        new_trial=self.trial_types_comboBox.currentText()
        event_and_params = {}
        params = []
        for i in range(self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').rowCount()):
            field = self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').itemAt(i,
                                                                                                 QFormLayout.ItemRole.FieldRole)
            if not isinstance(field.widget(), QLineEdit):
                event = field.widget().text()
                params = []
            else:
                params.append(field.widget().text())

            if event != "" and event is not None:
                event_and_params[event] = params
        #find the index to replace with the updated value
        rowsCount = self.parent.trials_table.rowCount()
        index=0
        for row in range(rowsCount):
            if self.parent.trials_table.item(row,0) is not None:
                if self.parent.trials_table.item(row,0).text() == new_trial:
                    index=row
        self.parent.trials_table.removeRow(index)

        for i in range(len(self.parent.trials_in_session)):
            if self.parent.trials_in_session[i] == new_trial:
                del self.parent.trials_in_session[i]
                del self.parent.trials_in_session[i]
                break
        self.parent.trials_in_session.extend([new_trial, event_and_params])


        self.parent.set_trials_table()
        self.parent.add_window.close()

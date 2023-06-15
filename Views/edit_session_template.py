from collections import defaultdict, OrderedDict

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout

from Views.utils import error_warning, get_string_dict, get_ui_path
from Models.DB_INIT import DB


class EditSessionUi(object):
    def __init__(self, parent):
        self.index = 0
        self.parent = parent
        self.vm = parent.vm
        self.background_gridLayout = None
        self.main_verticalLayout = None
        self.add_trial_label = None
        self.trial_types_label = None
        self.trial_types_comboBox = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.verticalLayout = None
        self.ok_btn = None
        self.verticalScrollBar = None
        self.set_trials_table_pointer = None
        self.trial_params_labels = []
        self.trial_params_widgets = defaultdict(list)
        # TODO delete when self.vm.is_contingent(event_name) implemented
        self.are_contingents = []
        self.formLayout = parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')
        self.db=DB()

    def setupUi(self, dialog ,session_name):
        uic.loadUi(get_ui_path('edit_session_template.ui'), dialog)
        self.trial_types_comboBox = dialog.findChild(QtWidgets.QComboBox, 'trial_types_comboBox')
        trials=self.db.get_trial_name_by_session(session_name)
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
        self.are_contingents.clear()  # TODO delete when self.vm.is_contingent(event_name) implemented

        for i in range(self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').rowCount() - 1, -1, -1):
            # Get the widget in the current row
            widget = self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').itemAt(i).widget()
            if widget is not None:
                # Remove the current row from the layout
                self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').removeRow(i)

    def set_trial_form(self, events_name: list):
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

            # add line edit accordingly for the parameters
                self.set_trial_form_handler(event_name, self.vm.is_input_event(event_name))


    def set_trial_form_handler(self, event_name: str, is_input_event):
        dict = ["delay"]
        if event_name == 'Tone':
            dict = dict + ['duration', 'frequency','tone amplitude']
        elif event_name == 'Reward':
            dict = dict + ['duration']
        else:
            dict = dict + ["duration"]

        for param in dict:
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
        events_name = self.vm.get_events_by_trial_name(chosen)
        events_name = [item[0] for item in events_name]
        self.clear_form()
        self.set_trial_form(events_name)

    def clear_form(self):
        if len(self.trial_params_labels) != 0:
            self.delete_params()

    def accept(self):
        new_trial = self.parent.chosen_trial_type_name
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


        self.parent.trials_in_session.extend([new_trial, event_and_params])
        self.parent.set_trials_table()
        self.parent.add_window.close()

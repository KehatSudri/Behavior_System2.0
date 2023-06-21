from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel, QDialogButtonBox, QVBoxLayout, QLineEdit, QComboBox
from Views.utils import error_warning, get_string_dict


class EditTrialUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.window_gridLayout = None
        self.main_verticalLayout = QtWidgets.QVBoxLayout()
        self.edit_trial_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = None
        self.buttonBox = None
        self.formLayout = QtWidgets.QFormLayout()
        self.trial_params_labels = []
        self.trial_params_widgets = collections.defaultdict(list)
        self.set_trials_table_pointer = None

    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(398, 386)
        self.window_gridLayout = QtWidgets.QGridLayout(dialog)
        self.window_gridLayout.setObjectName("window_gridLayout")
        self.main_verticalLayout.setObjectName("main_verticalLayout")
        self.edit_trial_label = QtWidgets.QLabel(dialog)
        self.edit_trial_label.setStyleSheet("font: 22pt \"Arial\";")
        self.edit_trial_label.setObjectName("edit_trial_label")
        self.main_verticalLayout.addWidget(self.edit_trial_label)
        self.scrollArea = QtWidgets.QScrollArea(dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 305))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.main_verticalLayout.addWidget(self.scrollArea)
        self.main_verticalLayout.setStretch(2, 3)
        self.main_verticalLayout.setStretch(3, 10)
        self.window_gridLayout.addLayout(self.main_verticalLayout, 0, 0, 1, 1)
        self.retranslateUi(dialog)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.window_gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        # present params of the chosen trial
        self.update()

    def update(self):
        self.set_trials_table_pointer = self.parent.set_trials_table_pointer
        self.create_form()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.buttonBox)

    def create_form(self):
        # get the chosen trial type and set it's parameters
        self.parent.selected_trial = self.parent.trials_tableWidget.currentRow()
        self.parent.chosen_trial_type_name = [*self.parent.trials_in_session[self.parent.selected_trial].keys()][0]
        events_name = [
            *self.parent.trials_in_session[self.parent.trials_tableWidget.currentRow()][
                self.parent.chosen_trial_type_name].keys()]
        self.set_trial_form(events_name)

    def set_trial_form(self, events_name: list):
        # add row for each event accordingly
        is_contingent = None
        event_name_font = QtGui.QFont()
        event_name_font.setBold(True)
        for event_name in events_name:
            # add a label for the event name
            event_name_font = QtGui.QFont()
            event_name_font.setBold(True)
            label = QLabel(event_name + ":")
            label.setFont(event_name_font)
            self.trial_params_labels.append(label)
            self.formLayout.addRow(label)
            # add line edit accordingly for the parameters
            if self.vm.is_contingent(event_name):  # contingent event case
                is_contingent = True
                self.set_trial_form_handler(is_contingent, event_name)
            else:
                is_contingent = False
                self.set_trial_form_handler(is_contingent, event_name)

    def set_trial_form_handler(self, is_contingent: bool, event_name: str):
        if is_contingent:  # contingent event case
            event_dict = {"Conditioned event": True, "Interval from input": False, "Wanted event": True,
                          "Wanted event time range": {"Min": False, "Max": False}, "Not wanted event": True,
                          "Not wanted event time range": {"Min": False, "Max": False}}
            for param, value in event_dict:  # event's
                label = QLabel(param)
                self.trial_params_labels.append(label)
                if type(value) == bool:  # check if not range case
                    if value:  # check if ComboBox case
                        combo_box = QComboBox()
                        self.trial_params_widgets[event_name].append(combo_box)
                        self.formLayout.addRow(label, combo_box)
                    else:
                        # SpinBox case
                        spin_box = QtWidgets.QSpinBox()
                        spin_box.setMaximum(100000)
                        self.trial_params_widgets[event_name].append(spin_box)
                        self.formLayout.addRow(label, spin_box)
                else:  # range case
                    self.formLayout.addRow(label)
                    for key, val in value.items():
                        if val:  # check if ComboBox case
                            label = QLabel(key)
                            combo_box = QComboBox()
                            self.trial_params_labels.append(label)
                            self.trial_params_widgets[event_name].append(combo_box)
                            self.formLayout.addRow(label, combo_box)
                        else:
                            # SpinBox case
                            label = QLabel(key)
                            spin_box = QtWidgets.QSpinBox()
                            spin_box.setMaximum(100000)
                            self.trial_params_labels.append(label)
                            self.trial_params_widgets[event_name].append(spin_box)
                            self.formLayout.addRow(label, spin_box)
        else:  # simple event case
            event_params = \
                list(self.parent.trials_in_session[self.parent.selected_trial][self.parent.chosen_trial_type_name][
                         event_name].keys())
            for param in event_params:  # event's params
                label = QLabel(param)
                line_edit = QLineEdit()
                self.trial_params_labels.append(label)
                # set current text value of param on line edit button
                line_edit.setText(str(
                    self.parent.trials_in_session[self.parent.selected_trial][self.parent.chosen_trial_type_name][
                        event_name][
                        param]))
                self.trial_params_widgets[event_name].append(line_edit)
                self.formLayout.addRow(label, line_edit)

    def are_valid_values(self, edited_trial):
        for param, val in edited_trial.items():
            if not val:
                return False
        return True

    def accept(self):
        edited_trial = self.parent.trial_types[self.parent.chosen_trial_type_name]
        # update the edited trial parameters
        for event, event_params in edited_trial.items():
            params_values = {param: self.trial_params_widgets[event][i].text() for i, param in enumerate(event_params)}
            # check if not an empty input
            if not self.are_valid_values(params_values):
                error_warning("An error accrued, please try again.")
                return
            edited_trial[event] = params_values
        # add new trial
        trial_index, trial_name = self.parent.selected_trial, self.parent.chosen_trial_type_name
        self.parent.trials_in_session[trial_index][trial_name] = edited_trial
        get_string_dict(self.parent.trials_in_session[trial_index])

        # update trials table on the window
        self.set_trials_table_pointer()
        self.parent.edit_window.close()

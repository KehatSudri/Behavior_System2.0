from collections import defaultdict, OrderedDict

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QComboBox

from Views.utils import error_warning, get_string_dict, get_ui_path  # , set_conditioned_event


class AddTrialUi(object):
    def __init__(self, parent):
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
        self.buttonBox = None
        self.verticalScrollBar = None
        self.formLayout = parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')

        self.trial_params_labels = []
        self.trial_params_widgets = defaultdict(list)
        self.set_trials_table_pointer = None
        #self.trial_types_click(0)
        # TODO delete when self.vm.is_contingent(event_name) implemented
        self.are_contingents = []
        # self.contingents = OrderedDict()

    def setupUi(self, dialog):
        uic.loadUi(get_ui_path('add_trial.ui'), dialog)
        self.trial_types_comboBox = dialog.findChild(QtWidgets.QComboBox, 'trial_types_comboBox')
        self.trial_types_comboBox.addItems([name[0] for name in self.parent.trials_names])
        self.trial_types_comboBox.activated.connect(self.trial_types_click)
        self.buttonBox = dialog.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        # present params of the chosen trial
        #self.update()
        #present first trial type as default
        #self.trial_types_click(0)

    # def update(self):
    #     self.set_trials_table_pointer = self.parent.set_trials_table_pointer
    #     # creating a dialog button for ok and cancel
    #     #self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    #     # connect the OK button to function
    #     self.buttonBox.accepted.connect(self.accept)
    #     # adding action when form is rejected
    #     # self.buttonBox.rejected.connect(reject)
    #     # creating a vertical layout
    #     main_layout = QVBoxLayout()
    #     # adding button box to the layout
    #     main_layout.addWidget(self.buttonBox)

    def delete_params(self):
        for i in range(len(self.trial_params_labels)):
            label = self.trial_params_labels.pop()
            self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').removeRow(label)
        # init the lists tha holds the widgets for each row
        self.trial_params_labels = []
        self.trial_params_widgets = defaultdict(list)
        self.are_contingents.clear()  # TODO delete when self.vm.is_contingent(event_name) implemented

    def set_trial_form(self, events_name: list):
        index = 0  # TODO delete when self.vm.is_contingent(event_name) implemented
        # add row for each event and it's parameters
        for event_name in events_name:
            is_contingent = self.vm.is_contingent(event_name)  # TODO remove when self.vm.is_contingent(event_name) implemented
            # self.are_contingents.append(is_contingent)
            # index += 1
            if not is_contingent:
                # add a label for the event name
                event_name_font = QtGui.QFont()
                event_name_font.setBold(True)
                label = QLabel(event_name + ":")
                label.setFont(event_name_font)
                self.trial_params_labels.append(label)
                formLayout=self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')
                formLayout.addRow(label)
            # add line edit accordingly for the parameters
            self.set_trial_form_handler(event_name, is_contingent)

    def set_trial_form_handler(self, event_name: str, is_contingent: bool):
        if is_contingent:
            # contingent event case
            # key: parameter_label, val: is_text
            event_dict = {"Conditioned event": True, "Interval from input": False, "Wanted event": True,
                          "Wanted event time range": {"Min": False, "Max": False}, "Not wanted event": True,
                          "Not wanted event time range": {"Min": False, "Max": False}}
            events = ["None", "A", "B", "C"]

            for parameter, value in event_dict.items():  # event's
                if type(value) == bool:  # check if not range case
                    # params
                    if value:  # check if ComboBox case
                        label = QLabel(parameter)
                        combo_box = QComboBox()
                        combo_box.addItems(events)  # TODO need to get list of events
                        combo_box.setCurrentIndex(0)
                        self.trial_params_labels.append(label)
                        self.trial_params_widgets[event_name].append(combo_box)
                        self.formLayout.addRow(label, combo_box)
                    else:
                        # SpinBox case
                        label = QLabel(parameter)
                        spin_box = QtWidgets.QSpinBox()
                        spin_box.setMaximum(100000)
                        self.trial_params_labels.append(label)
                        self.trial_params_widgets[event_name].append(spin_box)
                        self.formLayout.addRow(label, spin_box)
                else:  # range case
                    label = QLabel(parameter)
                    self.trial_params_labels.append(label)
                    self.formLayout.addRow(label)
                    for key, val in value.items():
                        if val:  # check if ComboBox case
                            label = QLabel(key)
                            combo_box = QComboBox()
                            combo_box.addItems(events)  # TODO need to get list of events
                            combo_box.setCurrentIndex(0)
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
        else:
            # simple event case
            for event_parameter in [name[0] for name in self.parent.trials_names]:  # event's
                # params
                label = QLabel(event_parameter)
                line_edit = QLineEdit()
                self.trial_params_labels.append(label)
                self.trial_params_widgets[event_name].append(line_edit)
                self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout').addRow(label, line_edit)

    def trial_types_click(self, index):
        self.parent.trial_index = index
        # get the chosen trial type and set it's parameters
        if len(self.parent.trials_names) == 0:
            return
        chosen = self.parent.chosen_trial_type_name = [name[0] for name in self.parent.trials_names][index]
        events_name = self.vm.get_events_by_trial_name(chosen)
        self.clear_form()
        self.set_trial_form(events_name[0].split(",")[:-1])

    def clear_form(self):
        if len(self.trial_params_labels) != 0:
            self.delete_params()

    def are_valid_values(self, new_trial):
        index = 0
        for event, event_params in new_trial.items():
            if self.vm.is_contingent(event):
            #if self.are_contingents[index]:
                for parameter, value in event.items():  # event's
                    if type(value) != bool:  # check if range case
                        for key, val in value.items():
                            if not val:  # SpinBox case
                                params_values = {param: self.trial_params_widgets[event][i].text() for i, param in
                                                 enumerate(event_params)}
                                for params_key in params_values:
                                    if not params_values[params_key]:
                                        return False
            else:
                params_values = {param: self.trial_params_widgets[event][i].text() for i, param in
                                 enumerate(event_params)}
                for params_key in params_values:
                    if not params_values[params_key]:
                        return False
            index += 1
        return True

    def accept(self):
        new_trial = self.parent.trial_types[1]
        print(new_trial)
        # update new trial parameters
        # for event, event_params in new_trial.items():
        #     params_values = {param: self.trial_params_widgets[event][i].text() for i, param in
        #                      enumerate(event_params)}
        #     new_trial[event] = params_values
        # check if not an empty input
        print(new_trial)
        # if not self.are_valid_values(new_trial):
        #     error_warning("An error accrued, please try again.")
        #     return
        # validate parameters values
        #self.are_valid_values(new_trial)
        # add new trial
        self.parent.trials_in_session.append(get_string_dict({self.parent.chosen_trial_type_name: new_trial}))
        self.parent.percentages.append(0)
        self.parent.percent_per_block.append([0] * len(self.parent.block_list))
        # add a percentage to each block
        # for i in range(len(self.parent.block_list)):
        #     self.parent.prcnt_per_block[i].append()
        # update trials table on the window
        self.set_trials_table_pointer()
        self.parent.add_window.close()

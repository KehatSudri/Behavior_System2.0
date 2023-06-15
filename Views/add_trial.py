from collections import defaultdict, OrderedDict

from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout

from Views.utils import error_warning, get_string_dict, get_ui_path  # , set_conditioned_event


class AddTrialUi(object):
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
        # self.contingents = OrderedDict()
        self.formLayout = parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')

    def setupUi(self, dialog):
        uic.loadUi(get_ui_path('add_trial.ui'), dialog)
        self.trial_types_comboBox = dialog.findChild(QtWidgets.QComboBox, 'trial_types_comboBox')
        self.trial_types_comboBox.addItems([name[0] for name in self.parent.trials_names])
        self.trial_types_comboBox.activated.connect(self.trial_types_click)
        self.trial_types_click(0)
        self.ok_btn = dialog.findChild(QtWidgets.QDialogButtonBox, 'ok_btn')
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(dialog.reject)

        # present params of the chosen trial
        # self.update()
        # present first trial type as default
        # self.trial_types_click(0)

    def update(self):
        self.set_trials_table_pointer = self.parent.set_trials_table_pointer
        # creating a dialog button for ok and cancel
        # self.ok_btn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # connect the OK button to function
        self.ok_btn.accepted.connect(self.accept)
        # adding action when form is rejected
        # self.ok_btn.rejected.connect(reject)
        # creating a vertical layout
        main_layout = QVBoxLayout()
        # adding button box to the layout
        main_layout.addWidget(self.ok_btn)

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
            # print(self.parent.trial_types[0])
            # is_contingent = self.vm.is_contingent(
            #     event_name,self.parent.chosen_trial_type_name)[0]

            # if not is_contingent:
            # add a label for the event name
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
            # if not i == len(events_name) - 1:
            #     delay_label = QLabel("Delay")
            #     delay_label.setFont(bold_font)
            #     line_edit = QLineEdit()
            #     formLayout = self.parent.add_window.findChild(QtWidgets.QFormLayout, 'formLayout')
            #     formLayout.addRow(QLabel(""))
            #     line_edit.setText("0")
            #     formLayout.addRow(delay_label, line_edit)
            #     formLayout.addRow(QLabel(""))

            # if not i == len(events_name) - 1:
            #     print("dddd")
            #     delay_label = QLabel("Delay")
            #     delay_label.setFont(bold_font)
            #     self.trial_params_labels.append(delay_label)
            #     formLayout.addRow(label)
            #     line_edit = QLineEdit()
            #     # formLayout.addRow(QLabel(""))
            #     formLayout.addRow(delay_label,line_edit)
            #     # formLayout.addRow(QLabel(""))

    def set_trial_form_handler(self, event_name: str, is_input_event):
        # if is_contingent:
        #     # contingent event case
        #     # key: parameter_label, val: is_text
        #     event_dict = {"Conditioned event": True, "Interval from input": False, "Wanted event": True,
        #                   "Wanted event time range": {"Min": False, "Max": False}, "Not wanted event": True,
        #                   "Not wanted event time range": {"Min": False, "Max": False}}
        #
        #     events = ["None", "A", "B", "C"]
        #
        #     for parameter, value in event_dict.items():  # event's
        #
        #         if type(value) == bool:  # check if not range case
        #             # params
        #             if value:  # check if ComboBox case
        #                 label = QLabel(parameter)
        #                 combo_box = QComboBox()
        #                 combo_box.addItems(events)  # TODO need to get list of events
        #                 combo_box.setCurrentIndex(0)
        #                 self.trial_params_labels.append(label)
        #                 self.trial_params_widgets[event_name].append(combo_box)
        #                 self.formLayout.addRow(label, combo_box)
        #             else:
        #                 # SpinBox case
        #                 label = QLabel(parameter)
        #                 spin_box = QtWidgets.QSpinBox()
        #                 spin_box.setMaximum(100000)
        #                 self.trial_params_labels.append(label)
        #                 self.trial_params_widgets[event_name].append(spin_box)
        #                 self.formLayout.addRow(label, spin_box)
        #         else:  # range case
        #             label = QLabel(parameter)
        #             self.trial_params_labels.append(label)
        #             self.formLayout.addRow(label)
        #             for key, val in value.items():
        #                 if val:  # check if ComboBox case
        #                     label = QLabel(key)
        #                     combo_box = QComboBox()
        #                     combo_box.addItems(events)  # TODO need to get list of events
        #                     combo_box.setCurrentIndex(0)
        #                     self.trial_params_labels.append(label)
        #                     self.trial_params_widgets[event_name].append(combo_box)
        #                     self.formLayout.addRow(label, combo_box)
        #                 else:
        #                     # SpinBox case
        #                     label = QLabel(key)
        #                     spin_box = QtWidgets.QSpinBox()
        #                     spin_box.setMaximum(100000)
        #                     self.trial_params_labels.append(label)
        #                     self.trial_params_widgets[event_name].append(spin_box)
        #                     self.formLayout.addRow(label, spin_box)
        # else:
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

    def are_valid_values(self, new_trial):
        index = 0
        for event, event_params in new_trial.items():
            if self.vm.is_contingent(event, new_trial):
                # if self.are_contingents[index]:
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

        # update new trial parameters
        # for event, event_params in new_trial.items():
        #     params_values = {param: self.trial_params_widgets[event][i].text() for i, param in
        #                      enumerate(event_params)}
        #     new_trial[event] = params_values
        # check if not an empty input

        # if not self.are_valid_values(new_trial):
        #     error_warning("An error accrued, please try again.")
        #     return
        # validate parameters values
        # self.are_valid_values(new_trial)
        # add new trial

        self.parent.trials_in_session.extend([new_trial, event_and_params])
        # print(self.parent.trials_in_session)

        # self.parent.percentages.append(0)
        # self.parent.percent_per_block.append([0] * len(self.parent.block_list))
        # add a percentage to each block
        # for i in range(len(self.parent.block_list)):
        #     self.parent.prcnt_per_block[i].append()
        # update trials table on the window
        self.parent.set_trials_table()
        # self.index+=1
        # print(self.index)
        # self.set_trials_table_pointer()
        self.parent.add_window.close()

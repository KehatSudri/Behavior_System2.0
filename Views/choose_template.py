from PyQt6 import QtCore, QtWidgets, uic
from collections import OrderedDict
from Views.utils import error_warning, get_ui_path
from Models.DB_INIT import DB
import numpy as np

class ChooseTemplateUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.choose_subject_id_cb = None
        self.filter_by_id_radio_btn = None
        self.all_radio_btn = None
        self.choose_template_cb = None
        self.subject_ids = self.parent.vm.get_list_of_subjects()[::-1]  # check this func
        self.current_all_templates = []
        self.templates = {}  # TODO get from parent cache
        self.subjects = set()  # TODO get from parent cache
        self.init()
    def init(self):
        self.db=DB()
        subjects=self.db.get_subjects()
        subjectsArray = [x[0] for x in subjects]
        for subject in subjectsArray:
            related_sessions=self.db.get_sessions_by_subject(subject)
            self.subjects.add(subject)
            self.templates[subject]=[subject +" "+ x[0] for x in related_sessions]

    def setup_ui(self, dialog, event_handler):
        self.all_templates = self.get_all_templates()
        uic.loadUi(get_ui_path('choose_template.ui'), dialog)
        dialog.accepted.connect(lambda: event_handler(self.choose_template_cb.currentText()))
        dialog.rejected.connect(lambda: print('cancel'))
        self.choose_template_cb = dialog.findChild(QtWidgets.QComboBox, 'choose_template_cb')
        self.choose_subject_id_cb = dialog.findChild(QtWidgets.QComboBox, 'choose_subject_id_cb')
        self.choose_subject_id_cb.setEnabled(False)
        self.choose_subject_id_cb.addItems(self.subjects)
        self.choose_subject_id_cb.currentTextChanged.connect(lambda: self.on_filter_by_id_change_event_handler())

        self.all_radio_btn = dialog.findChild(QtWidgets.QRadioButton, 'all_radio_btn')
        self.filter_by_id_radio_btn = dialog.findChild(QtWidgets.QRadioButton, 'filter_by_id_radio_btn')
        self.all_radio_btn.toggled.connect(lambda: self.on_radio_change_event_handler())
        self.all_radio_btn.toggle()

        return

    def subject_id_click(self, index):
        self.templates_comboBox.clear()
        self.templates_comboBox.addItems(
            self.parent.vm.get_template_list_by_subject(self.subject_id_comboBox.currentText()).values())

    def set_templates_display(self):
        self.all_radioButton.toggled.connect(lambda: self.templates_display(self.all_radioButton))
        self.filter_by_subject_id_radioButton.toggled \
            .connect(lambda: self.templates_display(self.filter_by_subject_id_radioButton))

    def templates_display(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "All":  # all subject ids case
                self.subject_id_comboBox.setEnabled(False)
                self.templates_comboBox.clear()
                self.is_filtered_by_subject = False
                self.templates_comboBox.addItems(self.parent.vm.get_template_list_by_date_exp_sess_names().values())
            if btn.text() == "Filter by subject id":  # filter by subject id case
                self.subject_id_comboBox.setEnabled(True)
                self.templates_comboBox.clear()
                self.templates_comboBox.addItems(
                    self.parent.vm.get_template_list_by_subject(self.subject_id_comboBox.currentText()).values())
                self.is_filtered_by_subject = True

    def set_template_data_in_parent(self, temp_id):
        sess_id, sess_name, exp_name, iti_type, iti_min, iti_max, iti_behave, end_def, end_val, order, total, \
            block_sizes, blocks_order, rew_prcnt, last_used = self.parent.vm.get_data_for_template_id(temp_id)
        if order != 'random':
            block_sizes = ([int(val) for val in block_sizes.replace("[", "").replace("]", "").split(",")])
        self.parent.vm.sessionVM.session_name = sess_name
        self.parent.vm.sessionVM.trials_order = order
        blocks_order = blocks_order.replace("\'", "").replace(" ", "").replace("[", "").replace("]", "").split(",")
        self.parent.session_name_lineEdit.setText(sess_name)
        self.parent.experimenter_name_lineEdit.setText(exp_name)
        self.parent.random_reward_percent_spinBox.setValue(rew_prcnt)
        # trials order
        index = self.parent.trials_order_comboBox.findText(order, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.parent.trials_order_comboBox.setCurrentIndex(index)
        # chosen iti type
        if iti_type == "random":
            self.parent.random_iti_radioBtn.setChecked(True)
            self.parent.min_iti_spinBox.setValue(iti_min)
            self.parent.max_iti_spinBox.setValue(iti_max)
        else:
            self.parent.chosen_behavior = iti_behave
            self.parent.behavior_iti_radioBtn.setChecked(True)
            index = self.parent.behaviors_comboBox.findText(iti_behave, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.parent.behaviors_comboBox.setCurrentIndex(index)
        # end definition
        index = self.parent.end_def_comboBox.findText(end_def, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.parent.end_def_comboBox.setCurrentIndex(index)
        self.parent.end_def_spinBox.setValue(end_val)
        # trials def
        trials_def = self.parent.vm.get_trials_def_for_sess(sess_id, order)
        self.set_trials_in_parent(order, trials_def, total, block_sizes, blocks_order)

    def set_subject_id_in_parent(self):
        if self.is_filtered_by_subject:
            # extract also subject id if relevant
            sub_id = self.subject_id_comboBox.currentText()
            self.parent.subject_id_lineEdit.setText(sub_id)
            self.parent.vm.curr_session.subject_id = sub_id
        else:
            self.parent.subject_id_lineEdit.setText("")
            self.parent.vm.curr_session.subject_id = ""

    def set_trials_in_parent(self, order, trials_def, total=None, block_sizes=None, blocks_order=None):
        self.parent.trials_in_session.clear()
        trials = []
        for trial in trials_def.trial_list:
            t = {}
            t[trial.name] = OrderedDict()  # TODO missing intervals
            for i in range(len(trial.events)):
                event = trial.events[i]
                # for event in trial.events:
                e = {}
                params = event.get_list_params()
                for param in params:
                    e[param] = getattr(event, param)
                if event.get_type_str() in t[trial.name]:
                    # get max rep
                    max_rep = 0
                    key_list = list(t[trial.name].keys())
                    for key in key_list:
                        split_key = key.split("#")
                        if split_key[0] == event.get_type_str():
                            if len(split_key) == 1:
                                max_rep = 1
                            else:
                                if split_key[1] > max_rep:
                                    max_rep = split_key[1]
                    t[trial.name][event.get_type_str() + "#" + str(max_rep + 1)] = e
                else:
                    t[trial.name][event.get_type_str()] = e  # this is the problem! same type goes to same place
                # put interval in list
                if len(trial.events) > 1 and i != len(trial.events) - 1:
                    intv_str = "interval"
                    if i > 0:
                        intv_str += ("#" + str(i + 1))
                    intv = trial.intervals[i]
                    t[trial.name][intv_str] = {'min': str(intv[0]), 'max': str(intv[1])}

            trials.append(t)
            # self.parent.trials_in_session = trials
            # TODO trials to parent
        for i in range(len(trials)):
            self.parent.trials_in_session.append(trials[i])
            self.parent.set_trials_table_pointer()

        if order == "random":
            # set random order fields to the given data
            self.parent.percentages = trials_def.percent_list
            self.parent.total_num = total
            # nullify block fields in case some was already put
            self.parent.blocks_ord.clear()
            self.parent.block_list.clear()
            self.parent.percent_per_block.clear()
            self.parent.block_sizes.clear()
            # create empty list of percentages for each existing trial to carry future changes
            for i in range(len(self.parent.percentages)):
                self.parent.percent_per_block.append([])

        else:
            # set blocks order fields to the given data
            self.parent.blocks_ord = blocks_order
            self.parent.block_list = trials_def.block_list
            self.parent.percent_per_block = trials_def.percent_per_block
            self.parent.block_sizes = block_sizes
            # nullify random order fields
            self.parent.percentages = [0] * len(self.parent.percent_per_block)
            self.parent.total_num = 0

    def accept(self):
        # TODO: update all relevant fields in parent
        chosen_temp_id = self.templates_comboBox.currentText()


        if chosen_temp_id == "":
            error_warning("There are no templates in the system.")
            # TODO check what should we do in this case
        chosen_temp_id = int(chosen_temp_id.split(":")[0])
        self.parent.vm.choose_template_from_list(chosen_temp_id)
        self.set_template_data_in_parent(chosen_temp_id)
        self.set_subject_id_in_parent()
        self.parent.choose_template_window.close()

    # we need this
    def get_all_templates(self):
        self.current_all_templates = [template for sublist in self.templates.values() for template in sublist]

    # we need this
    def on_radio_change_event_handler(self):
        if self.all_radio_btn.isChecked():
            self.choose_subject_id_cb.setEnabled(False)
            self.choose_template_cb.clear()
            self.choose_template_cb.addItems(self.current_all_templates)
        elif self.filter_by_id_radio_btn.isChecked():
            self.choose_subject_id_cb.setEnabled(True)
            self.choose_template_cb.clear()
            template_key = self.choose_subject_id_cb.currentText()
            self.choose_template_cb.addItems(self.templates[template_key])

    # we need this
    def on_filter_by_id_change_event_handler(self):
        self.choose_template_cb.clear()
        template_key = self.choose_subject_id_cb.currentText()
        self.choose_template_cb.addItems(self.templates[template_key])

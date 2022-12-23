from PyQt6 import QtCore, QtWidgets
from collections import OrderedDict

from Views.utils import error_warning


class ChooseTemplateUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.window_gridLayout = None
        self.central_gridLayout = None
        self.header_label = None
        self.all_radioButton = None
        self.filter_by_subject_id_radioButton = None
        self.subject_id_comboBox = None
        self.subject_ids = self.parent.vm.get_list_of_subjects()[::-1]
        self.choose_template_label = None
        self.templates_comboBox = None
        self.templates = []
        self.buttonBox = None
        self.is_filtered_by_subject = None

    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(434, 301)
        self.window_gridLayout = QtWidgets.QGridLayout(dialog)
        self.window_gridLayout.setObjectName("window_gridLayout")
        self.central_gridLayout = QtWidgets.QGridLayout()
        #self.central_gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        #self.central_gridLayout.setContentsMargins(20, -1, 20, -1)
        self.central_gridLayout.setObjectName("central_gridLayout")
        # set a header for the window
        self.header_label = QtWidgets.QLabel(dialog)
        #self.header_label.setStyleSheet("font: 22pt \"Gabriola\";")
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.central_gridLayout.addWidget(self.header_label, 0, 0, 1, 3)
        # set radio buttons to choose if display all templates or filter
        self.filter_by_subject_id_radioButton = QtWidgets.QRadioButton(dialog)
        #self.filter_by_subject_id_radioButton.setStyleSheet("font: 12pt \"Gabriola\";")
        self.filter_by_subject_id_radioButton.setObjectName("filter_by_subject_id_radioButton")
        self.central_gridLayout.addWidget(self.filter_by_subject_id_radioButton, 1, 1, 1, 1)
        self.subject_id_comboBox = QtWidgets.QComboBox(dialog)
        self.subject_id_comboBox.setObjectName("subject_id_comboBox")
        self.subject_id_comboBox.addItems(self.subject_ids)
        # self.subject_id_comboBox.setCurrentText("<choose subject id>")
        self.subject_id_comboBox.setEnabled(False)
        self.subject_id_comboBox.activated.connect(self.subject_id_click)
        self.central_gridLayout.addWidget(self.subject_id_comboBox, 1, 2, 1, 1)
        self.all_radioButton = QtWidgets.QRadioButton(dialog)
        #self.all_radioButton.setStyleSheet("font: 12pt \"Gabriola\";")
        self.all_radioButton.setObjectName("all_radioButton")
        self.central_gridLayout.addWidget(self.all_radioButton, 1, 0, 1, 1)
        # set a comboBox to hold all the subject ids available in db
        self.templates_comboBox = QtWidgets.QComboBox(dialog)
        self.templates_comboBox.setObjectName("templates_comboBox")
        self.templates_comboBox.addItems(self.templates)
        # self.combo_box.setCurrentText("templates")
        self.central_gridLayout.addWidget(self.templates_comboBox, 4, 1, 1, 2)
        # create a label to choose a template
        self.choose_template_label = QtWidgets.QLabel(dialog)
        #self.choose_template_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.choose_template_label.setObjectName("choose_template_label")
        self.central_gridLayout.addWidget(self.choose_template_label, 4, 0, 1, 1)
        #spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.central_gridLayout.addItem(spacer_item, 5, 1, 1, 2)
        # set a buttonBox to hold OK and Cancel buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        #self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        #self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.central_gridLayout.addWidget(self.buttonBox, 6, 1, 1, 2)
        #spacer_item1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.central_gridLayout.addItem(spacer_item1, 2, 1, 2, 1)
        # self.central_gridLayout.setColumnStretch(0, 1)
        # self.central_gridLayout.setColumnStretch(1, 1)
        self.central_gridLayout.setColumnStretch(2, 1)
        # self.central_gridLayout.setRowStretch(0, 2)
        self.central_gridLayout.setRowStretch(1, 1)
        # self.central_gridLayout.setRowStretch(2, 2)
        # self.central_gridLayout.setRowStretch(3, 2)
        # self.central_gridLayout.setRowStretch(4, 100)
        # self.central_gridLayout.setRowStretch(5, 2)
        self.window_gridLayout.addLayout(self.central_gridLayout, 0, 0, 1, 1)

        self.set_templates_display()

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dialog)

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
            self.parent.percentages = [0]*len(self.parent.percent_per_block)
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



    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Choose template"))
        self.header_label.setText(_translate("Dialog", "Using ready template"))
        self.choose_template_label.setText(_translate("Dialog", "Choose template:"))
        self.filter_by_subject_id_radioButton.setText(_translate("Dialog", "Filter by subject id"))
        self.all_radioButton.setText(_translate("Dialog", "All"))



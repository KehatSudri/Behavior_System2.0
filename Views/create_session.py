import subprocess
import threading

from datetime import datetime
from pathlib import Path
from PyQt6 import QtCore, QtWidgets, uic
from Models.DB_INIT import DB
from Views.add_trial import AddTrialUi
from Views.edit_session_template import EditSessionUi
from Views.choose_template import ChooseTemplateUi
from Views.edit_trial import EditTrialUi
from Views.utils import error_warning, get_ui_path
from Views.random_order import RandomOrderUi
from Views.notes import NotesUi


def run_subprocess(command):
    subprocess.run(command)


class CreateSessionUi(object):
    def __init__(self, parent):
        self.add_ui = None
        self.add_window = None
        self.trials_ord_dialog_ui = None
        self.trials_ord_dialog = None
        self.trials_order_cb = None
        self.exp_name_te = None
        self.subject_id_te = None
        self.session_name_te = None
        self.parent = parent
        self.vm = parent.vm
        self.main_window = None
        self.chosen_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.main_gridLayout = QtWidgets.QGridLayout()
        self.headline_label = None
        self.choose_template_horizontalLayout = QtWidgets.QHBoxLayout()
        self.choose_template_pushButton = None
        self.session_name_and_date_horizontalLayout = QtWidgets.QHBoxLayout()
        self.session_name_label = None
        self.session_name_lineEdit = None
        self.date_label = None
        self.date_value_label = None
        self.subject_and_experimenter_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.subject_id_label = None
        self.subject_id_lineEdit = None
        self.experimenter_name_label = None
        self.experimenter_name_lineEdit = None
        self.trials_gridLayout = QtWidgets.QGridLayout()
        self.trials_tableWidget = None
        self.trials_label = None
        self.def_trial_horizontalLayout = QtWidgets.QHBoxLayout()
        self.order_horizontalLayout = QtWidgets.QHBoxLayout()
        self.trials_order_label = None
        self.trials_order_comboBox = None
        self.buttons_to_set_trial_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_trial_pushButton = None
        self.edit_trial_pushButton = None
        self.remove_trial_pushButton = None
        self.iti_and_end_def_gridLayout = QtWidgets.QGridLayout()
        self.navigation_gridLayout = QtWidgets.QGridLayout()
        self.next_pushBtn = None
        self.back_pushBtn = None
        self.iti_min_max_values_gridLayout = QtWidgets.QGridLayout()
        self.max_iti_spinBox = None
        self.min_iti_spinBox = None
        self.min_iti_label = None
        self.max_iti_spinBox = None
        self.min_iti_spinBox = None
        self.max_iti_label = None
        self.behaviors_comboBox = None
        self.end_def_value_horizontalLayout = QtWidgets.QHBoxLayout()
        # self.end_by_label = None
        self.end_def_spinBox = None
        self.end_def_comboBox = None
        self.end_def_label = None
        self.iti_label = None
        self.iti_def_horizontalLayout = QtWidgets.QHBoxLayout()
        self.behavior_iti_radioBtn = None
        self.random_iti_radioBtn = None
        self.random_reward_percent_horizontalLayout = QtWidgets.QHBoxLayout()
        self.random_reward_percent_label = None
        self.random_reward_percent_spinBox = None
        self.chosen_behavior = None
        if len(self.vm.get_behaviors_list()) > 0:
            self.chosen_behavior = self.vm.get_behaviors_list()[0]
        self.chosen_end_def = None
        self.chosen_iti_type = None
        self.trials_ord_window = None
        self.db = DB()
        self.behavior_iti_widgets = None
        self.random_iti_widgets = None
        self.trials_table = None
        self.trial_types = self.vm.get_list_trials_names()
        self.trials_names = self.vm.get_trial_names()
        self.trials_in_session = []  # holds all the trials in the current session
        self.selected_trial = -1  # holds the trial that the user tap on the table
        self.set_trials_table_pointer = self.set_trials_table
        self.percentages = []
        self.total_num = 0
        self.blocks_ord = []
        self.block_list = []
        self.percent_per_block = []
        self.block_sizes = []
        self.vm.sessionVM.trials_order = "random"
        self.iti_behaviors = self.vm.get_behaviors_list()
        self.end_defs = self.vm.get_end_def_list()
        self.notes = ""

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('create_session.ui'), self.main_window)
        self.remove_trial_pushButton = self.main_window.findChild(QtWidgets.QPushButton, "remove_trial_pushButton")
        self.add_trial_pushButton = self.main_window.findChild(QtWidgets.QPushButton, "add_trial")
        self.edit_pushButton = self.main_window.findChild(QtWidgets.QPushButton, "edit_pushButton")
        self.notesBtn = self.main_window.findChild(QtWidgets.QPushButton, "notes_pushButton")
        self.notesBtn.clicked.connect(self.on_notes_click)
        self.session_name_te = self.main_window.findChild(QtWidgets.QTextEdit, "session_name_te")
        self.subject_id_te = self.main_window.findChild(QtWidgets.QTextEdit, "subject_id_te")
        self.exp_name_te = self.main_window.findChild(QtWidgets.QTextEdit, "exp_name_te")
        self.trials_table = self.main_window.findChild(QtWidgets.QTableWidget, "trials_tableWidget")
        self.date_value_label = self.main_window.findChild(QtWidgets.QLabel, "date_value_label")
        # self.trials#_order_cb = self.main_window.findChild(QtWidgets.QComboBox, 'trials_order_cb')
        choose_template_btn = self.main_window.findChild(QtWidgets.QPushButton, "choose_template_btn")
        next_btn = self.main_window.findChild(QtWidgets.QPushButton, "next_btn")
        choose_template_btn.clicked.connect(self.on_choose_template_click)
        # self.t#rials_order_cb.addItems(["random", "blocks"])
        next_btn.clicked.connect(lambda: self.on_next_click(0))
        self.add_trial_pushButton.clicked.connect(self.on_add_click)
        self.edit_pushButton.clicked.connect(self.on_edit_click)
        self.remove_trial_pushButton.clicked.connect(self.on_remove_click)
        # self.trials_gridLayout=self.main_window.findChild(QtWidgets.QGridLayout, "trials_gridLayout_3")
        back_btn = self.main_window.findChild(QtWidgets.QPushButton, "back_btn")
        back_btn.clicked.connect(self.on_back_click)
        self.date_value_label.setText((datetime.now()).strftime("%d/%m/%Y"))
        self.fixed_iti_radioBtn = main_window.findChild(QtWidgets.QRadioButton, 'behavior_iti_radioBtn_3')
        self.random_iti_radioBtn = main_window.findChild(QtWidgets.QRadioButton, 'random_iti_radioBtn_3')
        self.min_iti_label = self.main_window.findChild(QtWidgets.QLabel, "min_iti_label_3")
        self.min_iti_spinBox = self.main_window.findChild(QtWidgets.QDoubleSpinBox, "min_iti_spinBox")
        self.max_iti_label = self.main_window.findChild(QtWidgets.QLabel, "max_iti_label_3")
        self.max_iti_spinBox = self.main_window.findChild(QtWidgets.QDoubleSpinBox, "max_iti_spinBox")
        self.fixed_iti_radioBtn.toggled.connect(self.toggle_spinbox)
        self.fixed_iti_radioBtn.setChecked(True)
        self.edit_pushButton.setEnabled(False)
        self.max_trial_time = self.main_window.findChild(QtWidgets.QDoubleSpinBox, "doubleSpinBox")

    def on_choose_template_click(self):
        # TODO add on clicked event handler for component
        self.chosen_window = QtWidgets.QDialog()
        choose_template = ChooseTemplateUi(self)
        choose_template.setup_ui(self.chosen_window, self.on_template_change_event_handler)
        self.chosen_window.show()
        # self.second_window_ui = ChooseTemplateUi(self)
        # self.second_window_ui.setupUi(self.second_window)
        # self.second_window.show()

    def toggle_spinbox(self, checked):
        if checked:
            self.max_iti_spinBox.hide()
            self.min_iti_label.hide()
            self.max_iti_label.hide()
        else:
            self.max_iti_spinBox.show()
            self.min_iti_label.show()
            self.max_iti_label.show()

    def on_notes_click(self):
        self.chosen_window = QtWidgets.QMainWindow()
        self.chosen_window_ui = NotesUi(self)
        self.chosen_window_ui.setupUi(self.chosen_window)
        self.chosen_window.show()

    def on_add_click(self):
        self.add_window = QtWidgets.QDialog()
        self.add_ui = AddTrialUi(self)
        self.add_ui.setupUi(self.add_window)
        self.add_window.show()

    def on_edit_click(self):
        self.add_window = QtWidgets.QDialog()
        self.add_ui = EditSessionUi(self)
        self.add_ui.setupUi(self.add_window, self.session_name_te.toPlainText())
        self.add_window.show()

    def deal_with_trial(self, treatment):

        is_not_empty = len(self.trials_in_session) > 0
        is_row_selected = self.trials_table.currentRow() != -1
        # check if there are trials and a trial was selected
        if is_not_empty and is_row_selected or self.trials_table.rowCount() != 0:
            if treatment == 0:  # edit case
                self.edit_window = QtWidgets.QDialog()
                self.edit_ui = EditTrialUi(self)
                self.edit_ui.setupUi(self.edit_window)
                self.edit_window.show()
                # self.second_window_ui = EditTrialUi(self)
                # self.second_window_ui.setupUi(self.second_window)
                # self.second_window.show()
            else:  # remove case
                # get the chosen block's row and remove it
                index = self.trials_table.currentRow()  # ignore 0th which represents blocks parameters
                if not self.trials_in_session:
                    self.trials_table.removeRow(index)
                    self.trials_table.setCurrentCell(-1, self.trials_table.currentColumn())
                    return
                # print(self.trials_in_session)
                del self.trials_in_session[index]
                del self.trials_in_session[index]
                # print(self.trials_in_session)
                self.trials_table.removeRow(index)
                # set current row to be unselected
                self.trials_table.setCurrentCell(-1, self.trials_table.currentColumn())

                # chosen_row = self.trials_tableWidget.currentRow()
                # self.trials_tableWidget.removeRow(chosen_row)
                # if len(self.percentages) != 0:
                # del self.percentages[index]
                # else:
                # del self.percent_per_block[index]
                # del self.trials_in_session[self.trials_tableWidget.currentRow()]
                # self.trials_tableWidget.removeRow(self.trials_tableWidget.currentRow())
                # if len(self.percentages)!=0:
                #     del self.percentages[self.trials_tableWidget.currentRow()]
                # else:
                #     del self.prcnt_per_block[self.trials_tableWidget.currentRow()]
                # for i in range(len(self.block_list)):
                #     del self.prcnt_per_block[i][self.trials_tableWidget.currentRow()] #TODO CHACK THIS
        elif is_not_empty:
            error_warning("Trial is not selected.")
        else:
            error_warning("There are no trials in the current session.")

    # def on_edit_click(self):
    #     self.deal_with_trial(0)

    def on_remove_click(self):
        self.deal_with_trial(1)

    def on_row_selection_changed(self):
        # set row selection on default
        self.edit_trial_pushBtn.setEnabled(
            bool(self.trials_tableWidget.selectionModel().selectedRows())
        )
        self.remove_trial_pushBtn.setEnabled(
            bool(self.trials_tableWidget.selectionModel().selectedRows())
        )

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.trials_tableWidget.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def iti_cfg(self):
        self.behavior_iti_radioBtn.toggled.connect(lambda: self.iti_state(self.behavior_iti_radioBtn))
        self.random_iti_radioBtn.toggled.connect(lambda: self.iti_state(self.random_iti_radioBtn))

    def iti_state(self, btn):
        # check if one of the radio buttons was pressed
        # 1 represents behavior chosen
        # 2 represents random chosen
        if btn.isChecked():
            if btn.text() == "behavior":
                self.hide_show_iti_def(False, 1)
            if btn.text() == "random":
                self.hide_show_iti_def(False, 2)
            self.chosen_iti_type = btn.text()

    def hide_show_iti_def(self, to_hide: bool, flag: int):
        widgets = []
        other_widgets = []
        if flag == 0:
            widgets = self.behavior_iti_widgets + self.random_iti_widgets
        elif flag == 1:
            widgets = self.behavior_iti_widgets
            other_widgets = self.random_iti_widgets
        else:
            widgets = self.random_iti_widgets
            other_widgets = self.behavior_iti_widgets
        for w in widgets:
            if to_hide:
                w.hide()
            else:
                w.show()
        for w in other_widgets:
            if to_hide:
                w.show()
            else:
                w.hide()

    def on_next_click(self, flag):
        # print(self.trials_in_session)
        session_name = self.session_name_te.toPlainText()
        subject_id = self.subject_id_te.toPlainText()
        experimenter_name = self.exp_name_te.toPlainText()
        last_used = self.date_value_label.text()
        date_object = datetime.strptime(last_used, "%d/%m/%Y")
        formatted_date_last_used = date_object.strftime("%Y-%m-%d")
        is_fixed_iti = self.fixed_iti_radioBtn.isChecked()
        max_iti = self.max_iti_spinBox.value()
        min_iti = self.min_iti_spinBox.value()
        max_trial_time = self.max_trial_time.value()
        sessions_names = self.db.get_sessions_names()
        notes = self.notes
        if session_name in ([x[0] for x in sessions_names]):
            error_warning("Error: Session name already exists.")
            return
        if session_name == "":
            error_warning("Please enter Session name")
            return
        if subject_id == "":
            error_warning("Please enter subjectID")
            return
        if experimenter_name == "":
            error_warning("Please enter experimenter name")
            return
        if self.trials_table.rowCount() == 0:
            error_warning("Please add Trials")
            return
        if not self.fixed_iti_radioBtn.isChecked() and not self.random_iti_radioBtn.isChecked():
            error_warning("Please set ITI")
            return
        if self.max_trial_time.value() == 0:
            error_warning("Please fill max Trial duration")
            return

        if flag:  # only when flag=1 I want to insert information to DB
            try:
                self.vm.insert_session_to_DB(
                    session_name,
                    subject_id,
                    experimenter_name,
                    formatted_date_last_used,
                    min_iti,
                    max_iti,
                    is_fixed_iti,
                    max_trial_time,
                    notes)
            except Exception as e:
                msg = str(e)
                if "name" in msg:  # here I need to check if something was edit then to create new sesion on DB if no just continue
                    error_warning("Error: Session name already exists.")
                return

            # insert to session to trials table
            for i in range(0, len(self.trials_in_session), 2):
                self.vm.insert_session_to_trials(session_name, self.trials_in_session[i])
            return
        config_data = [session_name, self.trials_in_session, is_fixed_iti]
        self.trials_ord_dialog = QtWidgets.QDialog()
        self.trials_ord_dialog_ui = RandomOrderUi(self)
        self.trials_ord_dialog_ui.setupUi(self.trials_ord_dialog, self.on_session_define_event_handler, config_data,
                                          self.on_next_click)
        self.trials_ord_dialog.show()

    def set_trials_table(self):
        params = ""
        table = self.trials_table
        index = table.rowCount()
        table.insertRow(index)
        table.setItem(index, 0, QtWidgets.QTableWidgetItem(self.trials_in_session[index * 2]))
        for event, parameters in self.trials_in_session[index * 2 + 1].items():
            if self.db.is_random_event_in_a_given_trial(self.trials_in_session[index * 2], event)[0]:
                if event == 'Tone':
                    params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                        1] + ", duration - " + parameters[
                                  2] + ", frequency - " + parameters[3] + ", tone amplitude - " + parameters[4] + "\n"
                elif event == 'Reward':
                    params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                        1] + ", duration - " + parameters[2] + "\n"
                else:
                    params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                        1] + ", duration - " + parameters[
                                  2] + "\n"
            else:
                if event == 'Tone':
                    params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[
                        1] + ", frequency - " + parameters[2] + ", tone amplitude - " + parameters[3] + "\n"
                elif event == 'Reward':
                    params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[1] + "\n"
                else:
                    params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[
                        1] + "\n"

            table.setItem(index, 1, QtWidgets.QTableWidgetItem(params))
            self.db = DB()
            trial_name = self.trials_in_session[index * 2]
            self.db.insert_params(trial_name, event, str(','.join(parameters)))

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def parse_trial_params(self, trials):
        trials_names, trials_params = [], []
        for trial in trials:
            pair = [(keys, val) for keys, val in trial.items()]
            name = [i[0] for i in pair]
            param = [i[1] for i in pair]
            trials_names += name
            trials_params.append(param)
        return trials_names, trials_params

    # we need this
    def on_template_change_event_handler(self, template):
        subject, session_name = template.split()
        self.trials_in_session = []
        trials_dict = {}
        template_info = self.db.get_template(session_name, subject)
        var1, session_name, subject, exp_name, date, min_iti, max_iti, is_fixed_iti_type, max_trial_time, notes = \
            template_info[0]
        self.session_name_te.setText(session_name)
        self.subject_id_te.setText(subject)
        self.exp_name_te.setText(exp_name)
        self.min_iti_spinBox.setValue(min_iti)
        self.max_iti_spinBox.setValue(max_iti)
        self.trials_table.clear()
        self.trials_table.setRowCount(0)
        self.max_trial_time.setValue(max_trial_time)
        self.notes = notes
        trials = self.db.get_trial_name_by_session(session_name)
        trials_ = [x[0] for x in trials]
        col1 = QtWidgets.QTableWidgetItem("Trial name")
        col2 = QtWidgets.QTableWidgetItem("parameters")
        self.trials_table.setHorizontalHeaderItem(0, col1)
        self.trials_table.setHorizontalHeaderItem(1, col2)
        for trial in trials_:
            table = self.trials_table
            index = table.rowCount()
            table.insertRow(index)
            table.setItem(index, 0, QtWidgets.QTableWidgetItem(trial))
            events = self.db.get_events_by_trial_name(trial)
            events = [x[0] for x in events]
            params = ""
            for event in events:
                parameters = self.db.get_params_by_event_and_trial_name(event, trial)
                parameters = [x[0] for x in parameters]
                parameters_ar = [item.split(',') for item in parameters]
                trials_dict[event] = parameters[0].split(',')
                for parameters in parameters_ar:
                    if self.db.is_random_event_in_a_given_trial(trial, event)[0]:
                        if event == 'Tone':
                            params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                                1] + ", duration - " + parameters[
                                          2] + ", frequency - " + parameters[3] + ", tone amplitude - " + parameters[
                                          4] + "\n"
                        elif event == 'Reward':
                            params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                                1] + ", duration - " + parameters[2] + "\n"
                        else:
                            params += event + ":" + " min delay - " + parameters[0] + ", max delay - " + parameters[
                                1] + ", duration - " + parameters[
                                          2] + "\n"
                    else:
                        if event == 'Tone':
                            params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[
                                1] + ", frequency - " + parameters[2] + ", tone amplitude - " + parameters[3] + "\n"
                        elif event == 'Reward':
                            params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[1] + "\n"
                        else:
                            params += event + ":" + " delay - " + parameters[0] + ", duration - " + parameters[
                                1] + "\n"
            table.setItem(index, 1, QtWidgets.QTableWidgetItem(params))
            self.trials_in_session.append(trial)
            self.trials_in_session.append(trials_dict)
        self.edit_pushButton.setEnabled(True)
        self.add_trial_pushButton.setEnabled(False)
        self.remove_trial_pushButton.setEnabled(False)
        if is_fixed_iti_type:
            self.fixed_iti_radioBtn.setChecked(True)
            self.random_iti_radioBtn.setChecked(False)
        else:
            self.fixed_iti_radioBtn.setChecked(False)
            self.random_iti_radioBtn.setChecked(True)
        # self.trials_in_session.append(session_name)
        # self.trials_in_session.append(trials_dict)
        print(self.trials_in_session)

    def on_session_define_event_handler(self):
        config_path = str(Path(__file__).parent.parent / 'config_files' / 'session_config.txt')
        bs_runner_path = r"BS_Runner/Debug/BS_Runner.exe"
        command = [bs_runner_path, config_path, self.session_name_te.toPlainText()]
        subprocess_thread = threading.Thread(target=run_subprocess, args=(command,))
        subprocess_thread.start()

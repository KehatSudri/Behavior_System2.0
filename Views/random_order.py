import threading

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView
from Models.prepare_session_information import prepare_session_information
from Views.control_session_board import ControlSessionBoardUi
from Models import Trial_Model
from Views.utils import error_warning, dict_one_line_style, get_ui_path


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class RandomOrderUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.window_gridLayout = None
        self.main_window_gridLayout = QtWidgets.QGridLayout()
        self.explanation_label = None
        self.total_num_of_trials_label = None
        self.total_num_of_trials_spinBox = None
        self.trials_tableWidget = None
        self.buttonBox = None
        self.percentages = []
        self.num_of_rows = len(self.parent.trials_in_session)
        self.set_trials_table_pointer = None


    def setupUi(self, dialog, event_handler,config_data,onNextClick):
        self.on_next_click = onNextClick
        self.event_handler=event_handler
        self.config_info=config_data
        uic.loadUi(get_ui_path('random_order.ui'), dialog)
        # dialog.accepted.connect(lambda: event_handler(self.choose_template_cb.currentText()))
        dialog.accepted.connect(self.accept)
        # dialog.rejected.connect()
        self.trials_tableWidget = dialog.findChild(QtWidgets.QTableWidget, "trials_tableWidget")
        self.isRandomOrder = dialog.findChild(QtWidgets.QCheckBox, 'checkBox')
        for i in range (int(len(self.parent.trials_in_session)/2))   :
            self.trials_tableWidget.insertRow(i)
            self.trials_tableWidget.setItem(i, 0, QTableWidgetItem(self.parent.trials_in_session[i*2]))
            self.trials_tableWidget.setItem(i, 1, QTableWidgetItem("1"))

        return

    def get_total_num_of_trials(self):
        total_num_of_trials = self.total_num_of_trials_spinBox.value()
        self.parent.total_num = total_num_of_trials
        return total_num_of_trials

    def set_trials_table(self):
        self.trials_tableWidget.setRowCount(self.num_of_rows)
        # if len(self.parent.percentages) == 0:
        #     for i in range(self.num_of_rows):
        #         self.percentages.append(0)
        #         #self.parent.percentages.append(0)
        # else:
        #     for i in range(self.num_of_rows):
        #         self.percentages.append(self.parent.percentages[i])
                #self.parent.percentages.append(0)
        for i in range(self.num_of_rows):
            trial_name = [*self.parent.trials_in_session[i].keys()][0]
            # set first column with trial names
            self.trials_tableWidget.setItem(i, 0, QTableWidgetItem(trial_name))
            # set second column with trial parameters
            self.trials_tableWidget.setItem(i, 1,
                                            QTableWidgetItem(
                                                dict_one_line_style(self.parent.trials_in_session[i][trial_name])))
            # set third column with trial percentages
            #self.trials_tableWidget.setItem(num_trials - 1, 2, QTableWidgetItem(str(self.percentages[num_trials-1])))
            self.trials_tableWidget.setItem(i, 2, QTableWidgetItem(str(self.parent.percentages[i])))
            #self.trials_tableWidget.setItem(i, 2, QTableWidgetItem(str(self.percentages[i])))
        # Set an adaptive width for table
        trials_table_adaptive_width = self.trials_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)

    def read_table_data(self):
        # read all the given percentages for each trial
        for i in range(self.trials_tableWidget.rowCount()):
            # no percentage was given
            if self.trials_tableWidget.item(i, 2) is None:
                error_warning("An error accrued, please try again.")
                return False
            current_value = self.trials_tableWidget.item(i, 2).text()
            # check if the given value is a number
            if current_value.isnumeric():
                #self.percentages[i] = int(current_value)
                self.parent.percentages[i] = int(current_value)
            else:
                error_warning("An error accrued, please try again.")
                return False
        # check if the percentages sum to 100
        #sum_percentages = sum(self.percentages)
        #sum_percentages = sum(self.percentages)
        sum_percentages = sum(self.parent.percentages)
        if sum_percentages != 100:
            error_warning("An error accrued, please try again.")
            return False
        return True


    def accept(self):
        self.on_next_click(1)
        session_name = self.config_info[0]
        # ports = self.config_info[1]
        # dependencies = self.config_info[2]
        # trials_in_session_specific = self.config_info[1]
        # j = self.config_info[2]
        trials_in_session = self.config_info[1]
        is_fixed_iti = self.config_info[2]
        isRandomOrder=self.isRandomOrder.isChecked()
        repeats = []
        for row in range(self.trials_tableWidget.rowCount()):
            item = self.trials_tableWidget.item(row, 1)
            if item is not None:
                repeats.append(item.text())
        if not repeats:
            error_warning("Number of repetition should be at least 1")
            return
        for i in range(0, len(trials_in_session), 2):
            ports = (self.vm.get_ports(trials_in_session[i]))
            dependencies = self.vm.get_dependencies(trials_in_session[i])
            prepare_session_information(session_name,ports,dependencies,trials_in_session[i],i,trials_in_session,is_fixed_iti,repeats,isRandomOrder)
        self.event_handler()
        # # check if a number was selected for total number of trials
        # if self.get_total_num_of_trials() is None:
        #     error_warning("An error accrued, please try again.")
        #     return
        # else:
        #     # read the percentages that were given
        #     if not self.read_table_data():
        #         return
        #     self.read_table_data()
        #     # set percentage list and total num to model
        #     trials = self.parent.vm.create_trial_list(self.parent.trials_in_session)
        #     self.parent.vm.curr_session.trials_def = Trial_Model.Trials_def_rand(trials, self.parent.percentages, self.parent.total_num)
        #
        #     # open a new session
        #     self.session_window = QtWidgets.QDialog()
        #     self.session_ui = ControlSessionBoardUi(self)
        #     self.session_ui.setupUi(self.session_window)
        #     self.session_window.show()
        #     # close current window
        #     self.parent.trials_ord_window.close()
        #     threading.Thread(target=self.parent.vm.start_Session).start()
        #     #self.parent.vm.start_Session()
        #     self.parent.main_window.close()

    def reject(self):
        print("reject")
        self.parent.trials_ord_window.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Random = QtWidgets.QDialog()
    ui = RandomOrderUi()
    ui.setupUi(Random)
    Random.show()
    sys.exit(app.exec_())

import threading

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView

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

    def setupUi(self, dialog, event_handler):
        print(self.parent.trials_in_session)
        uic.loadUi(get_ui_path('random_order.ui'), dialog)
        # dialog.accepted.connect(lambda: event_handler(self.choose_template_cb.currentText()))
        dialog.accepted.connect(lambda: event_handler())
        dialog.rejected.connect(lambda: print('cancel'))
        trials_tableWidget = dialog.findChild(QtWidgets.QTableWidget, "trials_tableWidget")
        print(len(self.parent.trials_in_session))
        for i in range (int(len(self.parent.trials_in_session)/2))   :
            trials_tableWidget.insertRow(i)
            trials_tableWidget.setItem(i, 0, QTableWidgetItem(self.parent.trials_in_session[i*2]))
        return
        dialog.setObjectName("dialog")
        dialog.resize(401, 355)
        self.window_gridLayout = QtWidgets.QGridLayout(dialog)
        self.window_gridLayout.setObjectName("window_gridLayout")
        self.main_window_gridLayout.setObjectName("main_window_gridLayout")
        # an explanation about the window's purpose
        self.explanation_label = QtWidgets.QLabel(dialog)
        self.explanation_label.setStyleSheet("font: 25pt \"Arial\";")
        self.explanation_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.explanation_label.setObjectName("explanation_label")
        self.main_window_gridLayout.addWidget(self.explanation_label, 0, 0, 1, 2)
        # label for choosing number of trials
        self.total_num_of_trials_label = QtWidgets.QLabel(dialog)
        self.total_num_of_trials_label.setStyleSheet("font: 12pt \"Arial\";")
        self.total_num_of_trials_label.setObjectName("total_num_of_trials_label")
        self.main_window_gridLayout.addWidget(self.total_num_of_trials_label, 1, 0, 1, 1)
        # add a spinbox button to choose number of trials
        self.total_num_of_trials_spinBox = QtWidgets.QSpinBox(dialog)
        self.total_num_of_trials_spinBox.setObjectName("total_num_of_trials_spinBox")
        self.total_num_of_trials_spinBox.setMaximum(100000)
        self.total_num_of_trials_spinBox.setValue(self.parent.total_num)
        self.total_num_of_trials_spinBox.valueChanged.connect(self.get_total_num_of_trials)
        self.main_window_gridLayout.addWidget(self.total_num_of_trials_spinBox, 1, 1, 1, 1)
        # a table to hold all tha trials and their percentage in the session
        self.trials_tableWidget = QtWidgets.QTableWidget(dialog)
        self.trials_tableWidget.setStyleSheet("font: 12pt \"Arial\";")
        self.trials_tableWidget.setObjectName("trials_tableWidget")
        self.trials_tableWidget.setColumnCount(3)
        self.trials_tableWidget.setRowCount(0)
        self.trials_tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.trials_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        delegate = ReadOnlyDelegate(self.trials_tableWidget)
        # set the first two rows to be read-only
        self.trials_tableWidget.setItemDelegateForColumn(0, delegate)
        self.trials_tableWidget.setItemDelegateForColumn(1, delegate)
        # set 3 columns
        item = QtWidgets.QTableWidgetItem()
        self.trials_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trials_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.trials_tableWidget.setHorizontalHeaderItem(2, item)
        self.main_window_gridLayout.addWidget(self.trials_tableWidget, 2, 0, 1, 2)
        # Set an adaptive width for table
        trials_table_adaptive_width = self.trials_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        # a vertical spacer
        spacer_item = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_window_gridLayout.addItem(spacer_item, 3, 0, 1, 1)
        # ok and back buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.main_window_gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.main_window_gridLayout.setColumnStretch(0, 1)
        self.main_window_gridLayout.setColumnStretch(1, 1)
        self.main_window_gridLayout.setRowStretch(0, 1)
        self.window_gridLayout.addLayout(self.main_window_gridLayout, 0, 0, 1, 1)

        self.set_trials_table()

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

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
        print("accept")
        # check if a number was selected for total number of trials
        if self.get_total_num_of_trials() is None:
            error_warning("An error accrued, please try again.")
            return
        else:
            # read the percentages that were given
            if not self.read_table_data():
                return
            self.read_table_data()
            # set percentage list and total num to model
            trials = self.parent.vm.create_trial_list(self.parent.trials_in_session)
            self.parent.vm.curr_session.trials_def = Trial_Model.Trials_def_rand(trials, self.parent.percentages, self.parent.total_num)

            # open a new session
            self.session_window = QtWidgets.QDialog()
            self.session_ui = ControlSessionBoardUi(self)
            self.session_ui.setupUi(self.session_window)
            self.session_window.show()
            # close current window
            self.parent.trials_ord_window.close()
            threading.Thread(target=self.parent.vm.start_Session).start()
            #self.parent.vm.start_Session()
            self.parent.main_window.close()

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

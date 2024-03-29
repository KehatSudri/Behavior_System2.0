from pathlib import Path
from Models.DB_INIT import DB
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem
from Models.prepare_session_information import prepare_session_information
from Views.utils import error_warning, dict_one_line_style, get_ui_path, get_base_path, get_file_path_from_configs


class RandomOrderUi(object):
    def __init__(self, parent):
        self.on_next_click = None
        self.event_handler = None
        self.config_info = None
        self.isRandomOrder = None
        self.parent = parent
        self.vm = self.parent.vm
        self.window_gridLayout = None
        self.main_window_gridLayout = QtWidgets.QGridLayout()
        self.total_num_of_trials_label = None
        self.total_num_of_trials_spinBox = None
        self.trials_tableWidget = None
        self.buttonBox = None
        self.percentages = []
        self.num_of_rows = len(self.parent.trials_in_session)
        self.set_trials_table_pointer = None

    def setupUi(self, dialog, event_handler, config_data, onNextClick):
        self.on_next_click = onNextClick
        self.event_handler = event_handler
        self.config_info = config_data
        uic.loadUi(get_ui_path('random_order.ui'), dialog)
        dialog.accepted.connect(self.accept)
        self.trials_tableWidget = dialog.findChild(QtWidgets.QTableWidget, "trials_tableWidget")
        self.isRandomOrder = dialog.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.isRandomOrder.stateChanged.connect(self.checkbox_state_changed)
        self.isRandomOrder.setChecked(True)
        for i in range(int(len(self.parent.trials_in_session) / 2)):
            self.trials_tableWidget.insertRow(i)
            self.trials_tableWidget.setItem(i, 0, QTableWidgetItem(self.parent.trials_in_session[i * 2]))
            self.trials_tableWidget.setItem(i, 1, QTableWidgetItem("1"))
            self.trials_tableWidget.setItem(i, 2, QTableWidgetItem("0"))
            self.trials_tableWidget.setItem(i, 3, QTableWidgetItem("0"))
        return

    def checkbox_state_changed(self):
        if not self.isRandomOrder.isChecked():
            self.trials_tableWidget.removeColumn(self.trials_tableWidget.columnCount() - 1)
        else:
            self.trials_tableWidget.setColumnCount(self.trials_tableWidget.columnCount() + 1)
            column_index = self.trials_tableWidget.columnCount() - 1
            header_item = QTableWidgetItem("Percent")
            self.trials_tableWidget.setHorizontalHeaderItem(column_index, header_item)
            for i in range(int(len(self.parent.trials_in_session) / 2)):
                self.trials_tableWidget.setItem(i, 3, QTableWidgetItem("0"))

    def get_total_num_of_trials(self):
        total_num_of_trials = self.total_num_of_trials_spinBox.value()
        self.parent.total_num = total_num_of_trials
        return total_num_of_trials

    def set_trials_table(self):
        self.trials_tableWidget.setRowCount(self.num_of_rows)
        for i in range(self.num_of_rows):
            trial_name = [*self.parent.trials_in_session[i].keys()][0]
            self.trials_tableWidget.setItem(i, 0, QTableWidgetItem(trial_name))
            self.trials_tableWidget.setItem(i, 1,
                                            QTableWidgetItem(
                                                dict_one_line_style(self.parent.trials_in_session[i][trial_name])))
            self.trials_tableWidget.setItem(i, 2, QTableWidgetItem(str(self.parent.percentages[i])))
        # Set an adaptive width for table
        trials_table_adaptive_width = self.trials_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)

    def is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def accept(self):
        for row in range(self.trials_tableWidget.rowCount()):
            if not self.trials_tableWidget.item(row, 1).text().isnumeric() and not self.is_float(
                    self.trials_tableWidget.item(row, 1).text()):
                error_warning("Please enter only numbers")
                return
            if not self.trials_tableWidget.item(row, 2).text().isnumeric() and not self.is_float(
                    self.trials_tableWidget.item(row, 2).text()):
                error_warning("Please enter only numbers")
                return
            if self.trials_tableWidget.item(row, 3) and (
                    not self.trials_tableWidget.item(row, 3).text().isnumeric() and not self.is_float(
                    self.trials_tableWidget.item(row, 3).text())):
                error_warning("Please enter only numbers")
                return
        self.on_next_click(1)

        session_name = self.config_info[0]
        trials_in_session = self.config_info[1]
        is_fixed_iti = self.config_info[2]
        isRandomOrder = self.isRandomOrder.isChecked()
        repeats = []
        MaxTime = []
        Percent = []
        for row in range(self.trials_tableWidget.rowCount()):
            item = self.trials_tableWidget.item(row, 1)
            item2 = self.trials_tableWidget.item(row, 2)
            if isRandomOrder:
                item3 = self.trials_tableWidget.item(row, 3)
            if item is not None:
                repeats.append(item.text())
                MaxTime.append(item2.text())
                if isRandomOrder:
                    Percent.append(item3.text())
        if not repeats:
            error_warning("Number of repetition should be at least 1")
            return
        configs_path = get_file_path_from_configs('session_config.txt')

        with open(configs_path, "a") as file:
            db = DB()
            max_session_time = db.get_max_trial_time(self.parent.current_id)
            file.write(str(max_session_time[0]) + "\n")
            iti_vals = db.get_iti_vals(self.parent.current_id)
            if is_fixed_iti:
                file.write(str(iti_vals[0]) + ",")
            else:
                file.write(str(iti_vals[0]) + ";" + str(iti_vals[1]) + ",")
            file.write(str(isRandomOrder) + "\n")

        for i in range(0, len(trials_in_session), 2):
            ports = (self.vm.get_ports(trials_in_session[i]))
            dependencies = self.vm.get_dependencies(trials_in_session[i])
            prepare_session_information(ports, dependencies, trials_in_session[i], i, trials_in_session
                                        , repeats, isRandomOrder, MaxTime, Percent)
        self.event_handler()

    def reject(self):
        self.parent.trials_ord_window.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Random = QtWidgets.QDialog()
    ui = RandomOrderUi()
    ui.setupUi(Random)
    Random.show()
    sys.exit(app.exec_())

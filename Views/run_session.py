import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel, QHeaderView, QTableWidgetItem
import random
import matplotlib
from collections import OrderedDict

from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.utils import dict_one_line_style, get_string_dict

matplotlib.use('Qt5Agg')

import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class RunningGraphsUi(object):

    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.vm.sessionVM.property_changed += self.EventHandler
        self.vm.property_changed += self.EventHandler
        self.trials_names, self.trials_params = self.parent.parent.parent.parse_trial_params(
            self.parent.parent.parent.trials_in_session)

        self.num_of_samples = 100

        self.total_counter = np.zeros(len(self.trials_names))
        self.successive_counter = np.zeros(len(self.trials_names))
        # self.parent.parent.parent.vm.sessionVM.property_changed += self.EventHandler
        self.counter = 0
        self.graphs_labels = []
        self.graphs_widgets = []

        self.window_gridLayout = None
        self.main_verticalLayout = QtWidgets.QVBoxLayout()
        # self.total_counter_label = None
        # self.success_rate_label = None
        self.counters_tableWidget = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = None
        self.formLayout = QtWidgets.QFormLayout()

        self.counters_timer = QTimer()
        self.graphs_timer = QtCore.QTimer()
        self.end_session = False


        self.graphs = OrderedDict()
        self.init_graphs()
        self.counters = None
        self.graphics_view = []

        self.x = list(range(100))  # 100 time points

        self.data_window = QtWidgets.QDialog()
        self.data_ui = None

    def setupUi(self, dialog):
        self.init()
        dialog.setObjectName("dialog")
        dialog.resize(500, 600)
        self.window_gridLayout = QtWidgets.QGridLayout(dialog)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # self.main_verticalLayout = QtWidgets.QVBoxLayout()
        self.main_verticalLayout.setObjectName("main_verticalLayout")
        # Set counters: total and success rate
        # self.total_counter_label = QtWidgets.QLabel(dialog)
        # self.total_counter_label.setStyleSheet("font: 12pt \"Gabriola\";")
        # self.total_counter_label.setObjectName("label")
        # self.main_verticalLayout.addWidget(self.total_counter_label)
        # self.success_rate_label = QtWidgets.QLabel(dialog)
        # self.success_rate_label.setStyleSheet("font: 12pt \"Gabriola\";")
        # self.success_rate_label.setObjectName("label_2")
        # self.main_verticalLayout.addWidget(self.success_rate_label)
        # set table for counters
        label = QLabel("Counters:")
        label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.main_verticalLayout.addWidget(label)  # add a label for the counters
        self.counters_tableWidget = QtWidgets.QTableWidget(dialog)
        self.counters_tableWidget.setObjectName("counters_tableWidget")
        self.counters_tableWidget.setColumnCount(0)
        self.counters_tableWidget.setRowCount(0)
        self.main_verticalLayout.addWidget(self.counters_tableWidget)
        # add a scroll area to preset the graphs
        self.scrollArea = QtWidgets.QScrollArea(dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 305))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        # self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.main_verticalLayout.addWidget(self.scrollArea)
        self.main_verticalLayout.setStretch(2, 3)
        self.main_verticalLayout.setStretch(3, 10)
        self.window_gridLayout.addLayout(self.main_verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        self.counters = self.create_trial_list_counters()
        self.update_counters()

        self.set_form(self.graphs)

        # self.timer = QTimer()
        self.counters_timer.setInterval(500)
        self.counters_timer.timeout.connect(self.update_counters)
        self.counters_timer.start()

        # self.graphs_timer = QtCore.QTimer()
        self.graphs_timer.setInterval(40)
        self.graphs_timer.timeout.connect(self.update_plot_data)
        self.graphs_timer.start()

        self.vm.sessionVM.property_changed += self.EventHandler
        self.parent.parent.parent.vm.sessionVM.property_changed += self.EventHandler

    def init_graphs(self):
        self.events_for_sess = self.vm.get_event_list_for_sess()
        for e in self.events_for_sess:

            self.graphs[e] = [0 for _ in range(self.num_of_samples)]


    def init(self):
        # self.vertical_layout = None
        # self.scroll_area = None
        # self.scroll_area_widget_contents = QtWidgets.QWidget()
        # self.scroll_area_vertical_layout = None
        # self.form_layout = QtWidgets.QFormLayout()
        # self.trial_params_labels = []
        range_it = 100
        # self.graphs = {"Licking": [0]*100,
        #                "Speed": [random.randint(0, 10) for _ in range(20)],
        #                "d": [random.randint(0, 10) for _ in range(50)],
        #                "e": [random.randint(0, 10) for _ in range(50)],
        #                "t": [random.randint(0, 10) for _ in range(50)],
        #                "y": [random.randint(0, 10) for _ in range(range_it)],
        #                "u": [random.randint(0, 10) for _ in range(range_it)],
        #                "i": [random.randint(0, 10) for _ in range(50)],
        #                "o": [random.randint(0, 10) for _ in range(50)],
        #                "p": [random.randint(0, 10) for _ in range(50)]}
        self.counters = {"Trial X": ["0", "0"], "Trial Y": ["0", "0"]}
        self.trials_in_sess = self.parent.parent.parent.trials_in_session
        self.trial_params_labels = []
        # self.graphs = {"Licking": [random.randint(0, 1) for i in range(50)],
        #                "Speed": [random.randint(0, 10) for i in range(50)],
        #                "d": [random.randint(0, 10) for i in range(50)],
        #                "e": [random.randint(0, 10) for i in range(50)],
        #                "t": [random.randint(0, 10) for i in range(50)],
        #                "y": [random.randint(0, 10) for i in range(50)],
        #                "u": [random.randint(0, 10) for i in range(50)],
        #                "i": [random.randint(0, 10) for i in range(50)],
        #                "o": [random.randint(0, 10) for i in range(50)],
        #                "p": [random.randint(0, 10) for i in range(50)]}
        # self.counters = {"Trial X": ["0", "0"], "Trial Y": ["0", "0"]}
        self.counters_tableWidget = QtWidgets.QTableWidget()
        self.counters_tableWidget.setObjectName("counters_tableWidget")
        # self.counters = self.create_trial_list_counters()
        # self.counters = None
        # self.gridLayout = QtWidgets.QGridLayout(Dialog)
        # self.gridLayout.setObjectName("gridLayout")
        self.main_verticalLayout = QtWidgets.QVBoxLayout()
        self.main_verticalLayout.setObjectName("main_verticalLayout")

    def set_trials_list(self):
        self.counters = self.create_trial_list_counters()

    def create_trial_list_counters(self):
        start_list = [0] * 2
        counters = {}
        for i in range(len(self.trials_names)):
            counters[self.trials_names[i]] = start_list
            # self.blocks_tableWidget.setVerticalHeaderItem(i + 1, QTableWidgetItem(self.trials_names[i]))
            # set the matching parameters for trials
            # self.counters_tableWidget.setItem(0, i,
            #                                     QTableWidgetItem(str(self.trials_params[i])))
        return counters


    def update_counters(self):
        # if self.end_session:
        #     return
        for i in range(len(self.total_counter)):
            self.counters_tableWidget.setItem(1, i, QTableWidgetItem(str(int(self.total_counter[i]))))
            self.counters_tableWidget.setItem(2, i, QTableWidgetItem(str(int(self.successive_counter[i]))))
            # self.counters_tableWidget.setItem(1, QTableWidgetItem(str(int(self.total_counter))))
            # self.counters_tableWidget.setItem(2, QTableWidgetItem(str(int(self.successive_counter))))
        # self.clear_form()
        # self.init()
        # self.set_form(self.graphs)
        # (1, 1, QTableWidgetItem(str(self.counter)))
        # for i in range(len(self.graphs_widgets)):
        #     if i == 0:
        #         self.graphs_widgets[i].setData(random.randint(0, 1))
        #     else:
        #         self.graphs_widgets[i].setData(random.randint(0, 10))

    def update_input_plot_data(self, number_of_inputs):

        i = 0
        if len(self.vm.curr_session.data.T) < 10:
            return

        data = self.vm.curr_session.data[:, -10]
        for label, graph in self.graphs.items():
            if i < number_of_inputs:
                val = data[i]
                # if i == 0:
                #     val = random.randint(0, 1)
                # else:
                #     val = random.randint(0, 10)
                self.x = self.x[1:]  # Remove the first y element.
                self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

                graph1 = graph[1:]  # Remove the first
                graph1.append(val)  # Add a new random value.

                self.graphs[label] = graph1
                self.graphs_widgets[i].setData(graph1)  # Update the data.
                i += 1
            else:
                break

    def update_output_plot_data(self, number_of_inputs):
        data = self.vm.curr_session.output_vals
        data_binary = []
        for i in range(len(data)):
            if data[i]:
                data_binary.append(1)
            else:
                data_binary.append(0)
        i = 0
        for label, graph in self.graphs.items():
            if i < number_of_inputs:
                i += 1
                continue
            val = data_binary[i - number_of_inputs]
            # if i == 0:
            #     val = random.randint(0, 1)
            # else:
            #     val = random.randint(0, 10)
            self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

            graph1 = graph[1:]  # Remove the first
            graph1.append(val)  # Add a new random value.

            self.graphs[label] = graph1
            self.graphs_widgets[i].setData(graph1)  # Update the data.
            i += 1

    def update_plot_data(self):
        if self.end_session:
            return
        number_of_inputs = len(self.vm.input_events_names)
        self.update_input_plot_data(number_of_inputs)
        self.update_output_plot_data(number_of_inputs)
        # i = 0
        # data = self.vm.curr_session.data[:,-10]
        # for label, graph in self.graphs.items():
        #     val = data[i]
        #     if i == 0:
        #         val = random.randint(0, 1)
        #     else:
        #         val = random.randint(0, 10)
        #     self.x = self.x[1:]  # Remove the first y element.
        #     self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        #
        #     graph1 = graph[1:]  # Remove the first
        #     graph1.append(val)  # Add a new random value.
        #
        #     self.graphs[label] = graph1
        #     self.graphs_widgets[i].setData(graph1)  # Update the data.
        #     i += 1

    def set_form(self, graphs: dict):
        # add row for each graph accordingly
        for graph_name, values in graphs.items():
            # add a label for the graph
            label = QLabel(graph_name + ":")
            label.setStyleSheet("font: 12pt \"Gabriola\";")
            self.graphs_labels.append(label)
            # self.trial_params_labels.append(label)
            self.formLayout.addRow(label)

            self.set_graph(values)
        # add table of counters
        self.set_counters()
        # self.formLayout.addRow(self.counters_tableWidget)

    def delete_graphs(self):
        row = 0
        for i in range(len(self.graphs_labels)):
            label = self.graphs_labels.pop()
            self.formLayout.removeRow(label)
            graph = self.graphs_widgets.pop()
            self.formLayout.removeRow(graph)
            row += 2
        # init the lists tha holds the widgets for each row
        self.graphs_labels = []
        self.graphs_widgets = []

    def clear_form(self):
        if len(self.graphs_labels) != 0:
            self.delete_graphs()

    def set_graph(self, values):
        graphs_frame = QtWidgets.QFrame()
        graphs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        graphs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        graphs_frame.setObjectName("graphs_frame")
        graphics_view = pg.PlotWidget(graphs_frame)
        pen = pg.mkPen(color=(255, 0, 0))

        # graphics_view = pg.PlotWidget()
        graphics_view.setGeometry(QtCore.QRect(50, 30, 231, 151))
        graphics_view.setObjectName("graphics_view")
        gv = graphics_view.plot(self.x, values, pen)
        # self.graphics_view.append(graphics_view)
        self.graphs_widgets.append(gv)
        self.formLayout.addRow(graphics_view)

    def set_counters(self):
        # create a table to hold the counters
        self.counters_tableWidget.setColumnCount(len(self.counters))
        self.counters_tableWidget.setRowCount(3)
        self.counters_tableWidget.setHorizontalHeaderLabels([*self.counters.keys()])
        self.counters_tableWidget.setVerticalHeaderLabels(["Parameters", "Total", "Successive"])
        # Set an adaptive width for table
        trials_table_adaptive_width = self.counters_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        delegate = ReadOnlyDelegate(self.counters_tableWidget)
        # set the table to be read-only
        self.counters_tableWidget.setItemDelegateForRow(0, delegate)
        self.counters_tableWidget.setItemDelegateForRow(1, delegate)
        for i in range(len(self.counters)):
            self.counters_tableWidget.setItem(0, i, QTableWidgetItem(str(self.trials_params[i])))

    def set_total_count(self, counter):
        # for i in range(1, self.counters_tableWidget.columnCount())
        self.total_counter = counter
        # self.counter = int(counter[0])
        # self.counters_tableWidget.setItem(1, 1, QTableWidgetItem(str(self.counter)))
        # for i in range(len(counter)):
        #     self.counters_tableWidget.setItem(1, i, QTableWidgetItem(str(int(counter[i]))))

        # self.counters_tableWidget.setItem(1, 1, QTableWidgetItem(str(self.counter)))

    def set_successive_count(self, counter):
        # this should be atomic so won't refresh before updating all values!
        self.successive_counter = counter
        # for i in range(len(counter)):
        #     self.counters_tableWidget.setItem(2, i, QTableWidgetItem(str(int(counter[i]))))
        # pass

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Run a session"))
        # self.total_counter_label.setText(_translate("dialog", "Total trials: "))
        # self.success_rate_label.setText(_translate("dialog", "Success rate: "))

    def EventHandler(self, sender, *event_args):
        if type(sender) != BehaviorSystemViewModel:
            pass
        if event_args[0][0] == "VM_trial_types_total_counter":
            total_counter = self.vm.sessionVM.trial_types_total_counter
            self.set_total_count(total_counter)
        if event_args[0][0] == "VM_trial_types_successive_counter":
            success_counter = self.vm.sessionVM.trial_types_successive_counter
            self.set_successive_count(success_counter)
        if event_args[0][0] == "VM_is_running_session":
            # TODO stop all running things, or upload message saying session has ended
            pass
        if event_args[0][0] == "VM_end_session":
            self.end_session = self.vm.curr_session.end_session
            # if self.end_session:
            #     self.graphs_timer.stop()
            #     self.counters_timer.stop()
            # TODO stop all running things, or upload message saying session has ended
            pass
            # chang
            # change the property
            # self.is_running_session = self.model.is_running_session #is this necessary or it updates on its own

# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = RunningGraphsUi()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

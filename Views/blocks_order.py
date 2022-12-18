import threading
from collections import OrderedDict

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem

from Models import Trial_Model
from Views.control_session_board import ControlSessionBoardUi
from Views.utils import error_warning, dict_one_line_style


class BlocksOrderUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.trials = self.parent.trials_in_session  # TODO check if relevant at all
        self.trials_names, self.trials_params = self.parse_trial_params()
        self.window_gridLayout = None
        self.main_gridLayout = None
        # self.blocks_label = None
        self.blocks_label = self.parent.block_list
        self.header_label = None
        self.blocks_order_label = None
        self.buttonBox = None
        self.blocks_comboBox = self.parent.block_list
        #self.blocks_comboBox = None
        self.add_pushButton = None
        self.remove_pushButton = None
        self.remove_pushButton = None
        self.blocks_order_tableWidget = None
        self.set_new_block_horizontalLayout = None
        self.set_new_block_pushButton = None
        self.remove_block_pushButton = None
        self.blocks_tableWidget = None
        self.selected_block = -1
        self.blocks = OrderedDict({})
        # self.blocks_in_session = []
        #self.blocks_in_session = self.parent.blocks_ord

    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(596, 506)
        self.window_gridLayout = QtWidgets.QGridLayout(dialog)
        self.window_gridLayout.setObjectName("window_gridLayout")
        self.main_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.setContentsMargins(10, -1, 10, -1)
        self.main_gridLayout.setObjectName("main_gridLayout")
        self.blocks_label = QtWidgets.QLabel(dialog)
        self.blocks_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.blocks_label.setObjectName("blocks_label")
        self.main_gridLayout.addWidget(self.blocks_label, 1, 0, 1, 4)
        self.header_label = QtWidgets.QLabel(dialog)
        self.header_label.setStyleSheet("font: 30pt \"Gabriola\";")
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.main_gridLayout.addWidget(self.header_label, 0, 0, 1, 4)
        self.blocks_order_label = QtWidgets.QLabel(dialog)
        self.blocks_order_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.blocks_order_label.setObjectName("blocks_order_label")
        self.main_gridLayout.addWidget(self.blocks_order_label, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.main_gridLayout.addWidget(self.buttonBox, 9, 1, 1, 2)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addItem(spacer_item, 8, 1, 1, 1)
        self.blocks_comboBox = QtWidgets.QComboBox(dialog)
        self.blocks_comboBox.setObjectName("blocks_comboBox")
        self.main_gridLayout.addWidget(self.blocks_comboBox, 6, 2, 1, 1)
        self.add_pushButton = QtWidgets.QPushButton(dialog)
        self.add_pushButton.clicked.connect(self.on_add_click)
        self.add_pushButton.setObjectName("add_pushButton")
        self.main_gridLayout.addWidget(self.add_pushButton, 6, 1, 1, 1)
        self.remove_pushButton = QtWidgets.QPushButton(dialog)
        self.remove_pushButton.clicked.connect(self.on_remove_block_in_session_click)
        self.remove_pushButton.setObjectName("remove_pushButton")
        self.main_gridLayout.addWidget(self.remove_pushButton, 7, 1, 1, 1)
        self.blocks_order_tableWidget = QtWidgets.QTableWidget(dialog)
        self.blocks_order_tableWidget.setObjectName("blocks_order_tableWidget")
        # self.blocks_in_session_tableWidget.setColumnCount(0)
        self.blocks_order_tableWidget.setColumnCount(0)
        self.blocks_order_tableWidget.setRowCount(1)
        self.blocks_order_tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Blocks"))
        # set the data
        for j in range(len(self.parent.blocks_ord)):
            column_position = self.blocks_order_tableWidget.columnCount()
            self.blocks_order_tableWidget.insertColumn(column_position)
            self.blocks_order_tableWidget.\
                setHorizontalHeaderItem(column_position,
                                        QTableWidgetItem(self.parent.blocks_ord[j]))

        self.main_gridLayout.addWidget(self.blocks_order_tableWidget, 5, 0, 1, 4)
        self.set_new_block_horizontalLayout = QtWidgets.QHBoxLayout()
        self.set_new_block_horizontalLayout.setObjectName("set_new_block_horizontalLayout")
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.set_new_block_horizontalLayout.addItem(spacer_item1)
        self.set_new_block_pushButton = QtWidgets.QPushButton(dialog)
        self.set_new_block_pushButton.clicked.connect(self.on_set_new_block_click)
        self.set_new_block_pushButton.setObjectName("set_new_block_pushButton")
        self.set_new_block_horizontalLayout.addWidget(self.set_new_block_pushButton)
        self.main_gridLayout.addLayout(self.set_new_block_horizontalLayout, 3, 1, 1, 3)
        self.remove_block_pushButton = QtWidgets.QPushButton(dialog)
        self.remove_block_pushButton.clicked.connect(self.on_remove_block_click)
        self.remove_block_pushButton.setObjectName("remove_block_pushButton")
        self.set_new_block_horizontalLayout.addWidget(self.remove_block_pushButton)
        self.main_gridLayout.addLayout(self.set_new_block_horizontalLayout, 3, 2, 1, 3)

        self.blocks_tableWidget = QtWidgets.QTableWidget(dialog)
        self.blocks_tableWidget.setObjectName("blocks_tableWidget")
        self.blocks_tableWidget.setColumnCount(1)
        self.blocks_tableWidget.setRowCount(len(self.trials_names) + 1)
        self.blocks_tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.main_gridLayout.addWidget(self.blocks_tableWidget, 2, 0, 1, 4)
        # self.blocks_tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        self.main_gridLayout.setColumnStretch(0, 5)
        self.main_gridLayout.setRowStretch(0, 1)
        self.main_gridLayout.setRowStretch(1, 1)
        self.main_gridLayout.setRowStretch(2, 5)
        self.main_gridLayout.setRowStretch(3, 1)
        self.main_gridLayout.setRowStretch(4, 1)
        self.main_gridLayout.setRowStretch(5, 1)
        self.main_gridLayout.setRowStretch(6, 1)
        self.main_gridLayout.setRowStretch(7, 1)
        self.main_gridLayout.setRowStretch(8, 1)
        self.main_gridLayout.setRowStretch(9, 1)
        self.window_gridLayout.addLayout(self.main_gridLayout, 0, 2, 1, 1)
        self.window_gridLayout.setColumnMinimumWidth(0, 1)
        self.window_gridLayout.setColumnMinimumWidth(1, 1)
        self.window_gridLayout.setColumnMinimumWidth(2, 1)

        # Set an adaptive width for table
        trials_table_adaptive_width = self.blocks_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        trials_table_adaptive_width = self.blocks_order_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        self.fill_block_table()

        self.retranslateUi(dialog)
        self.buttonBox.rejected.connect(dialog.reject)
        self.buttonBox.accepted.connect(self.accept)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def fill_block_table(self):
        # set the first column header- parameters for each trial
        self.blocks_tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Parameters"))
        # set the first row header-the block's name
        self.blocks_tableWidget.setVerticalHeaderItem(0, QTableWidgetItem("Block size"))
        # update rows' headers- each with a trial name
        # and on the right it's parameters
        for i in range(len(self.trials_names)):
            self.blocks_tableWidget.setVerticalHeaderItem(i + 1, QTableWidgetItem(self.trials_names[i]))
            self.blocks_tableWidget.setItem(i + 1, 0,
                                            QTableWidgetItem(dict_one_line_style(self.trials_params[i][0])))
        # if there are blocks set already
        if len(self.parent.block_list) != 0:
            for block_name in self.parent.block_list:
                column_position = self.blocks_tableWidget.columnCount()
                self.add_block_column(block_name, column_position)
            self.fill_data_in_table()

    def fill_data_in_table(self):
        # go over the list of blocks
        # fill if relevant: block size in first row, then go over trials and fill percentage
        for j in range(len(self.blocks)):
            size = self.parent.block_sizes[j]
            self.blocks_tableWidget.setItem(0, j + 1, QTableWidgetItem(str(size)))
            # go over the j-th block's data
            for i in range(1, self.blocks_tableWidget.rowCount()):
                # check if no data was given
                self.blocks_tableWidget.setItem(i, j + 1,
                                                QTableWidgetItem(str(self.parent.percent_per_block[i - 1][j])))

    def add_block_column(self, block_name, pos):
        self.blocks[block_name] = []
        self.blocks_comboBox.addItems([block_name])
        self.blocks_tableWidget.insertColumn(pos)
        self.blocks_tableWidget.setHorizontalHeaderItem(pos, QTableWidgetItem(block_name))
        # append the new block to list of blocks in parent
        if block_name not in self.parent.block_list:
            self.parent.block_list.append(block_name)

    def on_set_new_block_click(self):
        column_position = self.blocks_tableWidget.columnCount()
        new_block_header, ok_pressed = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(),
                                                                      "Set a new block", "Block name:",
                                                                      QtWidgets.QLineEdit.Normal)

        # check if the user adds a new block
        if ok_pressed:
            # validate name of block doesn't already exists
            if new_block_header in self.parent.block_list:
                # TODO error until writes different name
                pass
            else:
                self.add_block_column(new_block_header, column_position)

    def on_remove_block_click(self):
        is_not_empty = len(self.blocks) > 0
        is_col_selected = self.blocks_tableWidget.currentColumn() != -1
        # check if there are blocks and a block was selected
        if is_not_empty and is_col_selected:
            # get the chosen block's column and remove it
            index = self.blocks_tableWidget.currentColumn() - 1  # ignore 0th which represents blocks parameters
            # iterator = iter(self.blocks.keys())
            # for _ in range(index):
            #     next(iterator)
            # del self.blocks[next(iterator)]
            block_name = self.parent.block_list[index]
            del self.blocks[block_name]
            del self.parent.block_list[index]
            self.blocks_tableWidget.removeColumn(self.blocks_tableWidget.currentColumn())
            # set current column to be unselected
            self.blocks_tableWidget.setCurrentCell(self.blocks_tableWidget.currentRow(), -1)
            self.blocks_comboBox.clear()
            self.blocks_comboBox.addItems(self.blocks)
            # go over the list of blocks order, and remove elements that equal to the removed block
            i = 0
            while i < len(self.parent.blocks_ord):
                # if the current element is the removed block, remove it from gui and from parents list
                if self.parent.blocks_ord[i] == block_name:
                    self.blocks_order_tableWidget.removeColumn(i)
                    del self.parent.blocks_ord[i]
                # go to the next element
                else:
                    i += 1

        # error cases
        elif is_not_empty:
            error_warning("There are no block in the current session.")
        else:
            error_warning("A block is not selected.")


    def read_table_data(self):

        for key, val in self.blocks.items():
            self.blocks[key] = []
        # read all the given data for each block
        for j in range(len(self.blocks)):
            # go over the j-th block's data
            for i in range(self.blocks_tableWidget.rowCount()):
                # check if no data was given
                if self.blocks_tableWidget.item(i, j + 1) is None:
                    error_warning("An error accrued, please try again.")
                    return False
                current_value = self.blocks_tableWidget.item(i, j + 1).text()
                # check if the given value is a number
                if current_value.isnumeric():
                    # if so, add it to the j-th block's
                    jth_block_values = list(self.blocks.items())[j][1]
                    jth_block_values.append(int(current_value))
                else:
                    error_warning("An error accrued, please try again.")
                    return False
            # check if the percentages sum to 100
            sum_percentages = sum(jth_block_values) - jth_block_values[0]
            if sum_percentages != 100:
                error_warning("Sum of percentage for each block must be 100")
                return False
            # set j-th block size
            if j < len(self.parent.block_sizes):
                self.parent.block_sizes[j] = jth_block_values[0]
            else:
                self.parent.block_sizes.append(jth_block_values[0])
            # set percents per block for each trial
            for k in range(1, len(jth_block_values)):
                if j < len(self.parent.percent_per_block[k - 1]):
                    self.parent.percent_per_block[k - 1][j] = jth_block_values[k]
                else:
                    self.parent.percent_per_block[k - 1].append(jth_block_values[k])
        if len(self.parent.blocks_ord)<1:
            error_warning("Please enter blocks order to run in session")
            return False
        return True

    def accept(self):
        # check the input in the table of blocks
        is_valid = self.read_table_data()
        if is_valid:
            self.start_session()

    def start_session(self):
        trials = self.parent.vm.create_trial_list(self.parent.trials_in_session)
        self.parent.vm.curr_session.trials_def = Trial_Model.Trials_def_blocks(trials, self.parent.block_list,
                                                                               self.parent.percent_per_block,
                                                                               self.parent.block_sizes,
                                                                               self.parent.blocks_ord)
        # open a new session
        self.session_window = QtWidgets.QDialog()
        self.session_ui = ControlSessionBoardUi(self)
        self.session_ui.setupUi(self.session_window)
        self.session_window.show()

        # close current window
        self.parent.trials_ord_window.close()
        threading.Thread(target=self.parent.vm.start_Session).start()
        # self.parent.vm.start_Session()
        # TODO: need to close parent window

    def on_add_click(self):
        # add a block to the current session
        column_position = self.blocks_order_tableWidget.columnCount() + 1
        current_block = self.blocks_comboBox.currentText()
        # self.blocks_order_tableWidget.insertColumn(column_position)
        # self.blocks_order_tableWidget.setHorizontalHeaderItem(column_position,
        #                                                       QTableWidgetItem(
        #                                                                current_block))
        self.blocks_order_tableWidget.setColumnCount(column_position)
        self.blocks_order_tableWidget.setItem(0, column_position - 1, QTableWidgetItem(current_block))
        self.parent.blocks_ord.append(current_block)

    def on_remove_block_in_session_click(self):
        is_not_empty = len(self.parent.blocks_ord) > 0
        index = self.blocks_order_tableWidget.currentColumn()
        is_col_selected = index != -1
        # check if there are blocks and a block was selected
        if is_not_empty and is_col_selected:
            # get the chosen block's column and remove it
            # index = self.blocks_in_session_tableWidget.currentColumn()
            # parameters
            # iterator = iter(self.blocks_in_session.keys())
            # for _ in range(index):
            #     next(iterator)
            # del self.blocks_in_session[next(iterator)]
            #del self.blocks_in_session[index]
            del self.parent.blocks_ord[index]
# TODO check this part
            self.blocks_order_tableWidget.removeColumn(index)
            # set current column to be unselected
            self.blocks_order_tableWidget.setCurrentCell(self.blocks_order_tableWidget.currentRow(), -1)
#until here

        # error case
        elif is_not_empty:
            error_warning("A block is not selected.")
        else:
            error_warning("There are no block in the current session.")

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Blocks order"))
        self.blocks_label.setText(_translate("dialog", "Blocks:"))
        self.header_label.setText(_translate("dialog", "Define blocks order session"))
        self.blocks_order_label.setText(_translate("dialog", "Blocks order:"))
        self.add_pushButton.setText(_translate("dialog", "Add"))
        self.remove_pushButton.setText(_translate("dialog", "Remove"))
        self.set_new_block_pushButton.setText(_translate("dialog", "Set a new block"))
        self.remove_block_pushButton.setText(_translate("dialog", "Remove a block"))

    def parse_trial_params(self):
        trials_names, trials_params = [], []
        for trial in self.trials:
            pair = [(keys, val) for keys, val in trial.items()]
            name = [i[0] for i in pair]
            param = [i[1] for i in pair]
            trials_names += name
            trials_params.append(param)
        return trials_names, trials_params

from collections import OrderedDict

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QDialog, QDialogButtonBox, QLabel, \
    QVBoxLayout, QPushButton

from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.utils import error_warning, list_to_str, get_ui_path


class WarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning")

        q_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(q_buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Trial type was changed, are you sure you want to do this?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class EditTrialTypeUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = parent.vm
        self.main_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.main_gridLayout = None
        self.scroll_verticalLayout = QtWidgets.QVBoxLayout()
        self.trial_types_names = self.vm.get_trial_names()
        self.trial_types_dict = self.vm.get_list_trials_types_def()
        self.chosen_trial_type_name = ""
        self.choose_trial_type_horizontalLayout = QtWidgets.QHBoxLayout()
        self.choose_trial_type_label = None
        self.trial_types_comboBox = None
        self.change_trial_type_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.change_trial_type_label = None
        self.trial_type_name_lineEdit = None
        self.add_event_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Add_event_pushButton = None
        self.events_name = ["1", "2", "3", "4"]
        self.events_dict = {"1": ['a', 'b', 'c'], "2": ['d'], "3": ['e', 'f'], "4": ['g']}
        self.events_comboBox = None
        self.remove_horizontalLayout = QtWidgets.QHBoxLayout()
        self.remove_pushButton = None
        self.events_order_label = None
        self.trial_types_tableWidget = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None
        self.accept_pushButton = None
        self.new_name = ""
        self.order = OrderedDict()

        self.vm.property_changed += self.EventHandler
        self.is_error = False

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('edit_trial_type.ui'), main_window)

        self.back_pushButton = main_window.findChild(QPushButton, 'back_pushButton')
        self.back_pushButton.clicked.connect(self.on_back_click)

        self.Add_event_pushButton = main_window.findChild(QPushButton, 'Add_event_pushButton')
        self.Add_event_pushButton.clicked.connect(self.on_add_click)

        return
        main_window.setObjectName("main_window")
        main_window.resize(493, 597)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # set a header for the window
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Arial\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.window_gridLayout.addWidget(self.headline_label, 0, 0, 1, 1)
        # set a scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 473, 386))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.main_gridLayout.setObjectName("gridLayout")
        # set a layout for the scroll area
        self.scroll_verticalLayout.setObjectName("scroll_verticalLayout")
        # set to choose a trial template
        self.choose_trial_type_horizontalLayout.setObjectName("choose_trial_type_horizontalLayout")
        self.choose_trial_type_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.choose_trial_type_label.setObjectName("choose_trial_type_label")
        self.choose_trial_type_horizontalLayout.addWidget(self.choose_trial_type_label)
        self.trial_types_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.trial_types_comboBox.setObjectName("trial_types_comboBox")
        self.trial_types_comboBox.addItems(self.trial_types_names)
        self.trial_types_comboBox.activated.connect(self.trial_types_click)
        self.choose_trial_type_horizontalLayout.addWidget(self.trial_types_comboBox)
        self.choose_trial_type_horizontalLayout.setStretch(0, 1)
        self.choose_trial_type_horizontalLayout.setStretch(1, 2)
        self.main_gridLayout.addLayout(self.choose_trial_type_horizontalLayout, 0, 0, 1, 1)
        # set to change trial type name events
        # self.change_trial_type_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.change_trial_type_name_horizontalLayout.setObjectName("change_trial_type_name_horizontalLayout")
        self.change_trial_type_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.change_trial_type_label.setObjectName("change_trial_type_label")
        self.change_trial_type_name_horizontalLayout.addWidget(self.change_trial_type_label)
        self.trial_type_name_lineEdit = QtWidgets.QLineEdit(self.central_widget)
        self.trial_type_name_lineEdit.setEnabled(True)
        self.trial_type_name_lineEdit.setText(self.chosen_trial_type_name)
        self.trial_type_name_lineEdit.editingFinished.connect(self.on_trial_type_name_edit)
        self.trial_type_name_lineEdit.setStyleSheet("font: 12pt \"Arial\";")
        self.change_trial_type_name_horizontalLayout.addWidget(self.trial_type_name_lineEdit)
        self.change_trial_type_name_horizontalLayout.setStretch(0, 1)
        self.change_trial_type_name_horizontalLayout.setStretch(1, 2)
        self.main_gridLayout.addLayout(self.change_trial_type_name_horizontalLayout, 1, 0, 1, 1)
        # set to add events
        self.add_event_horizontalLayout.setObjectName("add_event_horizontalLayout")
        self.Add_event_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.Add_event_pushButton.setObjectName("Add_event_pushButton")
        self.Add_event_pushButton.clicked.connect(self.on_add_click)
        self.add_event_horizontalLayout.addWidget(self.Add_event_pushButton)
        self.events_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.events_comboBox.setObjectName("events_comboBox")
        self.events_comboBox.addItems(self.events_name)
        self.add_event_horizontalLayout.addWidget(self.events_comboBox)
        self.add_event_horizontalLayout.setStretch(0, 1)
        self.add_event_horizontalLayout.setStretch(1, 2)
        self.main_gridLayout.addLayout(self.add_event_horizontalLayout, 2, 0, 1, 1)
        # set to remove events
        self.remove_horizontalLayout.setObjectName("remove_horizontalLayout")
        self.remove_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.remove_pushButton.setObjectName("remove_pushButton")
        self.remove_pushButton.clicked.connect(self.on_remove_click)
        self.remove_horizontalLayout.addWidget(self.remove_pushButton)
        #spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.remove_horizontalLayout.addItem(spacer_item)
        self.remove_horizontalLayout.setStretch(0, 1)
        self.remove_horizontalLayout.setStretch(1, 2)
        self.scroll_verticalLayout.addLayout(self.remove_horizontalLayout)
        # set to display events order
        self.events_order_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.events_order_label.setObjectName("events_order_label")
        self.scroll_verticalLayout.addWidget(self.events_order_label)
        self.set_trial_types_table()
        self.scroll_verticalLayout.addWidget(self.trial_types_tableWidget)
        self.scroll_verticalLayout.setStretch(0, 1)
        self.scroll_verticalLayout.setStretch(2, 5)
        self.main_gridLayout.addLayout(self.scroll_verticalLayout, 4, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        # add a back button
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        #left_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.navigation_horizontalLayout.addItem(left_spacer_item)
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        self.accept_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.accept_pushButton.setObjectName("accept_pushButton")
        self.accept_pushButton.clicked.connect(self.on_accept_click)
        self.navigation_horizontalLayout.addWidget(self.accept_pushButton)
        #right_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
        #                                          QtWidgets.QSizePolicy.Minimum)
        #self.navigation_horizontalLayout.addItem(right_spacer_item)
        self.navigation_horizontalLayout.setStretch(0, 1)
        self.navigation_horizontalLayout.setStretch(1, 1)
        self.navigation_horizontalLayout.setStretch(2, 1)
        self.navigation_horizontalLayout.setStretch(3, 1)
        self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 2, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        # set default indexes for both combobox
        self.trial_types_click(0)
        self.events_comboBox.setCurrentIndex(0)

    def trial_types_click(self, index):
        if len(self.trial_types_names) == 0:
            return

        current_trial_type = self.trial_types_names[index]
        if self.chosen_trial_type_name is not current_trial_type:
            if self.chosen_trial_type_name != "":  # trial type selection was changed
                dlg = WarningDialog()
                if dlg.exec():  # ok case
                    self.chosen_trial_type_name = current_trial_type
                    self.update_trial_types_table()
                    self.order = self.trial_types_dict[self.chosen_trial_type_name]
                    return
                else:  # cancel case
                    self.events_comboBox.setCurrentIndex(self.events_name.index(self.chosen_trial_type_name))
                    self.order = self.trial_types_dict[self.chosen_trial_type_name]
                    return
            self.chosen_trial_type_name = current_trial_type
            self.order = self.trial_types_dict[self.chosen_trial_type_name]
            self.update_trial_types_table()

    def update_trial_types_table(self):
        self.trial_type_name_lineEdit.setText(self.chosen_trial_type_name)
        self.trial_types_tableWidget.setRowCount(len(self.trial_types_dict[self.chosen_trial_type_name].keys()))
        index = 0
        for event, params in self.trial_types_dict[self.chosen_trial_type_name].items():
            self.trial_types_tableWidget.setItem(index, 0,
                                                 QTableWidgetItem(event))
            self.trial_types_tableWidget.setItem(index, 1,
                                                 QTableWidgetItem(list_to_str(params)))
            index += 1

    def set_trial_types_table(self):
        self.trial_types_tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.trial_types_tableWidget.setObjectName("trial_types_tableWidget")
        self.trial_types_tableWidget.setColumnCount(2)
        self.trial_types_tableWidget.setRowCount(0)
        # set table to be scrolled vertically
        #self.trial_types_tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.sectionResized)
        #self.trial_types_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Set an adaptive width for table
        trials_table_adaptive_width = self.trial_types_tableWidget.horizontalHeader()
        #trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        # set headers for columns
        self.trial_types_tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Event"))
        self.trial_types_tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Parameters"))

    def on_trial_type_name_edit(self):
        self.chosen_trial_type_name = self.trial_type_name_lineEdit.text()

    def on_add_click(self):
        current_event = self.events_comboBox.currentText()
        params = self.events_dict[current_event]
        row = self.trial_types_tableWidget.rowCount()
        self.trial_types_tableWidget.setRowCount(row + 1)
        self.trial_types_tableWidget.setItem(row, 0, QTableWidgetItem(current_event))
        self.trial_types_tableWidget.setItem(row, 1, QTableWidgetItem(list_to_str(params)))
        self.order[current_event] = params

    def on_remove_click(self):
        is_not_empty = len(self.trial_types_names) > 0
        index = self.trial_types_tableWidget.currentRow()
        is_row_selected = index != -1
        # check if there are events and an event was selected
        if is_not_empty and is_row_selected:
            erased_event = list(self.order.keys())[index]
            del self.order[erased_event]
            # del self.parent.block_list[index]
            self.trial_types_tableWidget.removeRow(index)
            # set current column to be unselected
            self.trial_types_tableWidget.setCurrentCell(-1, self.trial_types_tableWidget.currentColumn())
        # error cases
        elif is_not_empty:
            error_warning("There are no events in the current trial type.")
        else:
            error_warning("An event is not selected.")

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def on_accept_click(self):
        if not self.is_error:
            self.update_db()
            self.parent.main_window.show()
            self.main_window.close()

    # TODO update trial template on db
    def update_db(self):
        pass

    def EventHandler(self, sender, *event_args):
        if type(sender) != BehaviorSystemViewModel:
            pass
        if event_args[0][0] == "VM_edit_trial_types_error":
            error_warning("This trial type cannot be edited since it is in templates history")
            self.is_error = True
        elif event_args[0][0] == "VM_edit_trial_types_success":
            self.is_error = False


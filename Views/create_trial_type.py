from PyQt6 import QtCore, QtGui, QtWidgets

from Views.utils import error_warning


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class CreateTrialTypeUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.main_gridLayout = None
        self.scroll_verticalLayout = QtWidgets.QVBoxLayout()
        self.trial_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.trial_name_label = None
        self.trial_type_name_lineEdit = None
        self.is_contingent_horizontalLayout = QtWidgets.QHBoxLayout()
        self.simple_radioButton = None
        self.contingent_radioButton = None
        self.add_event_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_event_pushButton = None
        self.events = self.parent.vm.model.output_events_names
        self.events_comboBox = None
        self.remove_horizontalLayout = QtWidgets.QHBoxLayout()
        self.remove_event_pushButton = None
        self.events_label = None
        self.events_tableWidget = None
        self.accept_horizontalLayout = QtWidgets.QHBoxLayout()
        self.accept_pushButton = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None

        # values to return
        self.trial_type_name = ""
        self.chosen_event = ""
        self.chosen_is_contingent = False
        self.events_order = []
        self.is_contingent_order = []

    def setupUi(self, main_window):
        self.main_window = main_window
        main_window.setObjectName("main_window")
        main_window.resize(496, 600)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # set a header for the window
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Gabriola\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.window_gridLayout.addWidget(self.headline_label, 0, 0, 1, 1)
        # set a scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("Gabriola")
        font.setPointSize(15)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 476, 389))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.main_gridLayout.setObjectName("main_gridLayout")
        self.scroll_verticalLayout.setObjectName("scroll_verticalLayout")
        self.trial_name_horizontalLayout.setObjectName("trial_name_horizontalLayout")
        self.trial_name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.trial_name_label.setObjectName("trial_name_label")
        self.trial_name_horizontalLayout.addWidget(self.trial_name_label)
        self.trial_type_name_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.trial_type_name_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
        self.trial_type_name_lineEdit.editingFinished.connect(self.on_trial_type_name_edit)
        self.trial_type_name_lineEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.trial_type_name_lineEdit.setFont(font)
        # self.trial_type_name_lineEdit.setTabStopWidth(80)
        self.trial_type_name_lineEdit.setObjectName("trial_type_name_lineEdit")
        self.trial_name_horizontalLayout.addWidget(self.trial_type_name_lineEdit)
        self.trial_name_horizontalLayout.setStretch(0, 1)
        self.trial_name_horizontalLayout.setStretch(1, 2)
        self.scroll_verticalLayout.addLayout(self.trial_name_horizontalLayout)
        # define if simple or contingent event
        self.is_contingent_horizontalLayout.setObjectName("is_contingent_horizontalLayout")
        self.simple_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.simple_radioButton.setObjectName("simple_radioButton")
        self.simple_radioButton.setChecked(True)
        self.is_contingent_horizontalLayout.addWidget(self.simple_radioButton)
        self.contingent_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.contingent_radioButton.setObjectName("contingent_radioButton")
        self.is_contingent_horizontalLayout.addWidget(self.contingent_radioButton)
        self.scroll_verticalLayout.addLayout(self.is_contingent_horizontalLayout)
        # settings to add an event
        self.add_event_horizontalLayout.setObjectName("add_event_horizontalLayout")
        self.add_event_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.add_event_pushButton.setObjectName("add_event_pushButton")
        self.add_event_pushButton.clicked.connect(self.on_add_click)
        self.add_event_horizontalLayout.addWidget(self.add_event_pushButton)
        self.events_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.events_comboBox.setObjectName("events_comboBox")
        self.events_comboBox.addItems(self.events)
        self.events_comboBox.setCurrentIndex(0)
        self.add_event_horizontalLayout.addWidget(self.events_comboBox)
        self.add_event_horizontalLayout.setStretch(0, 1)
        self.add_event_horizontalLayout.setStretch(1, 2)
        self.scroll_verticalLayout.addLayout(self.add_event_horizontalLayout)
        # settings to remove an event
        self.remove_horizontalLayout.setObjectName("remove_horizontalLayout")
        # set a push button to remove an event
        self.remove_event_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.remove_event_pushButton.setObjectName("remove_event_pushButton")
        self.remove_event_pushButton.clicked.connect(self.on_remove_click)
        self.remove_horizontalLayout.addWidget(self.remove_event_pushButton)
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.remove_horizontalLayout.addItem(spacer_item)
        self.remove_horizontalLayout.setStretch(0, 1)
        self.remove_horizontalLayout.setStretch(1, 2)
        self.scroll_verticalLayout.addLayout(self.remove_horizontalLayout)
        # set events table
        self.events_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.events_label.setObjectName("events_label")
        self.scroll_verticalLayout.addWidget(self.events_label)
        self.events_tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        # set an adaptive width for table
        trials_table_adaptive_width = self.events_tableWidget.horizontalHeader()
        trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.events_tableWidget.setFont(font)
        self.events_tableWidget.setObjectName("events_tableWidget")
        self.events_tableWidget.setColumnCount(2)
        self.events_tableWidget.setRowCount(0)
        self.events_tableWidget.setStyleSheet("font: 12pt \"Gabriola\";")
        self.events_tableWidget.setVerticalHeaderItem(0, QTableWidgetItem(""))
        # set headers for each column
        self.events_tableWidget.setHorizontalHeaderLabels(["Event", "Simple/Contingent"])
        delegate = ReadOnlyDelegate(self.events_tableWidget)
        # set the table to be read-only
        self.events_tableWidget.setItemDelegateForColumn(0, delegate)
        self.events_tableWidget.setItemDelegateForColumn(1, delegate)
        self.events_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.scroll_verticalLayout.addWidget(self.events_tableWidget)
        self.scroll_verticalLayout.setStretch(0, 1)
        self.scroll_verticalLayout.setStretch(1, 1)
        self.scroll_verticalLayout.setStretch(2, 1)
        self.scroll_verticalLayout.setStretch(3, 1)
        self.scroll_verticalLayout.setStretch(4, 1)
        self.scroll_verticalLayout.setStretch(5, 5)
        self.main_gridLayout.addLayout(self.scroll_verticalLayout, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # set an option to add the new trial type
        self.accept_horizontalLayout.setObjectName("accept_horizontalLayout")
        right_spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(right_spacer_item1)
        self.accept_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.accept_pushButton.setObjectName("accept_pushButton")
        self.accept_pushButton.clicked.connect(self.accept)
        self.accept_horizontalLayout.addWidget(self.accept_pushButton)
        right_spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(right_spacer_item1)
        self.accept_horizontalLayout.setStretch(0, 1)
        self.accept_horizontalLayout.setStretch(1, 1)
        self.accept_horizontalLayout.setStretch(2, 1)
        self.main_gridLayout.addLayout(self.accept_horizontalLayout, 4, 0, 1, 1)

        self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        # set navigation options
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(spacer_item1)
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(spacer_item2)
        self.navigation_horizontalLayout.setStretch(0, 1)
        self.navigation_horizontalLayout.setStretch(1, 1)
        self.navigation_horizontalLayout.setStretch(2, 1)
        self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 2, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.is_contingent_cfg()

    def on_trial_type_name_edit(self):
        self.trial_type_name = self.trial_type_name_lineEdit.text()

    def is_contingent_cfg(self):
        self.simple_radioButton.toggled.connect(lambda: self.is_contingent_state(self.simple_radioButton))
        self.contingent_radioButton.toggled.connect(lambda: self.is_contingent_state(self.contingent_radioButton))

    def is_contingent_state(self, btn):
        # check if the event is simple or contingent
        if btn.isChecked():
            if btn.text() == "Simple event":
                self.chosen_is_contingent = False
            if btn.text() == "Contingent event":
                self.chosen_is_contingent = True

    def on_add_click(self):
        # add an event to the current trial type
        row_position = self.events_tableWidget.rowCount()
        current_event = self.events_comboBox.currentText()
        self.events_tableWidget.setRowCount(row_position + 1)
        self.events_tableWidget.setItem(row_position, 0, QTableWidgetItem(current_event))
        if self.chosen_is_contingent:
            self.events_tableWidget.setItem(row_position, 1, QTableWidgetItem("Contingent"))
        else:
            self.events_tableWidget.setItem(row_position, 1, QTableWidgetItem("Simple"))
        self.events_order.append(current_event)
        self.is_contingent_order.append(self.chosen_is_contingent)

    def on_remove_click(self):
        is_not_empty = len(self.events_order) > 0
        chosen_row = self.events_tableWidget.currentRow()
        is_col_selected = chosen_row != -1
        # check if there are events and an event was selected
        if is_not_empty and is_col_selected:
            del self.events_order[chosen_row]
            del self.is_contingent_order[chosen_row]
            self.events_tableWidget.removeRow(chosen_row)
            # set current column to be unselected
            self.events_tableWidget.setCurrentCell(-1, self.events_tableWidget.currentRow())
        # error cases
        elif is_not_empty:
            error_warning("An event is not selected.")
        else:
            error_warning("There are no events in the current session.")

    def accept(self):
        name = self.trial_type_name
        events = self.events_order
        self.parent.vm.add_trial_type(name, events)
        pass

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Create trial type"))
        self.headline_label.setText(_translate("main", "Create trial type"))
        self.trial_name_label.setText(_translate("main", "Trial name:"))
        self.simple_radioButton.setText(_translate("main", "Simple event"))
        self.contingent_radioButton.setText(_translate("main", "Contingent event"))
        self.add_event_pushButton.setText(_translate("main", "Add event"))
        self.remove_event_pushButton.setText(_translate("main", "Remove event"))
        self.events_label.setText(_translate("main", "Events:"))
        self.accept_pushButton.setText(_translate("main", "Add trial type"))
        self.back_pushButton.setText(_translate("main", "Back"))

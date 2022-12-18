from PyQt5 import QtCore, QtGui, QtWidgets

from Views.utils import error_warning, notification


class CreateEventUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.main_window = None
        self.central_widget = None
        self.window_verticalLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.main_gridLayout = None
        self.scroll_verticalLayout = QtWidgets.QVBoxLayout()
        self.event_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.event_name_label = None
        self.event_name_lineEdit = None
        self.event_port_horizontalLayout = QtWidgets.QHBoxLayout()
        self.event_port_label = None
        self.event_port_lineEdit = None
        self.input_radioButton = None
        self.output_radioButton = None
        self.io_horizontalLayout = QtWidgets.QHBoxLayout()
        self.analog_digital_horizontalLayout = QtWidgets.QHBoxLayout()
        self.digital_radioButton = None
        self.is_reward_horizontalLayout = QtWidgets.QHBoxLayout()
        self.is_reward_label = None
        self.is_reward_comboBox = None
        self.analog_radioButton = None
        self.analog_horizontalLayout = QtWidgets.QHBoxLayout()
        self.digital_horizontalLayout = QtWidgets.QHBoxLayout()
        self.digital_description_label = None
        self.analog_description_label = None
        self.accept_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_pushButton = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None
        # parameters to define new event
        self.event_name = ""
        self.event_port=""
        self.io_state = ""
        self.is_reward = False
        self.digital_or_analog = ""

    def setupUi(self, main_window):
        self.main_window = main_window
        main_window.setObjectName("main_window")
        main_window.resize(493, 571)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_verticalLayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.window_verticalLayout.setObjectName("window_verticalLayout")
        # set a header for the window
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Gabriola\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.window_verticalLayout.addWidget(self.headline_label)
        # set a scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("Gabriola")
        font.setPointSize(15)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 473, 313))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.main_gridLayout.setObjectName("main_gridLayout")
        self.scroll_verticalLayout.setObjectName("scroll_verticalLayout")
        self.scroll_verticalLayout.setStretch(0, 1)
        self.main_gridLayout.addLayout(self.scroll_verticalLayout, 3, 0, 1, 1)
        # set an option to choose a name for the event
        self.event_name_horizontalLayout.setObjectName("event_name_horizontalLayout")
        self.event_name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.event_name_label.setObjectName("event_name_label")
        self.event_name_horizontalLayout.addWidget(self.event_name_label)
        self.event_name_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.event_name_lineEdit.setObjectName("event_name_lineEdit")
        self.event_name_lineEdit.setEnabled(True)
        self.event_name_lineEdit.editingFinished.connect(self.on_event_name_edit)
        self.event_name_lineEdit.setStyleSheet("font: 12pt \"Gabriola\";")
        self.event_name_horizontalLayout.addWidget(self.event_name_lineEdit)
        self.event_name_horizontalLayout.setStretch(0, 1)
        self.event_name_horizontalLayout.setStretch(1, 1)
        self.scroll_verticalLayout.addLayout(self.event_name_horizontalLayout)
        # set port
        self.event_port_horizontalLayout.setObjectName("event_port_horizontalLayout")
        self.event_port_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.event_port_label.setObjectName("event_port_label")
        self.event_port_horizontalLayout.addWidget(self.event_port_label)
        self.event_port_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.event_port_lineEdit.setObjectName("event_port_lineEdit")
        self.event_port_lineEdit.setEnabled(True)
        self.event_port_lineEdit.editingFinished.connect(self.on_event_port_edit)
        self.event_port_lineEdit.setStyleSheet("font: 12pt \"Gabriola\";")
        self.event_port_horizontalLayout.addWidget(self.event_port_lineEdit)
        self.event_port_horizontalLayout.setStretch(0, 1)
        self.event_port_horizontalLayout.setStretch(1, 1)
        self.scroll_verticalLayout.addLayout(self.event_port_horizontalLayout)
        # set an option to choose if input/output event
        self.io_horizontalLayout.setObjectName("io_horizontalLayout")
        self.input_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.input_radioButton.setObjectName("input_radioButton")
        self.io_horizontalLayout.addWidget(self.input_radioButton)
        self.output_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.output_radioButton.setObjectName("output_radioButton")
        self.io_horizontalLayout.addWidget(self.output_radioButton)
        self.main_gridLayout.addLayout(self.io_horizontalLayout, 4, 0, 1, 1)
        self.io_horizontalLayout.setObjectName("io_horizontalLayout")
        # id output event, set an option to choose if this is a reward event
        self.is_reward_horizontalLayout.setObjectName("is_reward_horizontalLayout")
        self.is_reward_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.is_reward_label.setObjectName("is_reward_label")
        self.is_reward_label.setEnabled(False)
        self.is_reward_horizontalLayout.addWidget(self.is_reward_label)
        self.is_reward_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.is_reward_comboBox.setObjectName("is_reward_comboBox")
        self.is_reward_comboBox.addItems(["Yes", "No"])
        self.is_reward_comboBox.setEnabled(False)
        self.is_reward_comboBox.activated.connect(self.is_reward_click)
        self.is_reward_horizontalLayout.addWidget(self.is_reward_comboBox)
        self.main_gridLayout.addLayout(self.is_reward_horizontalLayout, 5, 0, 1, 1)
        # set an option to choose if digital or analog
        # digital
        self.digital_horizontalLayout.setObjectName("digital_horizontalLayout")
        self.digital_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.digital_radioButton.setObjectName("digital_radioButton")
        self.digital_horizontalLayout.addWidget(self.digital_radioButton)
        self.digital_description_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.digital_description_label.setObjectName("digital_description_label")
        self.digital_description_label.setEnabled(False)
        self.digital_horizontalLayout.addWidget(self.digital_description_label)
        self.main_gridLayout.addLayout(self.digital_horizontalLayout, 6, 0, 1, 1)
        # analog
        self.analog_horizontalLayout.setObjectName("analog_horizontalLayout")
        self.analog_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.analog_radioButton.setObjectName("analog_radioButton")
        self.analog_horizontalLayout.addWidget(self.analog_radioButton)
        # self.analog_digital_description_horizontalLayout.addWidget(self.digital_description_label)
        self.analog_description_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.analog_description_label.setObjectName("analog_description_label")
        self.analog_description_label.setEnabled(False)
        self.analog_horizontalLayout.addWidget(self.analog_description_label)
        self.main_gridLayout.addLayout(self.analog_horizontalLayout, 7, 0, 1, 1)
        # set an option to add the new event
        self.accept_horizontalLayout.setObjectName("accept_horizontalLayout")
        right_spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(right_spacer_item1)
        self.add_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.add_pushButton.setObjectName("add_pushButton")
        self.add_pushButton.clicked.connect(self.accept)
        self.accept_horizontalLayout.addWidget(self.add_pushButton)
        right_spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(right_spacer_item1)
        self.accept_horizontalLayout.setStretch(0, 1)
        self.accept_horizontalLayout.setStretch(1, 1)
        self.accept_horizontalLayout.setStretch(2, 1)
        self.main_gridLayout.addLayout(self.accept_horizontalLayout, 8, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.window_verticalLayout.addWidget(self.scrollArea)
        vertical_spacer_item = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
        self.window_verticalLayout.addItem(vertical_spacer_item)
        # set an option to go back to the main window
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        right_spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(right_spacer_item2)
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        left_spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(left_spacer_item2)
        self.navigation_horizontalLayout.setStretch(0, 1)
        self.navigation_horizontalLayout.setStretch(1, 1)
        self.navigation_horizontalLayout.setStretch(2, 1)
        self.window_verticalLayout.addLayout(self.navigation_horizontalLayout)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.set_io_display()
        self.set_digital_analog_display()

    def on_event_port_edit(self):
        self.event_port = self.event_port_lineEdit.text()

    def on_event_name_edit(self):
        self.event_name = self.event_name_lineEdit.text()

    def set_io_display(self):
        self.input_radioButton.toggled.connect(lambda: self.io_display(self.input_radioButton))
        self.output_radioButton.toggled \
            .connect(lambda: self.io_display(self.output_radioButton))

    def io_display(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "Input":  # input case
                self.is_reward_label.setEnabled(False)
                self.is_reward_comboBox.setEnabled(False)
                self.is_reward = False
                self.io_state = "Input"
            if btn.text() == "Output":  # output case
                self.is_reward_label.setEnabled(True)
                self.is_reward_comboBox.setEnabled(True)
                self.is_reward = self.is_reward_comboBox.currentText()
                self.io_state = "Output"

    def is_reward_click(self, index):
        if self.is_reward_comboBox.currentText() == "Yes":
            self.is_reward = True
        else:
            self.is_reward = False

    def set_digital_analog_display(self):
        self.digital_radioButton.toggled.connect(lambda: self.digital_analog_display(self.digital_radioButton))
        self.analog_radioButton.toggled \
            .connect(lambda: self.digital_analog_display(self.analog_radioButton))

    def digital_analog_display(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "Digital":  # digital case
                self.digital_description_label.setEnabled(True)
                self.analog_description_label.setEnabled(False)
                self.digital_or_analog = "Digital"
            if btn.text() == "Analog":  # analog case
                self.digital_description_label.setEnabled(False)
                self.analog_description_label.setEnabled(True)
                self.digital_or_analog = "Analog"

    def accept(self):
        if self.event_name == "" or self.event_port == "" or self.io_state == "" or self.digital_or_analog == "":
            error_warning("not all data is filled")
            return
        self.vm.insert_hardware_event_to_DB(self.event_name, self.event_port, self.io_state, self.digital_or_analog,
                                            str(self.is_reward))
        notification("Event was created")
        pass

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Create a new event"))
        self.headline_label.setText(_translate("main", "Create a new event"))
        self.add_pushButton.setText(_translate("main", "Add event"))
        self.is_reward_label.setText(_translate("main", "Is reward event:"))
        self.input_radioButton.setText(_translate("main", "Input"))
        self.output_radioButton.setText(_translate("main", "Output"))
        self.digital_radioButton.setText(_translate("main", "Digital"))
        self.analog_radioButton.setText(_translate("main", "Analog"))
        self.event_name_label.setText(_translate("main", "Event name:"))
        self.event_port_label.setText(_translate("main", "Port:"))
        self.digital_description_label.setText(_translate("main", "Duration"))
        self.analog_description_label.setText(_translate("main", "Duration, frequency, amplitude"))
        self.back_pushButton.setText(_translate("main", "Back"))

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class WarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning")

        q_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(q_buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to remove these session templates?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class DeleteSessionTemplate(object):
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
        self.remove_by_label = None
        self.subject_id_horizontalLayout = QtWidgets.QHBoxLayout()
        self.subject_id_radioButton = None
        self.subject_ids_comboBox = None
        self.experimenter_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.experimenter_name_radioButton = None
        self.experimenter_names_comboBox = None
        self.accept_horizontalLayout = QtWidgets.QHBoxLayout()
        self.accept_pushButton = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None

        self.subject_ids = self.parent.vm.get_list_of_subjects()[::-1]
        self.experimenter_names = [""]
        self.removed_subject_id = ""
        self.removed_experimenter_name = ""

    def setupUi(self, main_window):
        self.main_window = main_window
        main_window.setObjectName("main_window")
        main_window.resize(497, 500)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # set a header for the window
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 45pt \"Gabriola\";")
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 477, 258))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.main_gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.main_gridLayout.setObjectName("main_gridLayout")
        self.scroll_verticalLayout.setObjectName("scroll_verticalLayout")
        # set a label to choose option to remove
        self.remove_by_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.remove_by_label.setObjectName("remove_by_label")
        self.main_gridLayout.addWidget(self.remove_by_label, 0, 0, 1, 1)
        # set radio buttons to choose if remove templates by subject ids or by experimenter name
        # subject ids case
        self.subject_id_horizontalLayout.setObjectName("subject_id_horizontalLayout")
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.subject_id_horizontalLayout.addItem(spacer_item)
        self.subject_id_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.subject_id_radioButton.setObjectName("subject_id_radioButton")
        self.subject_id_horizontalLayout.addWidget(self.subject_id_radioButton)
        self.subject_ids_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.subject_ids_comboBox.setObjectName("subject_ids_comboBox")
        self.subject_ids_comboBox.activated.connect(self.subject_id_click)
        self.subject_ids_comboBox.addItems(self.subject_ids)
        self.subject_ids_comboBox.setEnabled(False)
        self.subject_id_horizontalLayout.addWidget(self.subject_ids_comboBox)
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.subject_id_horizontalLayout.addItem(spacer_item1)
        self.subject_id_horizontalLayout.setStretch(1, 1)
        self.subject_id_horizontalLayout.setStretch(2, 1)
        self.scroll_verticalLayout.addLayout(self.subject_id_horizontalLayout)
        # experimenter name case
        self.experimenter_name_horizontalLayout.setObjectName("experimenter_name_horizontalLayout")
        spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.experimenter_name_horizontalLayout.addItem(spacer_item2)
        self.experimenter_name_radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.experimenter_name_radioButton.setObjectName("experimenter_name_radioButton")
        self.experimenter_name_horizontalLayout.addWidget(self.experimenter_name_radioButton)
        self.experimenter_names_comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.experimenter_names_comboBox.setObjectName("experimenter_names_comboBox")
        self.experimenter_names_comboBox.addItems(self.experimenter_names)
        self.experimenter_names_comboBox.setEnabled(False)
        self.experimenter_names_comboBox.activated.connect(self.experimenter_name_click)
        self.experimenter_name_horizontalLayout.addWidget(self.experimenter_names_comboBox)
        spacer_item3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.experimenter_name_horizontalLayout.addItem(spacer_item3)
        self.experimenter_name_horizontalLayout.setStretch(1, 1)
        self.experimenter_name_horizontalLayout.setStretch(2, 1)
        self.scroll_verticalLayout.addLayout(self.experimenter_name_horizontalLayout)
        self.scroll_verticalLayout.setStretch(0, 1)
        self.scroll_verticalLayout.setStretch(1, 1)
        self.main_gridLayout.addLayout(self.scroll_verticalLayout, 3, 0, 1, 1)
        # set a button to accept
        self.accept_horizontalLayout.setObjectName("accept_horizontalLayout")
        spacer_item4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(spacer_item4)
        self.accept_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.accept_pushButton.setObjectName("accept_pushButton")
        self.accept_pushButton.clicked.connect(self.accept)
        self.accept_horizontalLayout.addWidget(self.accept_pushButton)
        spacer_item5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.accept_horizontalLayout.addItem(spacer_item5)
        self.accept_horizontalLayout.setStretch(0, 1)
        self.accept_horizontalLayout.setStretch(1, 1)
        self.accept_horizontalLayout.setStretch(2, 1)
        self.main_gridLayout.addLayout(self.accept_horizontalLayout, 5, 0, 1, 1)
        spacer_item6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_gridLayout.addItem(spacer_item6, 4, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        spacer_item7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.window_gridLayout.addItem(spacer_item7, 2, 0, 1, 1)
        # set button to go back
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        spacer_item8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(spacer_item8)
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        spacer_item9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navigation_horizontalLayout.addItem(spacer_item9)
        self.navigation_horizontalLayout.setStretch(0, 1)
        self.navigation_horizontalLayout.setStretch(1, 1)
        self.navigation_horizontalLayout.setStretch(2, 1)
        self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 3, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.set_remove_by_display()

    def set_remove_by_display(self):
        self.subject_id_radioButton.toggled.connect(lambda: self.remove_by_display(self.subject_id_radioButton))
        self.experimenter_name_radioButton.toggled \
            .connect(lambda: self.remove_by_display(self.experimenter_name_radioButton))

    def remove_by_display(self, btn):
        # check if one of the radio buttons was pressed
        if btn.isChecked():
            if btn.text() == "Subject id:":  # remove by subject ids case
                self.subject_ids_comboBox.setEnabled(True)
                self.experimenter_names_comboBox.setEnabled(False)
            if btn.text() == "Experimenter name:":  # remove by experimenter name case
                self.subject_ids_comboBox.setEnabled(False)
                self.experimenter_names_comboBox.setEnabled(True)

    def subject_id_click(self, index):
        self.removed_subject_id = self.subject_ids[index]
        self.removed_experimenter_name = ""

    def experimenter_name_click(self, index):
        self.removed_subject_id = ""
        self.removed_experimenter_name = self.experimenter_names[index]

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def accept(self):
        dlg = WarningDialog()
        if dlg.exec():  # ok case
            # TODO need to connect to db
            if self.removed_subject_id != "":  # remove by subject id
                pass
                self.subject_ids_comboBox.clear()
                del self.subject_ids[self.subject_ids.index(self.removed_subject_id)]
                self.subject_ids_comboBox.addItems(self.subject_ids)

            else:  # remove by experimenter name
                self.experimenter_names_comboBox.clear()
                del self.experimenter_names[self.experimenter_names.index(self.removed_experimenter_name)]
                self.experimenter_names_comboBox.addItems(self.experimenter_names)
        else:  # cancel case
            pass


    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Delete Session Template"))
        self.headline_label.setText(_translate("main", "Delete session template"))
        self.subject_id_radioButton.setText(_translate("main", "Subject id:"))
        self.experimenter_name_radioButton.setText(_translate("main", "Experimenter name:"))
        self.remove_by_label.setText(_translate("main", "Remove by:"))
        self.accept_pushButton.setText(_translate("main", "Accept"))
        self.back_pushButton.setText(_translate("main", "Back"))

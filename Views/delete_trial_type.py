from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QDialog, QDialogButtonBox, QVBoxLayout, \
    QLabel, QPushButton

from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.utils import dict_yaml_style, error_warning, get_ui_path


class WarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning")

        #q_buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        #self.buttonBox = QDialogButtonBox(q_buttons)
        #self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to remove this trial type?")
        self.layout.addWidget(message)
        #self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class DeleteTrialTypeUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = self.parent.vm
        self.vm.sessionVM.property_changed += self.EventHandler
        self.main_window = None
        self.central_widget = None
        self.window_gridLayout = None
        self.headline_label = None
        self.scrollArea = None
        self.scrollAreaWidgetContents = None
        self.gridLayout = None
        self.scroll_verticalLayout = QtWidgets.QVBoxLayout()
        self.remove_horizontalLayout = QtWidgets.QHBoxLayout()
        self.remove_pushButton = None
        self.trial_types_label = None
        self.trial_types_tableWidget = None
        self.navigation_horizontalLayout = QtWidgets.QHBoxLayout()
        self.back_pushButton = None
        self.trial_types = self.vm.get_list_trials_types_def()
        self.selected_trial_type = None
        self.trials_names = self.vm.get_trial_names()
        self.vm.property_changed += self.EventHandler
        self.is_error = False

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('delete_trial_type.ui'), main_window)

        self.back_pushButton = main_window.findChild(QPushButton, 'back_pushButton')
        self.back_pushButton.clicked.connect(self.on_back_click)
        return
        self.parent.main_window.hide()
        main_window.setObjectName("main_window")
        #main_window.resize(495, 597)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # set a headline for the window
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Arial\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.window_gridLayout.addWidget(self.headline_label, 0, 0, 1, 1)
        # set scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        #font = QtGui.QFont()
        #font.setFamily("Arial")
        #font.setPointSize(15)
        #self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 475, 386))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scroll_verticalLayout.setObjectName("scroll_verticalLayout")
        # set a remove button
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
        self.trial_types_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.trial_types_label.setObjectName("trial_types_label")
        self.scroll_verticalLayout.addWidget(self.trial_types_label)
        # set a table to hold all of the defined trial types
        self.trial_types_tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.trial_types_tableWidget.setObjectName("trial_types_tableWidget")
        # self.trial_types_tableWidget.setEditTriggers(
        #     QtWidgets.QAbstractItemView.NoEditTriggers)  # disable editing of the table TODO check this
        self.trial_types_tableWidget.setColumnCount(2)
        self.trial_types_tableWidget.setRowCount(0)
        # set headers for the table
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        self.trial_types_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Parameters")
        self.trial_types_tableWidget.setHorizontalHeaderItem(1, item)
        # set selection by rows
        #self.trial_types_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.selectRows) TODO check this
        #self.trial_types_tableWidget.setStyleSheet("font: 12pt \"Arial\";")
        # set an adaptive width for table
        #trials_table_adaptive_width = self.trial_types_tableWidget.horizontalHeader()
        #trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)
        # set the table to scroll vertically
        #self.trial_types_tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #self.trial_types_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.scroll_verticalLayout.addWidget(self.trial_types_tableWidget)
        #self.scroll_verticalLayout.setStretch(0, 1)
        #self.scroll_verticalLayout.setStretch(2, 5)
        self.gridLayout.addLayout(self.scroll_verticalLayout, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.window_gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        # set a navigation buttons
        self.navigation_horizontalLayout.setObjectName("navigation_horizontalLayout")
        #spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.navigation_horizontalLayout.addItem(spacer_item1)
        self.back_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.back_pushButton.setObjectName("back_pushButton")
        self.back_pushButton.clicked.connect(self.on_back_click)
        self.navigation_horizontalLayout.addWidget(self.back_pushButton)
        #spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.navigation_horizontalLayout.addItem(spacer_item2)
        #self.navigation_horizontalLayout.setStretch(0, 1)
        #self.navigation_horizontalLayout.setStretch(1, 1)
        #self.navigation_horizontalLayout.setStretch(2, 1)
        self.window_gridLayout.addLayout(self.navigation_horizontalLayout, 2, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.set_table()
        # self.on_row_selection_changed()

    def on_row_selection_changed(self):
        # set row selection on default
        # self.edit_trial_pushBtn.setEnabled(
        #     bool(self.trial_types_tableWidget.selectionModel().selectedRows())
        # )
        self.remove_pushButton.setEnabled(
            bool(self.trial_types_tableWidget.selectionModel().selectedRows())
        )

    def set_table(self):
        num_trial_types = len(self.trial_types)
        self.trial_types_tableWidget.setRowCount(num_trial_types)
        if num_trial_types != 0:
            for i in range(num_trial_types):
                trial_name = [*self.trial_types.keys()][i]
                self.trial_types_tableWidget.setItem(i, 0, QTableWidgetItem(trial_name))
                self.trial_types_tableWidget.setItem(i, 1,
                                                     QTableWidgetItem(dict_yaml_style(self.trial_types[trial_name])))

    def on_remove_click(self):
        dlg = WarningDialog()
        if dlg.exec():  # ok case
            is_not_empty = len(self.trial_types) > 0
            is_row_selected = self.trial_types_tableWidget.currentRow() != -1
            if is_not_empty and is_row_selected:
                # get the chosen block's row and remove it
                index = self.trial_types_tableWidget.currentRow()

                self.selected_trial_type = list(self.trial_types.keys())[index]
                if self.vm.delete_trial_type(self.selected_trial_type) == -1:  # update db
                    error_warning("trial cannot be deleted: relevant for saved session templates")
                else:
                    self.trial_types_tableWidget.removeRow(index)
                # set current row to be unselected
                self.trial_types_tableWidget.setCurrentCell(-1, self.trial_types_tableWidget.currentColumn())
            elif is_not_empty:
                error_warning("There are no trial types in the system.")
            else:
                error_warning("A trial type is not selected.")
        else:  # cancel case
            pass

    def on_back_click(self):
        if not self.is_error:
            self.parent.main_window.show()
            self.main_window.close()

    def EventHandler(self, sender, *event_args):
        if type(sender) != BehaviorSystemViewModel:
            pass
        if event_args[0][0] == "VM_delete_trial_types_error":
            error_warning("This trial type cannot be deleted since it is in templates history")
            self.is_error = True
        elif event_args[0][0] == "VM_delete_trial_types_success":
            self.is_error = False

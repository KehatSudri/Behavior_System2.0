from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableView, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt6 import QtCore, QtWidgets

from Views.add_trial import AddTrialUi
from Views.blocks_order import BlocksOrderUi
from Views.choose_template import ChooseTemplateUi

from Views.edit_trial import EditTrialUi
from Views.utils import error_warning, dict_yaml_style
from Views.random_order import RandomOrderUi


class CreateSessionUi(object):
    def __init__(self, parent):
        self.parent = parent
        self.vm = parent.vm
        self.main_window = None

        self.central_widget = None
        self.window_gridLayout = None
        self.main_gridLayout = QtWidgets.QGridLayout()

        self.headline_label = None
        self.choose_template_horizontalLayout = QtWidgets.QHBoxLayout()
        self.choose_template_pushButton = None
        self.session_name_and_date_horizontalLayout = QtWidgets.QHBoxLayout()
        self.session_name_label = None
        self.session_name_lineEdit = None
        self.date_label = None
        self.date_value_label = None
        self.subject_and_experimenter_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.subject_id_label = None
        self.subject_id_lineEdit = None
        self.experimenter_name_label = None
        self.experimenter_name_lineEdit = None
        self.trials_gridLayout = QtWidgets.QGridLayout()
        self.trials_tableWidget = None
        self.trials_label = None
        self.def_trial_horizontalLayout = QtWidgets.QHBoxLayout()
        self.order_horizontalLayout = QtWidgets.QHBoxLayout()
        self.trials_order_label = None
        self.trials_order_comboBox = None
        self.buttons_to_set_trial_horizontalLayout = QtWidgets.QHBoxLayout()
        self.add_trial_pushButton = None
        self.edit_trial_pushButton = None
        self.remove_trial_pushButton = None
        self.iti_and_end_def_gridLayout = QtWidgets.QGridLayout()
        self.navigation_gridLayout = QtWidgets.QGridLayout()
        self.next_pushBtn = None
        self.back_pushBtn = None
        self.iti_min_max_values_gridLayout = QtWidgets.QGridLayout()
        self.max_iti_spinBox = None
        self.min_iti_spinBox = None
        self.min_iti_label = None
        self.max_iti_spinBox = None
        self.min_iti_spinBox = None
        self.max_iti_label = None
        self.behaviors_comboBox = None
        self.end_def_value_horizontalLayout = QtWidgets.QHBoxLayout()
        # self.end_by_label = None
        self.end_def_spinBox = None
        self.end_def_comboBox = None
        self.end_def_label = None
        self.iti_label = None
        self.iti_def_horizontalLayout = QtWidgets.QHBoxLayout()
        self.behavior_iti_radioBtn = None
        self.random_iti_radioBtn = None
        self.random_reward_percent_horizontalLayout = QtWidgets.QHBoxLayout()
        self.random_reward_percent_label = None
        self.random_reward_percent_spinBox = None

        self.chosen_behavior = self.vm.get_behaviors_list()[0]
        self.chosen_end_def = None
        self.chosen_iti_type = None
        self.trials_ord_window = None
        #
        self.behavior_iti_widgets = None
        self.random_iti_widgets = None

        self.trial_types = self.vm.get_list_trials_types_def()
        self.trials_in_session = []  # holds all the trials in the current session
        self.selected_trial = -1  # holds the trial that the user tap on the table

        # Set a function pointer to update the table when a new trial is add
        # self.set_trials_table_pointer

        # Set a function pointer to update the table when a new trial is add
        self.set_trials_table_pointer = self.set_trials_table
        # disable editing of the table
        # self.trials_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.set_trials_table_pointer()

        # random order elements
        self.percentages = []
        self.total_num = 0
        # blocks order elements
        self.blocks_ord = []
        self.block_list = []
        self.percent_per_block = []
        self.block_sizes = []
        # VM
        # self.vm = sysVM
        self.vm.sessionVM.trials_order = "random"
        # self.iti_behaviors = sysVM.get_behaviors_list()
        # self.end_defs = sysVM.get_end_def_list()
        self.iti_behaviors = self.vm.get_behaviors_list()
        self.end_defs = self.vm.get_end_def_list()

        self.run_session_window = None

    def setupUi(self, main_window):
        self.main_window = main_window
        self.parent.main_window.hide()
        main_window.setObjectName("main_window")
        main_window.resize(609, 650)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.window_gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.window_gridLayout.setObjectName("window_gridLayout")
        # self.main_gridLayout = QtWidgets.QGridLayout()
        self.main_gridLayout.setObjectName("main_gridLayout")
        # set an headline label
        self.headline_label = QtWidgets.QLabel(self.central_widget)
        self.headline_label.setStyleSheet("font: 55pt \"Gabriola\";")
        self.headline_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headline_label.setObjectName("headline_label")
        self.main_gridLayout.addWidget(self.headline_label, 0, 0, 1, 1)
        # add a choose template push button
        # self.choose_template_horizontalLayout = QtWidgets.QHBoxLayout()
        # self.choose_template_horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.choose_template_horizontalLayout.setContentsMargins(0, -1, 0, -1)
        # self.choose_template_horizontalLayout.setSpacing(2)
        self.choose_template_horizontalLayout.setObjectName("choose_template_horizontalLayout")
        ##spacer_item5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##self.choose_template_horizontalLayout.addItem(spacer_item5)
        # add a choose template push button
        self.choose_template_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.choose_template_pushButton.setObjectName("choose_template_pushButton")
        self.choose_template_pushButton.clicked.connect(self.on_choose_template_click)
        self.choose_template_horizontalLayout.addWidget(self.choose_template_pushButton)
        ##spacer_item6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##self.choose_template_horizontalLayout.addItem(spacer_item6)
        self.choose_template_horizontalLayout.setStretch(0, 1)
        self.choose_template_horizontalLayout.setStretch(1, 2)
        self.choose_template_horizontalLayout.setStretch(2, 1)
        self.main_gridLayout.addLayout(self.choose_template_horizontalLayout, 1, 0, 1, 1)
        # set an horizontal layout to hold session name and date of experiment
        # self.session_name_and_date_horizontalLayout = QtWidgets.QHBoxLayout()
        self.session_name_and_date_horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.session_name_and_date_horizontalLayout.setSpacing(20)
        self.session_name_and_date_horizontalLayout.setObjectName("session_name_and_date_horizontalLayout")
        self.session_name_label = QtWidgets.QLabel(self.central_widget)
        self.session_name_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.session_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.session_name_label.setObjectName("session_name_label")
        self.session_name_and_date_horizontalLayout.addWidget(self.session_name_label)
        self.session_name_lineEdit = QtWidgets.QLineEdit(self.central_widget)
        self.session_name_lineEdit.setEnabled(True)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.session_name_lineEdit.setSizePolicy(sizePolicy)
        self.session_name_lineEdit.setMinimumSize(QtCore.QSize(0, 1))
        self.session_name_lineEdit.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.session_name_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
        self.session_name_lineEdit.editingFinished.connect(self.on_session_name_edit)
        # self.session_name_textEdit.setLineWidth(1)
        # self.session_name_textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.session_name_textEdit.setTabStopWidth(80)
        self.session_name_lineEdit.setObjectName("session_name_lineEdit")
        self.session_name_and_date_horizontalLayout.addWidget(self.session_name_lineEdit)
        self.date_label = QtWidgets.QLabel(self.central_widget)
        self.date_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.date_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.session_name_and_date_horizontalLayout.addWidget(self.date_label)
        self.date_value_label = QtWidgets.QLabel(self.central_widget)
        self.date_value_label.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.date_value_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.date_value_label.setObjectName("date_value_label")
        self.date_value_label.setText((datetime.now()).strftime("%d/%m/%Y"))
        self.session_name_and_date_horizontalLayout.addWidget(self.date_value_label)
        self.session_name_and_date_horizontalLayout.setStretch(0, 1)
        self.session_name_and_date_horizontalLayout.setStretch(1, 1)
        self.session_name_and_date_horizontalLayout.setStretch(2, 1)
        self.session_name_and_date_horizontalLayout.setStretch(3, 1)
        self.main_gridLayout.addLayout(self.session_name_and_date_horizontalLayout, 2, 0, 1, 1)
        # set an horizontal layout to hold the subject id and experimenter name
        # self.subject_and_experimenter_name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.subject_and_experimenter_name_horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.subject_and_experimenter_name_horizontalLayout.setSpacing(20)
        self.subject_and_experimenter_name_horizontalLayout.setObjectName(
            "subject_and_experimenter_name_horizontalLayout")

        self.subject_id_label = QtWidgets.QLabel(self.central_widget)
        self.subject_id_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.subject_id_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subject_id_label.setObjectName("subject_id_label")
        self.subject_and_experimenter_name_horizontalLayout.addWidget(self.subject_id_label)
        self.subject_id_lineEdit = QtWidgets.QLineEdit(self.central_widget)
        self.subject_id_lineEdit.setEnabled(True)
        self.subject_id_lineEdit.editingFinished.connect(self.on_subject_id_edit)

        self.subject_id_lineEdit.setMinimumSize(QtCore.QSize(0, 1))
        self.subject_id_lineEdit.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.subject_id_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)

        self.subject_id_lineEdit.setObjectName("subject_id_lineEdit")
        self.subject_and_experimenter_name_horizontalLayout.addWidget(self.subject_id_lineEdit)
        self.experimenter_name_label = QtWidgets.QLabel(self.central_widget)
        self.experimenter_name_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.experimenter_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.experimenter_name_label.setObjectName("experimenter_name_label")
        self.subject_and_experimenter_name_horizontalLayout.addWidget(self.experimenter_name_label)
        self.experimenter_name_lineEdit = QtWidgets.QLineEdit(self.central_widget)
        self.experimenter_name_lineEdit.setEnabled(True)
        self.experimenter_name_lineEdit.editingFinished.connect(self.on_experimenter_name_edit)

        self.experimenter_name_lineEdit.setMinimumSize(QtCore.QSize(0, 1))
        self.experimenter_name_lineEdit.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.experimenter_name_lineEdit.setInputMethodHints(QtCore.Qt.ImhLatinOnly)

        self.experimenter_name_lineEdit.setObjectName("experimenter_name_lineEdit")
        self.subject_and_experimenter_name_horizontalLayout.addWidget(self.experimenter_name_lineEdit)
        self.subject_and_experimenter_name_horizontalLayout.setStretch(0, 1)
        self.subject_and_experimenter_name_horizontalLayout.setStretch(1, 1)
        self.subject_and_experimenter_name_horizontalLayout.setStretch(2, 1)
        self.subject_and_experimenter_name_horizontalLayout.setStretch(3, 1)
        self.main_gridLayout.addLayout(self.subject_and_experimenter_name_horizontalLayout, 3, 0, 1, 1)

        # set a grid layout to hold the trials in the session in a table
        self.trials_gridLayout.setObjectName("trials_gridLayout")
        self.trials_tableWidget = QtWidgets.QTableWidget(self.central_widget)
        ##self.trials_tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        ##self.trials_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.trials_tableWidget.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.trials_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.trials_tableWidget.setColumnCount(2)
        self.trials_tableWidget.setObjectName("trials_tableWidget")
        self.trials_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.trials_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trials_tableWidget.setHorizontalHeaderItem(1, item)
        self.trials_gridLayout.addWidget(self.trials_tableWidget, 1, 0, 1, 1)
        self.trials_label = QtWidgets.QLabel(self.central_widget)
        self.trials_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.trials_label.setObjectName("trials_label")
        self.trials_gridLayout.addWidget(self.trials_label, 0, 0, 1, 1)
        self.trials_gridLayout.setColumnStretch(0, 1)
        self.trials_gridLayout.setRowStretch(1, 10)
        self.main_gridLayout.addLayout(self.trials_gridLayout, 4, 0, 1, 1)
        # set an horizontal layout to hold the definitions for a trial and handle one
        ##self.def_trial_horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.def_trial_horizontalLayout.setContentsMargins(20, 10, 20, 0)
        self.def_trial_horizontalLayout.setSpacing(20)
        self.def_trial_horizontalLayout.setObjectName("def_trial_horizontalLayout")

        self.order_horizontalLayout.setSpacing(5)
        self.order_horizontalLayout.setObjectName("order_horizontalLayout")
        self.trials_order_label = QtWidgets.QLabel(self.central_widget)

        self.trials_order_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.trials_order_label.setObjectName("trials_order_label")
        self.order_horizontalLayout.addWidget(self.trials_order_label)
        self.trials_order_comboBox = QtWidgets.QComboBox(self.central_widget)
        self.trials_order_comboBox.setObjectName("trials_order_comboBox")
        self.trials_order_comboBox.addItems(["random", "blocks"])
        self.trials_order_comboBox.activated.connect(self.order_click)
        self.order_horizontalLayout.addWidget(self.trials_order_comboBox)
        self.order_horizontalLayout.setStretch(0, 1)
        self.order_horizontalLayout.setStretch(1, 1)
        self.def_trial_horizontalLayout.addLayout(self.order_horizontalLayout)
        ##spacer_item4 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        ##self.def_trial_horizontalLayout.addItem(spacer_item4)

        ##self.buttons_to_set_trial_horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttons_to_set_trial_horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.buttons_to_set_trial_horizontalLayout.setSpacing(2)
        self.buttons_to_set_trial_horizontalLayout.setObjectName("buttons_to_set_trial_horizontalLayout")
        self.add_trial_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.add_trial_pushButton.setIconSize(QtCore.QSize(16, 16))
        self.add_trial_pushButton.setObjectName("add_trial_pushButton")
        self.add_trial_pushButton.clicked.connect(self.on_add_click)
        self.buttons_to_set_trial_horizontalLayout.addWidget(self.add_trial_pushButton)
        self.edit_trial_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.edit_trial_pushButton.setObjectName("edit_trial_pushButton")
        self.edit_trial_pushButton.clicked.connect(self.on_edit_click)
        self.buttons_to_set_trial_horizontalLayout.addWidget(self.edit_trial_pushButton)
        self.remove_trial_pushButton = QtWidgets.QPushButton(self.central_widget)
        self.remove_trial_pushButton.setObjectName("remove_trial_pushButton")
        self.remove_trial_pushButton.clicked.connect(self.on_remove_click)
        self.buttons_to_set_trial_horizontalLayout.addWidget(self.remove_trial_pushButton)
        self.def_trial_horizontalLayout.addLayout(self.buttons_to_set_trial_horizontalLayout)
        self.def_trial_horizontalLayout.setStretch(0, 1)
        self.def_trial_horizontalLayout.setStretch(1, 1)
        self.def_trial_horizontalLayout.setStretch(2, 1)
        self.main_gridLayout.addLayout(self.def_trial_horizontalLayout, 5, 0, 1, 1)
        # set a gridlayout to hold the iti and end definition and navigation buttons
        self.iti_and_end_def_gridLayout.setObjectName("iti_and_end_def_gridLayout")
        ##spacer_item = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        ##self.iti_and_end_def_gridLayout.addItem(spacer_item, 0, 4, 1, 1)

        self.navigation_gridLayout.setObjectName("navigation_gridLayout")
        self.next_pushBtn = QtWidgets.QPushButton(self.central_widget)
        self.next_pushBtn.setObjectName("next_pushBtn")
        self.next_pushBtn.clicked.connect(self.on_next_click)
        self.navigation_gridLayout.addWidget(self.next_pushBtn, 0, 1, 1, 1)
        self.back_pushBtn = QtWidgets.QPushButton(self.central_widget)
        self.back_pushBtn.clicked.connect(self.on_back_click)
        self.back_pushBtn.setObjectName("back_pushBtn")
        self.navigation_gridLayout.addWidget(self.back_pushBtn, 0, 0, 1, 1)
        self.navigation_gridLayout.setColumnStretch(0, 1)
        self.navigation_gridLayout.setColumnStretch(1, 1)
        self.iti_and_end_def_gridLayout.addLayout(self.navigation_gridLayout, 5, 1, 1, 3)
        ##spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        ##self.iti_and_end_def_gridLayout.addItem(spacer_item1, 4, 1, 1, 1)
        ##spacer_item2 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        ##self.iti_and_end_def_gridLayout.addItem(spacer_item2, 0, 0, 1, 1)

        self.iti_min_max_values_gridLayout.setObjectName("iti_min_max_values_gridLayout")
        self.min_iti_label = QtWidgets.QLabel(self.central_widget)
        self.min_iti_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.min_iti_label.setObjectName("min_iti_label")
        self.iti_min_max_values_gridLayout.addWidget(self.min_iti_label, 2, 0, 1, 1)
        self.max_iti_spinBox = QtWidgets.QSpinBox(self.central_widget)
        self.max_iti_spinBox.setObjectName("max_iti_spinBox")
        self.max_iti_spinBox.valueChanged.connect(self.get_max_iti)
        self.max_iti_spinBox.setMaximum(100000)
        self.iti_min_max_values_gridLayout.addWidget(self.max_iti_spinBox, 4, 1, 1, 1)
        self.min_iti_spinBox = QtWidgets.QSpinBox(self.central_widget)
        self.min_iti_spinBox.setObjectName("min_iti_spinBox")
        self.min_iti_spinBox.valueChanged.connect(self.get_min_iti)
        self.min_iti_spinBox.setMaximum(100000)
        self.iti_min_max_values_gridLayout.addWidget(self.min_iti_spinBox, 2, 1, 1, 1)
        self.max_iti_label = QtWidgets.QLabel(self.central_widget)
        self.max_iti_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.max_iti_label.setObjectName("max_iti_label")
        self.iti_min_max_values_gridLayout.addWidget(self.max_iti_label, 4, 0, 1, 1)
        self.behaviors_comboBox = QtWidgets.QComboBox(self.central_widget)
        self.behaviors_comboBox.setObjectName("behaviors_comboBox")
        self.behaviors_comboBox.addItems(self.iti_behaviors)
        self.behaviors_comboBox.activated.connect(self.iti_behavior_click)
        self.iti_min_max_values_gridLayout.addWidget(self.behaviors_comboBox, 0, 0, 1, 2)
        self.iti_and_end_def_gridLayout.addLayout(self.iti_min_max_values_gridLayout, 2, 1, 2, 1)

        self.end_def_value_horizontalLayout.setObjectName("end_def_value_horizontalLayout")
        # self.end_by_label = QtWidgets.QLabel(self.central_widget)
        # self.end_by_label.setStyleSheet("font: 12pt \"Gabriola\";")
        # self.end_by_label.setObjectName("end_by_label")
        # self.end_def_value_horizontalLayout.addWidget(self.end_by_label)
        self.end_def_spinBox = QtWidgets.QSpinBox(self.central_widget)
        self.end_def_spinBox.setObjectName("end_def_spinBox")
        self.end_def_spinBox.valueChanged.connect(self.get_end_def)
        self.end_def_spinBox.setMaximum(100000)
        self.end_def_value_horizontalLayout.addWidget(self.end_def_spinBox)
        self.iti_and_end_def_gridLayout.addLayout(self.end_def_value_horizontalLayout, 2, 3, 1, 1)
        self.end_def_comboBox = QtWidgets.QComboBox(self.central_widget)
        self.end_def_comboBox.setObjectName("end_def_comboBox")
        self.end_def_comboBox.addItems(self.end_defs)
        # self.end_by_label.setText(self.end_defs[0])
        # self.end_def_comboBox.activated.connect(self.end_by_click)
        self.iti_and_end_def_gridLayout.addWidget(self.end_def_comboBox, 1, 3, 1, 1)
        self.end_def_label = QtWidgets.QLabel(self.central_widget)
        self.end_def_label.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.end_def_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.end_def_label.setObjectName("end_def_label")
        self.iti_and_end_def_gridLayout.addWidget(self.end_def_label, 0, 3, 1, 1)
        self.iti_label = QtWidgets.QLabel(self.central_widget)
        self.iti_label.setStyleSheet("font: 12pt \"Gabriola\";")
        ##self.iti_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.iti_label.setObjectName("iti_label")
        self.iti_and_end_def_gridLayout.addWidget(self.iti_label, 0, 1, 1, 1)

        self.iti_def_horizontalLayout.setObjectName("iti_def_horizontalLayout")
        self.behavior_iti_radioBtn = QtWidgets.QRadioButton(self.central_widget)
        self.behavior_iti_radioBtn.setStyleSheet("font: 12pt \"Gabriola\";")
        self.behavior_iti_radioBtn.setObjectName("behavior_iti_radioBtn")
        self.iti_def_horizontalLayout.addWidget(self.behavior_iti_radioBtn)
        self.random_iti_radioBtn = QtWidgets.QRadioButton(self.central_widget)
        self.random_iti_radioBtn.setStyleSheet("font: 12pt \"Gabriola\";")
        self.random_iti_radioBtn.setObjectName("random_iti_radioBtn")
        self.iti_def_horizontalLayout.addWidget(self.random_iti_radioBtn)
        self.iti_and_end_def_gridLayout.addLayout(self.iti_def_horizontalLayout, 1, 1, 1, 1)
        ##spacer_item3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##self.iti_and_end_def_gridLayout.addItem(spacer_item3, 0, 2, 1, 1)

        self.random_reward_percent_horizontalLayout.setObjectName("random_reward_percent_horizontalLayout")
        self.random_reward_percent_label = QtWidgets.QLabel(self.central_widget)
        self.random_reward_percent_label.setStyleSheet("font: 12pt \"Gabriola\";")
        self.random_reward_percent_label.setObjectName("random_reward_percent_label")
        self.random_reward_percent_horizontalLayout.addWidget(self.random_reward_percent_label)
        self.random_reward_percent_spinBox = QtWidgets.QSpinBox(self.central_widget)
        self.random_reward_percent_spinBox.setObjectName("random_reward_percent_spinBox")
        self.random_reward_percent_horizontalLayout.addWidget(self.random_reward_percent_spinBox)
        self.random_reward_percent_horizontalLayout.setStretch(0, 1)
        self.random_reward_percent_horizontalLayout.setStretch(1, 1)
        self.iti_and_end_def_gridLayout.addLayout(self.random_reward_percent_horizontalLayout, 3, 3, 1, 1)
        self.iti_and_end_def_gridLayout.setColumnStretch(0, 2)
        self.iti_and_end_def_gridLayout.setColumnStretch(1, 2)
        self.iti_and_end_def_gridLayout.setColumnStretch(2, 1)
        self.iti_and_end_def_gridLayout.setColumnStretch(3, 2)
        self.iti_and_end_def_gridLayout.setColumnStretch(4, 2)
        self.main_gridLayout.addLayout(self.iti_and_end_def_gridLayout, 6, 0, 1, 1)

        self.main_gridLayout.setRowStretch(0, 1)
        self.main_gridLayout.setRowStretch(1, 1)
        self.main_gridLayout.setRowStretch(2, 1)
        self.main_gridLayout.setRowStretch(3, 1)
        self.main_gridLayout.setRowStretch(4, 10)
        self.main_gridLayout.setRowStretch(5, 1)
        self.main_gridLayout.setRowStretch(6, 1)
        self.window_gridLayout.addLayout(self.main_gridLayout, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        # save widgets for parameters to define for each iti option
        self.behavior_iti_widgets = [self.behaviors_comboBox]
        self.random_iti_widgets = [self.min_iti_spinBox, self.max_iti_spinBox,
                                   self.min_iti_label, self.max_iti_label]

        # disable editing of the table
        ##self.trials_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.set_trials_table_pointer()
        #
        ##self.trials_tableWidget.setSelectionBehavior(QTableView.SelectRows)
        # hide all the iti widgets for default
        self.hide_show_iti_def(True, 0)
        # define a connection for each option to define an iti
        self.iti_cfg()

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def on_choose_template_click(self):
        self.choose_template_window = QtWidgets.QDialog()
        self.choose_template_ui = ChooseTemplateUi(self)
        self.choose_template_ui.setupUi(self.choose_template_window)
        self.choose_template_window.show()
        # self.second_window_ui = ChooseTemplateUi(self)
        # self.second_window_ui.setupUi(self.second_window)
        # self.second_window.show()

    def on_add_click(self):
        self.add_window = QtWidgets.QDialog()
        self.add_ui = AddTrialUi(self)
        self.add_ui.setupUi(self.add_window)
        self.add_window.show()
        # self.second_window_ui = AddTrialUi(self)
        # self.second_window_ui.setupUi(self.second_window)
        # self.second_window.show()

    def deal_with_trial(self, treatment):
        is_not_empty = len(self.trials_in_session) > 0
        is_row_selected = self.trials_tableWidget.currentRow() != -1
        # check if there are trials and a trial was selected
        if is_not_empty and is_row_selected:
            if treatment == 0:  # edit case
                self.edit_window = QtWidgets.QDialog()
                self.edit_ui = EditTrialUi(self)
                self.edit_ui.setupUi(self.edit_window)
                self.edit_window.show()
                # self.second_window_ui = EditTrialUi(self)
                # self.second_window_ui.setupUi(self.second_window)
                # self.second_window.show()
            else:  # remove case
                # get the chosen block's row and remove it
                index = self.trials_tableWidget.currentRow()  # ignore 0th which represents blocks parameters
                del self.trials_in_session[index]
                self.trials_tableWidget.removeRow(index)
                # set current row to be unselected
                self.trials_tableWidget.setCurrentCell(-1, self.trials_tableWidget.currentColumn())

                # chosen_row = self.trials_tableWidget.currentRow()
                # self.trials_tableWidget.removeRow(chosen_row)
                # if len(self.percentages) != 0:
                del self.percentages[index]
                # else:
                del self.percent_per_block[index]
                # del self.trials_in_session[self.trials_tableWidget.currentRow()]
                # self.trials_tableWidget.removeRow(self.trials_tableWidget.currentRow())
                # if len(self.percentages)!=0:
                #     del self.percentages[self.trials_tableWidget.currentRow()]
                # else:
                #     del self.prcnt_per_block[self.trials_tableWidget.currentRow()]
                # for i in range(len(self.block_list)):
                #     del self.prcnt_per_block[i][self.trials_tableWidget.currentRow()] #TODO CHACK THIS
        elif is_not_empty:
            error_warning("A trial is not selected.")
        else:
            error_warning("There are no trials in the current session.")

    def on_edit_click(self):
        self.deal_with_trial(0)

    def on_remove_click(self):
        self.deal_with_trial(1)

    def on_row_selection_changed(self):
        # set row selection on default
        self.edit_trial_pushBtn.setEnabled(
            bool(self.trials_tableWidget.selectionModel().selectedRows())
        )
        self.remove_trial_pushBtn.setEnabled(
            bool(self.trials_tableWidget.selectionModel().selectedRows())
        )

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.trials_tableWidget.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def iti_cfg(self):
        self.behavior_iti_radioBtn.toggled.connect(lambda: self.iti_state(self.behavior_iti_radioBtn))
        self.random_iti_radioBtn.toggled.connect(lambda: self.iti_state(self.random_iti_radioBtn))

    def iti_state(self, btn):
        # check if one of the radio buttons was pressed
        # 1 represents behavior chosen
        # 2 represents random chosen
        if btn.isChecked():
            if btn.text() == "behavior":
                self.hide_show_iti_def(False, 1)
            if btn.text() == "random":
                self.hide_show_iti_def(False, 2)
            self.chosen_iti_type = btn.text()

    def hide_show_iti_def(self, to_hide: bool, flag: int):
        widgets = []
        other_widgets = []
        if flag == 0:
            widgets = self.behavior_iti_widgets + self.random_iti_widgets
        elif flag == 1:
            widgets = self.behavior_iti_widgets
            other_widgets = self.random_iti_widgets
        else:
            widgets = self.random_iti_widgets
            other_widgets = self.behavior_iti_widgets
        for w in widgets:
            if to_hide:
                w.hide()
            else:
                w.show()
        for w in other_widgets:
            if to_hide:
                w.show()
            else:
                w.hide()

    def is_valid_input(self):
        is_session_name_empty = len(self.session_name_lineEdit.text()) == 0  # check session name
        is_subject_id_empty = len(self.subject_id_lineEdit.text()) == 0  # check subject id
        is_experimenter_name_empty = len(self.experimenter_name_lineEdit.text()) == 0  # check experimenter name
        is_iti_empty = False
        if self.chosen_iti_type == "random":
            is_iti_empty = self.max_iti_spinBox.value() == 0 or self.min_iti_spinBox.value() == 0  # check iti value
            if self.max_iti_spinBox.value() < self.min_iti_spinBox.value():
                return False
        is_end_def_empty = self.end_def_spinBox.value() == 0  # check end definition value
        # is_random_reward_empty = self.random_reward_percent_spinBox.value() == 0  # check random reward percent
        if is_session_name_empty or is_subject_id_empty or is_experimenter_name_empty or is_iti_empty or \
                is_end_def_empty or is_end_def_empty:
            return False
        return True

    def set_vm_data(self):
        min_iti, max_iti, iti_behavior = None, None, None
        # get trials order
        # order = self.vm.sessionVM.trials_order
        iti_type = self.chosen_iti_type
        if iti_type == "random":
            # get value  accordingly - min,max for random, description for behavior
            min_iti = self.min_iti_spinBox.value()
            max_iti = self.max_iti_spinBox.value()
        else:
            iti_behavior = self.chosen_behavior
        # get end def, description and value
        end_def_val = self.end_def_spinBox.value()
        # end_def_description = self.chosen_end_def
        end_def_description = self.end_def_comboBox.currentText()
        # list of trials with parameters
        # trials = self.trials_in_session
        self.vm.set_iti(iti_type, min_iti, max_iti, iti_behavior)
        self.vm.set_end_def(end_def_description, end_def_val)
        self.vm.curr_session.rnd_reward_percent = self.random_reward_percent_spinBox.value()

        # self.vm.set_trials_list(trials) NOT RELEVANT AT THIS PART

    def on_next_click(self):
        if not self.is_valid_input():
            if self.max_iti_spinBox.value() < self.min_iti_spinBox.value():
                error_warning("An error accrued, please choose a valid iti range.")
                return
            error_warning("An error accrued, please try again.")
            return
        self.set_vm_data()
        order = self.vm.sessionVM.trials_order
        # if self.trials_ord_window is None:
        if order == "random":
            self.trials_ord_window = QtWidgets.QDialog()
            self.trials_ord_window_ui = RandomOrderUi(self)
            self.trials_ord_window_ui.setupUi(self.trials_ord_window)
        else:
            self.trials_ord_window = QtWidgets.QDialog()
            self.trials_ord_window_ui = BlocksOrderUi(self)
            self.trials_ord_window_ui.setupUi(self.trials_ord_window)
        self.trials_ord_window.show()

    def on_session_name_edit(self):
        session_name = self.session_name_lineEdit.text()
        self.vm.sessionVM.session_name = session_name

    def on_subject_id_edit(self):
        subject_id = self.subject_id_lineEdit.text()
        self.vm.sessionVM.subject_id = subject_id

    def on_experimenter_name_edit(self):
        experimenter_name = self.experimenter_name_lineEdit.text()
        self.vm.sessionVM.experimenter_name = experimenter_name

    def get_min_iti(self):
        min_iti = self.min_iti_spinBox.value()

    def get_max_iti(self):
        max_iti = self.max_iti_spinBox.value()

    def get_end_def(self):
        end_def = self.end_def_spinBox.value()

    def iti_behavior_click(self, index):
        self.chosen_behavior = self.iti_behaviors[index]

    # def end_by_click(self, index):
    #     # TODO: need to check ending behaviors and theirs definition
    #     if index == 0:
    #         self.end_by_label.setText("A")
    #     elif index == 1:
    #         self.end_by_label.setText("B")
    #     else:
    #         self.end_by_label.setText("C")
    #     self.chosen_end_def = self.vm.get_end_def_list()[index]

    def order_click(self, index):
        if index == 0:
            order = "random"
        else:
            order = "blocks"
        self.vm.sessionVM.trials_order = order

    def set_trials_table(self):
        self.trials_tableWidget.setRowCount(len(self.trials_in_session))
        # edit case
        if self.selected_trial >= 0:  # edit case
            self.selected_trial = -1
            row = self.trials_tableWidget.currentRow()
            new_values = self.trials_in_session[len(self.trials_in_session) - 1]
            # trial_name = [*new_values.keys()][0]
            self.trials_in_session[row] = new_values
            self.trials_tableWidget.setRowCount(len(self.trials_in_session))
            self.trials_tableWidget.setItem(row, 1,
                                            QTableWidgetItem(dict_yaml_style(self.trials_in_session[row])))
        else:  # add case
            num_trials = len(self.trials_in_session)
            if num_trials != 0:
                trial_name = [*self.trials_in_session[-1].keys()][0]
                self.trials_tableWidget.setItem(num_trials - 1, 0, QTableWidgetItem(trial_name))
                # self.trials_tableWidget.setItem(num_trials - 1, 1,
                #                                 QTableWidgetItem(
                #                                     str(self.trials_in_session[num_trials - 1][trial_name])))
                self.trials_tableWidget.setItem(num_trials - 1, 1,
                                                QTableWidgetItem(dict_yaml_style(
                                                    self.trials_in_session[num_trials - 1][trial_name])))
        # Set an adaptive width for table
        trials_table_adaptive_width = self.trials_tableWidget.horizontalHeader()
        ##trials_table_adaptive_width.setSectionResizeMode(QHeaderView.Stretch)

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Create a new session"))
        self.subject_id_label.setText(_translate("main", "Subject ID: "))
        self.subject_id_lineEdit.setToolTip(_translate("main",
                                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                       "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style "
                                                       "type=\"text/css\">\n "
                                                       "p, li { white-space: pre-wrap; }\n"
                                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; "
                                                       "font-size:8pt; font-weight:400; font-style:normal;\">\n "
                                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                       "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                       "-qt-block-indent:0; text-indent:0px;\"><br "
                                                       "/></p></body></html>"))
        self.experimenter_name_label.setText(_translate("main", "Experimenter name:"))
        self.experimenter_name_lineEdit.setToolTip(_translate("main",
                                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                              "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                              "<html><head><meta name=\"qrichtext\" content=\"1\" "
                                                              "/><style type=\"text/css\">\n "
                                                              "p, li { white-space: pre-wrap; }\n"
                                                              "</style></head><body style=\" font-family:\'MS Shell "
                                                              "Dlg 2\'; font-size:8pt; font-weight:400; "
                                                              "font-style:normal;\">\n "
                                                              "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                              "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                              "-qt-block-indent:0; text-indent:0px;\"><br "
                                                              "/></p></body></html>"))
        self.session_name_label.setText(_translate("main", "Session name:"))
        self.session_name_lineEdit.setToolTip(_translate("main",
                                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                         "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style "
                                                         "type=\"text/css\">\n "
                                                         "p, li { white-space: pre-wrap; }\n"
                                                         "</style></head><body style=\" font-family:\'MS Shell Dlg "
                                                         "2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n "
                                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                         "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                         "-qt-block-indent:0; text-indent:0px;\"><br "
                                                         "/></p></body></html>"))
        self.date_label.setText(_translate("main", "Date:"))
        # self.date_value_label.setText(_translate("main", "self.date_value_label"))
        item = self.trials_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("main", "type"))
        item = self.trials_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("main", "parameters"))
        self.trials_label.setText(_translate("main", "Trials: "))
        self.headline_label.setText(_translate("main", "Create a session"))
        self.next_pushBtn.setText(_translate("main", "Next"))
        self.back_pushBtn.setText(_translate("main", "Back"))
        self.min_iti_label.setText(_translate("main", "min: "))
        self.max_iti_label.setText(_translate("main", "max: "))
        self.end_def_label.setText(_translate("main", "End definition:"))
        self.iti_label.setText(_translate("main", "ITI:"))
        self.behavior_iti_radioBtn.setText(_translate("main", "behavior"))
        self.random_iti_radioBtn.setText(_translate("main", "random"))
        self.random_reward_percent_label.setText(_translate("main", "Random reward percent"))
        self.trials_order_label.setText(_translate("main", "Order:"))
        self.add_trial_pushButton.setText(_translate("main", "Add"))
        self.edit_trial_pushButton.setText(_translate("main", "Edit"))
        self.remove_trial_pushButton.setText(_translate("main", "Remove"))
        self.choose_template_pushButton.setText(_translate("main", "Choose Template"))

    def parse_trial_params(self, trials):
        trials_names, trials_params = [], []
        for trial in trials:
            pair = [(keys, val) for keys, val in trial.items()]
            name = [i[0] for i in pair]
            param = [i[1] for i in pair]
            trials_names += name
            trials_params.append(param)
        return trials_names, trials_params
    # def dict_str_style(self, d):
    #     d_casting_int = self.get_string_dict(d)
    #
    #     result = yaml.dump(d_casting_int, sort_keys=False, default_flow_style=False, default_style='')
    #     return result
    #
    # def get_string_dict(self, d):
    #     cast_str = lambda x: int(x) if x.isnumeric() else x
    #     d_casting_int = {}
    #     for outer_k, outer_v in d.items():
    #         d_casting_int[outer_k] = {}
    #         for param, value in outer_v.items():
    #             d_casting_int[outer_k][param] = cast_str(value)
    #     return d_casting_int

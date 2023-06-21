from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QPushButton
from Views.utils import get_ui_path, error_warning
from Models.DB_INIT import DB


class removeEventUi(object):
    def __init__(self, parent):
        self.db = None
        self.main_window = None
        self.table = None
        self.parent = parent
        self.events = []

    def setupUi(self, main_window):
        self.main_window = main_window
        uic.loadUi(get_ui_path('removeEvent.ui'), main_window)
        back_pushButton = main_window.findChild(QPushButton, 'back_pushButton')
        back_pushButton.clicked.connect(self.on_back_click)
        self.table = main_window.findChild(QtWidgets.QTableWidget, 'events_table')
        self.db = DB()
        self.events = self.db.get_hardware_events()
        for row, data in enumerate([t[1] for t in self.events]):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(data))
        remove_pushButton = main_window.findChild(QPushButton, 'remove_pushButton')
        remove_pushButton.clicked.connect(self.on_remove_click)

    def on_back_click(self):
        self.parent.main_window.show()
        self.main_window.close()

    def on_remove_click(self):
        is_not_empty = len(self.events) > 0
        chosen_row = self.table.currentRow()
        is_row_selected = chosen_row != -1
        if is_not_empty and is_row_selected:
            item = self.table.item(chosen_row, 0)
            self.db.remove_event(item.text())
            del self.events[chosen_row]
            self.table.removeRow(chosen_row)
        elif is_not_empty:
            error_warning("Please select an event.")
        else:
            error_warning("There are no events in the system.")

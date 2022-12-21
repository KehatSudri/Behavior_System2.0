import sys
from PyQt6 import QtWidgets
from Models.Behavior_System_Model import BehaviorSystemModel
from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.create_session import CreateSessionUi #this will be deleted as starting window would be different
from Views.system_main import SystemMainUi

if __name__ == "__main__":
    systemM = BehaviorSystemModel()  # maybe should give path to DB connection file
    systemVM = BehaviorSystemViewModel(systemM)
    systemVM.connect_to_DB()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SystemMainUi()
    ui.setupUi(MainWindow, systemVM)
    MainWindow.show()
    sys.exit(app.exec())

import sys
from PyQt6 import QtWidgets
from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Views.system_main import SystemMainUi

if __name__ == "__main__":
    try:
        systemVM = BehaviorSystemViewModel()
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        mainUi = SystemMainUi()
        mainUi.setupUi(mainWindow, systemVM)
        mainWindow.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An error occurred: {e}")

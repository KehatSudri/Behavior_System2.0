

if __name__ == "__main__":
    # import machine
    # import time
    #
    # # for i in range(5):
    # #     led.value(1)
    # #     time.sleep(1)
    # #     led.value(0)
    # #     time.sleep(1)
    # import serial
    #
    # arduino = serial.Serial(port='COM3', baudrate=115200)
    # led = machine.Pin(2, machine.Pin.OUT)
    # while True:
    #     for i in range(5):
    #         led.value(1)
    #         time.sleep(1)
    #         led.value(0)
    #         time.sleep(1)
    import sys
    from PyQt5 import QtWidgets
    from Models.Behavior_System_Model import BehaviorSystemModel
    from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
    from Views.create_session import CreateSessionUi  # this will be deleted as starting window would be different
    systemM = BehaviorSystemModel()  # maybe should give path to DB connection file
    systemVM = BehaviorSystemViewModel(systemM)
    systemVM.connect_to_DB()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CreateSessionUi()
    ui.setupUi(MainWindow, systemVM)
    MainWindow.show()
    sys.exit(app.exec_())

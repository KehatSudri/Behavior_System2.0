from Models.Event import Event


class INotifyPropertyChanged:
    def __init__(self):
        self.property_changed = Event()

    def notifyPropertyChanged(self, propName):
        if self.property_changed is not None:
            self.property_changed(self, [propName])

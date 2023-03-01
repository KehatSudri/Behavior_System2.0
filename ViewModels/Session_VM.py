from Models.INotifyPropertyChanged import INotifyPropertyChanged
from Models.Session_Model import SessionModel


class SessionViewModel(INotifyPropertyChanged):
    def __init__(self):
        super(SessionViewModel, self).__init__()
        self.model = SessionModel()

    def start_session(self):
        self.model.start()

    def pause_session(self):
        self.model.pause()

    def resume_session(self):
        self.model.resume()

    def finish_session(self):
        self.model.finish()

    @property
    def trial_types_successive_counter(self):
        return self.model.trial_types_successive_counter

    @trial_types_successive_counter.setter
    def trial_types_successive_counter(self, value):
        self.model.trial_types_successive_counter = value

    @property
    def trial_types_total_counter(self):
        return self.model.trial_types_total_counter

    @trial_types_total_counter.setter
    def trial_types_total_counter(self, value):
        self.model.trial_types_total_counter = value

    @property
    def session_id(self):
        return self.model.session_id

    @session_id.setter
    def session_id(self, value):
        self.model.session_id = value

    @property
    def subject_id(self):
        return self.model.subject_id

    @subject_id.setter
    def subject_id(self, value):
        self.model.subject_id = value

    @property
    def end_session(self):
        return self.model.end_session

    @end_session.setter
    def end_session(self, value):
        self.model.end_session = value

    @property
    def trials_def(self):
        return self.model.trials_def

    @trials_def.setter
    def trials_def(self, value):
        self.model.trials_def = value
    @property
    def session_name(self):
        return self.model.session_name

    @session_name.setter
    def session_name(self, value):
        self.model.session_name = value

    @property
    def experimenter_name(self):
        return self.model.experimenter_name

    @experimenter_name.setter
    def experimenter_name(self, value):
        self.model.experimenter_name = value
    @property
    def trial_types_successive_counter(self):
        return self.model.trial_types_successive_counter

    @trial_types_successive_counter.setter
    def trial_types_successive_counter(self, value):
        self.model.trial_types_successive_counter = value

    @property
    def trial_types_total_counter(self):
        return self.model.trial_types_total_counter

    @trial_types_total_counter.setter
    def trial_types_total_counter(self, value):
        self.model.trial_types_total_counter = value

    @property
    def iti(self):
        return self.model.iti

    @iti.setter
    def iti(self, value):
        self.model.iti = value

    @property
    def trials_order(self):
        return self.model.trials_order

    @trials_order.setter
    def trials_order(self, value):
        self.model.trials_order = value

    # make properties
    @property
    def timer(self):
        return self.model.timer

    @timer.setter
    def timer(self, value):
        # if value < -273.15:
        #     raise ValueError("Temperature below -273 is not possible")
        self.model.timer = value

    # select to notify only events that are relevant
    def SessionVMEventHandler(self, sender, *event_args):
        # is this if necessary?
        if type(sender) != SessionModel:
            self.subject_id = sender.subject_id
        if event_args[0][0] == "subject_id":
            # change the property
            self.notifyPropertyChanged("VM_" + event_args[0][0])
        self.notifyPropertyChanged("VM_" + event_args[0][0])
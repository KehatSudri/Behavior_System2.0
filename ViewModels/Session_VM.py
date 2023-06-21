from Models.Session_Model import SessionModel


class SessionViewModel:
    def __init__(self):
        super(SessionViewModel, self).__init__()
        self.model = SessionModel()

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


    # select to notify only events that are relevant
    def SessionVMEventHandler(self, sender, *event_args):
        if type(sender) != SessionModel:
            self.subject_id = sender.subject_id
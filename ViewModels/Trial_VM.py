from Models.Trial_Model import TrialModel


class TrialViewModel:
    def __init__(self, m: TrialModel):
        super(TrialViewModel, self).__init__()
        self.model = m
        self.type = None  # name the trial type
        # if we want to display this parameters during trial
        self.parameters = None  # dictionary that holds necessary parameters
        self.tone = None
        self.reward = None

    # make properties

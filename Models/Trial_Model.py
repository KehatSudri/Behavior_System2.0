import random
import time
import numpy as np
from abc import ABC, abstractmethod


class Interval(ABC):
    @abstractmethod
    def get_iti_type(self):
        pass


class RandInterval(Interval):
    def __init__(self, interval_range):
        super(RandInterval, self).__init__()
        self.min_interval, self.max_interval = interval_range
        self.iti_vec = None

    def get_iti_type(self):
        return "random"


def get_name_by_id(types, trial_id):
    for trial in types:
        if trial[0] == trial_id:
            return trial[1]
    return None


class TrialModel:
    def __init__(self, t_id=None, name=None, events: list = None, inters: list = None):
        super(TrialModel, self).__init__()
        self._trial_id = t_id
        self._name = name  # name the trial type
        self._events = events
        self._intervals = inters

    @property
    def trial_id(self):
        return self._trial_id

    @trial_id.setter
    def trial_id(self, value):
        if self._trial_id == value:
            return
        self._trial_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name == value:
            return
        self._name = value

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        if self._events == value:
            return
        self._events = value

    @property
    def intervals(self):
        return self._intervals

    @intervals.setter
    def intervals(self, value):
        if self._intervals == value:
            return
        self._intervals = value

    def get_intervals(self):
        if self.intervals is not None:
            return [np.random.randint(int(x[0]), int(x[1]) + 1) / 100 for x in self.intervals]
        return None

    def events_str(self):
        events = ""
        for e in self.events:
            events += e.get_type_str() + ","
        return events

    def intervals_str(self):
        inters = ""
        for i in self.intervals:
            inters += "(" + i[0] + "-" + i[1] + "),"
        return inters


class Trials_def(ABC):
    def __init__(self, trial_list: list):
        self.trials = trial_list

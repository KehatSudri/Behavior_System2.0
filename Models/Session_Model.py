import csv
import queue
import sys
import threading

import random
import time
from datetime import date, datetime, timedelta

import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration, Edge, WAIT_INFINITELY, LineGrouping
from nidaqmx.stream_readers import AnalogMultiChannelReader

import numpy as np

from Models.Trial_Model import Trials_def, Interval, TrialModel

BUFFER_SIZE = 50
LOG_DATA_IDX = 0


class BehaviourInterval(Interval):
    def __init__(self, behave_def=None):
        super(BehaviourInterval, self).__init__()
        self.definition = behave_def

    def get_iti_type(self):
        return "behavior"


class SessionTemplate:
    def __init__(self):
        self._session_id = None
        self._iti = None  # object type ITI holds the required inter-trial intervals
        self._end_def = None  # tuple of type and value
        self._trials_order = None  # blocks or random
        self._trials_def = None
        self._session_name = None
        self._experimenter_name = None
        self._last_used = None
        self.rnd_reward_percent = None

    @property
    def trials_def(self):
        return self._trials_def

    @trials_def.setter
    def trials_def(self, value):
        if self._trials_def == value:
            return
        self._trials_def = value

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if self._session_id == value:
            return
        self._session_id = value

    @property
    def last_used(self):
        return self._last_used

    @last_used.setter
    def last_used(self, value):
        if self._last_used == value:
            return
        self._last_used = value

    @property
    def iti(self):
        return self._iti

    @iti.setter
    def iti(self, value):
        if self._iti == value:
            return
        self._iti = value

    @property
    def end_def(self):
        return self._end_def

    @end_def.setter
    def end_def(self, value):
        if self._end_def == value:
            return
        self._end_def = value

    @property
    def trials_order(self):
        return self._trials_order

    @trials_order.setter
    def trials_order(self, value):
        if self._trials_order == value:
            return
        self._trials_order = value

    @property
    def session_name(self):
        return self._session_name

    @session_name.setter
    def session_name(self, value):
        if self._session_name == value:
            return
        self._session_name = value

    @property
    def experimenter_name(self):
        return self._experimenter_name

    @experimenter_name.setter
    def experimenter_name(self, value):
        if self._experimenter_name == value:
            return
        self._experimenter_name = value

    def set_params(self, trials_def: Trials_def = None, iti: Interval = None, end_def=None,
                   order: str = None, sess_name=None, exp_name=None, rnd_prcnt=None):
        if trials_def is not None:
            self.trials_def = trials_def
        if iti is not None:
            self.iti = iti
        if end_def is not None:
            self.end_def = end_def
        if order is not None:
            self.trials_order = order
        if sess_name is not None:
            self.session_name = sess_name
        if exp_name is not None:
            self.experimenter_name = exp_name
        if rnd_prcnt is not None:
            self.rnd_reward_percent = rnd_prcnt

    def get_params(self):
        return self.trials_def, self.iti, self.end_def, self.trials_order, self.session_name, self.experimenter_name, self.rnd_reward_percent


class SessionModel(SessionTemplate):
    def __init__(self):
        SessionTemplate.__init__(self)
        self.is_session_running = False
        self._subject_id = None
        self._session_id = None
        self._end_session = False
        self.log_path = None
        self._output_ports = None
        self.output_events_name_list = None
        self.output_vals = None

    @property
    def output_ports(self):
        return self._output_ports

    @property
    def subject_id(self):
        return self._subject_id

    @subject_id.setter
    def subject_id(self, value):
        if self._subject_id == value:
            return
        self._subject_id = value

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if self._session_id != value:
            self._session_id = value

    def get_params(self):
        return self.subject_id, self.trials_def, self.iti, self.end_def, self.trials_order, self.session_name, self.experimenter_name, self.rnd_reward_percent

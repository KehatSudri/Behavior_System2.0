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
            self.iti = iti  # object type ITI holds the required inter-trial intervals
        if end_def is not None:
            self.end_def = end_def  # tuple of type and value
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
        # get params and set params of template
        self._session_id = None  # Generate unique id for session
        self._end_session = False
        # self._session_date = date.today()  # TODO check type
        self.timer = 0
        self.log_path = None
        self._trial_types_total_counter = []
        self._trial_types_successive_counter = []
        self.input_flag = False
        self.input_has_come = threading.Event()
        self.is_give_reward = False
        self.reward_to_give = None
        self.log_queue = queue.Queue()
        self.sampling_rate = 5000
        self._output_ports = None
        self.output_events_name_list = None
        self.output_vals = None
        self.input_ports = ['Dev1/ai1']
        self.input_events_name_list = None
        self.input_flags = None
        self.buffer_in = None
        self._data = np.ndarray([])  # will contain a first column with zeros but that's fine
        self.stream_in = None
        self._input_to_read = None
        self.log_file = None
        self.buffer_in2 = None
        self.success_rate = 0
        self.reward_list_in_sess = None
        self.data_log_file = None
        self.data = np.zeros((1, 1))
        self.running_session = None
        self.should_pause = False

    def give_reward(self, reward_name):
        self.reward_to_give = reward_name  # self.output_events_name_list.index(reward_name)
        self.is_give_reward = True

    def start(self):
        if self.running_session is None:
            self.is_session_running = True
            self.running_session = self.get_read_in_task()
            self.running_session.start()

    def pause(self):
        if not self.is_session_running or self.should_pause:
            return
        self.should_pause = True
        self.running_session.stop()

    def resume(self):
        if not self.is_session_running or not self.should_pause:
            return
        self.should_pause = False
        self.running_session.start()

    def finish(self):
        if not self.is_session_running:
            return
        self.is_session_running = False
        self.running_session.close()
        self.running_session = None

    def get_read_in_task(self):
        read_input_task = nidaqmx.Task()
        for port in self.input_ports:
            read_input_task.ai_channels.add_ai_voltage_chan(port, terminal_config=TerminalConfiguration.RSE)
            # set sampling rate per channel per second!
            read_input_task.timing.cfg_samp_clk_timing(self.sampling_rate, source="", active_edge=Edge.RISING,
                                                       sample_mode=AcquisitionType.CONTINUOUS)
        self.stream_in = AnalogMultiChannelReader(read_input_task.in_stream)
        read_input_task.register_every_n_samples_acquired_into_buffer_event(10, self.reading_task_data_callback)
        return read_input_task

    def reading_task_data_callback(self, task_idx, event_type, num_samples,
                                   callback_data):  # bufsize_callback is passed to num_samples
        size = 500
        if self.is_session_running:
            # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
            # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
            self.buffer_in = np.zeros((len(self.input_ports), size))  # double definition ???
            self.stream_in.read_many_sample(self.buffer_in, size, timeout=WAIT_INFINITELY)
            # self.stream_in.read_one_sample(self.buffer_in2, timeout=WAIT_INFINITELY)
            # self.data = np.append(self.data, self.buffer_in, axis=1)  # appends buffered data to total variable data
            # self.input_to_read = np.append(self.input_to_read, self.buffer_in, axis=1)
            #    pass
            # self.input_to_read.put(self.buffer_in)
        return 0

    @property
    def output_ports(self):
        return self._output_ports

    @output_ports.setter
    def output_ports(self, value):
        if self.output_ports != value:
            self._output_ports = value
            self.output_vals = [False] * len(value)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def input_to_read(self):
        return self._input_to_read

    @input_to_read.setter
    def input_to_read(self, value):
        self._input_to_read = value

    @property
    def trial_types_successive_counter(self):
        return self._trial_types_successive_counter

    @trial_types_successive_counter.setter
    def trial_types_successive_counter(self, value):
        self._trial_types_successive_counter = value

    @property
    def trial_types_total_counter(self):
        return self._trial_types_total_counter

    @trial_types_total_counter.setter
    def trial_types_total_counter(self, value):
        self._trial_types_total_counter = value

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

    @property
    def end_session(self):
        return self._end_session

    @end_session.setter
    def end_session(self, value):
        if self._end_session != value:
            self._end_session = value

    def get_params(self):
        return self.subject_id, self.trials_def, self.iti, self.end_def, self.trials_order, self.session_name, self.experimenter_name, self.rnd_reward_percent

    def validate_ending(self, trial_num, is_trial_beggining):
        end_def_str, end_def_val = self.end_def
        if end_def_str == "Time passed (seconds)" and (
                self.add_times(datetime.now().time(), self.timer, True) > timedelta(seconds=end_def_val)):
            self.end_session = True
            return True
        if is_trial_beggining:
            if end_def_str == "Number of trials" and trial_num >= end_def_val:
                self.end_session = True
                return True
            if end_def_str == "Success rate" and end_def_val <= self.success_rate:
                self.end_session = True
                return True
        return False

    def is_input(self):
        return self.input_flag

    def reset_run(self, write_task, read_task):
        read_task.stop()
        self.output_vals = [False] * len(self.output_vals)
        write_task.write(self.output_vals)

    def add_times(self, time1, time2, is_substract_flag=False):
        time1 = str(time1).split(":")
        hour1, minute1, second1, microsec1 = int(time1[0]), int(time1[1]), int(time1[2].split(".")[0]), int(
            time1[2].split(".")[1])
        timer1 = timedelta(hours=hour1, minutes=minute1, seconds=second1, microseconds=microsec1)
        time2 = str(time2).split(":")
        hour2, minute2, second2, microsec2 = int(time2[0]), int(time2[1]), int(time2[2].split(".")[0]), int(
            time2[2].split(".")[1])
        timer2 = timedelta(hours=hour2, minutes=minute2, seconds=second2, microseconds=microsec2)
        if is_substract_flag:
            return timer1 - timer2
        else:
            return timer1 + timer2

    def run_session(self, log_file, max_successive_trials, max_trial_length):
        self.end_session = False
        # max_successive_trials = 30 #this should come from system
        # initiate counters for total and successive trials for each trial type in session
        self.trial_types_total_counter = np.zeros(len(self.trials_def.trials))
        self.trial_types_successive_counter = np.zeros(len(self.trials_def.trials))
        # get the trials ordered
        trials_to_run = self.trials_def.get_trials_order(max_successive_trials)
        # get the number of trials to run
        total_num = self.trials_def.get_total_num()
        # start to run the trials according to the iti type
        iti_t = self.iti.get_iti_type()
        # self.run_any_session(trials_to_run, total_num, log_file, max_trial_length, iti_t == "random")
        self.try_run(trials_to_run, total_num, log_file, max_trial_length, iti_t == "random")
        self.log_queue.join()

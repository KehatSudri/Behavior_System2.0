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

from Models import TrialEvents
from Models.INotifyPropertyChanged import INotifyPropertyChanged
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


class SessionModel(SessionTemplate, INotifyPropertyChanged):
    def __init__(self):
        SessionTemplate.__init__(self)
        INotifyPropertyChanged.__init__(self)
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
        self.pause = False
        self.repeat_trial = False
        self.is_give_reward = False
        self.reward_to_give = None
        self.log_queue = queue.Queue()
        self.sampling_rate = 5000
        self._output_ports = None
        self.output_events_name_list = None
        self.output_vals = None
        self.input_ports = []
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

    def give_reward(self, reward_name):
        self.reward_to_give = reward_name  # self.output_events_name_list.index(reward_name)
        self.is_give_reward = True

    def start(self):
        self.is_session_running = True
        self.input_ports.append('Dev1/ai1')
        t = self.get_read_in_task()
        t.start()

        # while 1:
        #     print(t.read(2))
        #     time.sleep(2)
        # with nidaqmx.Task() as task:
        #     task.ai_channels.add_ai_voltage_chan('Dev1/ai1')
        #     while self.is_session_running:
        #         data = task.read(number_of_samples_per_channel=2)
        #         print(data)
        #         time.sleep(1)

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
        if not self.end_session:
            # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
            # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
            self.buffer_in = np.zeros((len(self.input_ports), size))  # double definition ???
            self.stream_in.read_many_sample(self.buffer_in, size, timeout=WAIT_INFINITELY)
            # self.stream_in.read_one_sample(self.buffer_in2, timeout=WAIT_INFINITELY)
            print(self.buffer_in)
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
            self.notifyPropertyChanged("output_ports")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # if self.data is None:
        self._data = value
        self.notifyPropertyChanged("data")

    @property
    def input_to_read(self):
        return self._input_to_read

    @input_to_read.setter
    def input_to_read(self, value):
        self._input_to_read = value
        self.notifyPropertyChanged("input_to_read")

    @property
    def trial_types_successive_counter(self):
        return self._trial_types_successive_counter

    @trial_types_successive_counter.setter
    def trial_types_successive_counter(self, value):
        self._trial_types_successive_counter = value
        self.notifyPropertyChanged("trial_types_successive_counter")

    @property
    def trial_types_total_counter(self):
        return self._trial_types_total_counter

    @trial_types_total_counter.setter
    def trial_types_total_counter(self, value):
        # if self._trial_types_total_counter == value:
        #     return
        self._trial_types_total_counter = value
        self.notifyPropertyChanged("trial_types_total_counter")

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
            self.notifyPropertyChanged("session_id")

    @property
    def end_session(self):
        return self._end_session

    @end_session.setter
    def end_session(self, value):
        if self._end_session != value:
            self._end_session = value

            self.notifyPropertyChanged("end_session")

    def get_params(self):
        return self.subject_id, self.trials_def, self.iti, self.end_def, self.trials_order, self.session_name, self.experimenter_name, self.rnd_reward_percent

    def turn_input_on(self):
        # should do some validation and then
        self.input_flag = True

    def turn_input_off(self):
        self.input_flag = False

    # TODO validate function
    def find_list_idx(self, lens, idx):
        sum_of_lens = 0
        for i in len(lens):
            sum_of_lens += lens[i]
            if idx < (sum_of_lens - 1):
                return i

    def calc_sub_intervs(self, iti_vals, limit):
        return [random.randfloat(0, iti - limit) for iti in iti_vals]
        pass

    def get_trials_run_with_rnd_reward(self, trials_to_run, total_num, iti_vals):
        iti_vals2 = [int(a * 100) for a in iti_vals]
        trials = []
        itis = []
        reward_e = TrialEvents.Reward(4, 4, 4)  # TODO this should be from a list of reward, maybe randomized
        t = TrialModel(t_id=None, name="rnd reward", events=[reward_e], inters=None)
        # get indexes of intervals for rnd rewards
        num_of_rnd_reward = int(self.rnd_reward_percent * total_num / 100)
        idx_list = list(range(total_num))
        random.shuffle(idx_list)
        idx_list = idx_list[0:num_of_rnd_reward]
        idx_list.sort()
        limit = 0.01  # this should be the duration of the reward with a boundary?
        # get interval to give the reward
        for i in range(len(trials_to_run)):
            trials.append(trials_to_run[i])
            # if this idx is chosen for a rnd reward
            if len(idx_list) != 0 and idx_list[0] == i:
                wait_to_reward = random.randint(0, (iti_vals2[i])) / 100
                itis.append(wait_to_reward)
                itis.append(iti_vals[i] - wait_to_reward)
                trials.append(t)
                idx_list = idx_list[1:]
            else:
                itis.append(iti_vals[i])
        return trials, itis

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

    def get_rnd_reward_itis(self, total_num, iti_vals):
        # iti_vals2 = [int(a * 100) for a in iti_vals]
        iti_vals2 = iti_vals
        itis = []
        reward = []
        reward_e = TrialEvents.Reward(4, 4, 4)  # TODO this should be from a list of reward, maybe randomized
        t = TrialModel(t_id=None, name="rnd reward", events=[reward_e], inters=None)
        # get indexes of intervals for rnd rewards
        num_of_rnd_reward = int(self.rnd_reward_percent * total_num / 100)
        idx_list = list(range(1, total_num))
        random.shuffle(idx_list)
        idx_list = idx_list[0:num_of_rnd_reward]
        idx_list.sort()
        limit = 1  # this should be the duration of the reward with a boundary?
        if num_of_rnd_reward != 0:
            for i in range(len(idx_list)):
                # if this idx is chosen for a rnd reward
                wait_to_reward = random.randint(0, (iti_vals2[idx_list[i]] - limit))  # / 100
                itis.append(wait_to_reward)
                reward.append(reward_e)  # TODO this should be randomized from list of rewards
        return reward, idx_list, itis

    def get_trial_type_idx(self, trial):
        for i in range(len(self.trials_def.trials)):
            if self.trials_def.trials[i].name == trial.name:
                return i

    # def run_rnd_iti_session(self, trials_to_run, total_num, log_file, max_trial_length):
    #     iti_vals = self.iti.get_iti_vec()
    #     # get iti's , indexes and reward for random reward
    #     rewards, idxs, short_itis = self.get_rnd_reward_itis(total_num, iti_vals)
    #     # run until session end
    #     i, rew_count = 0, 0
    #     # keep starting time
    #     self.interval_start_time = datetime.now()
    #     last_type_idx = None
    #
    #     while not self.end_session:
    #         if self.pause:
    #             time.sleep(1)
    #             continue
    #
    #         cur_type_idx = self.get_trial_type_idx(trials_to_run[i])
    #         if last_type_idx is None:
    #             last_type_idx = cur_type_idx
    #         # run current trial
    #         trials_to_run[i].run()
    #         # update counters
    #         tmp_total = self.trial_types_total_counter
    #         tmp_successive = self.trial_types_successive_counter
    #         if cur_type_idx != last_type_idx:
    #             tmp_successive = np.zeros(len(self.trial_types_successive_counter))
    #         tmp_successive[cur_type_idx] += 1
    #         # self.trial_types_successive_counter[cur_type_idx] += 1
    #         self.trial_types_successive_counter = tmp_successive
    #         tmp_total[cur_type_idx] += 1
    #         self.trial_types_total_counter = tmp_total
    #         # self.trial_types_total_counter[cur_type_idx] += 1
    #         print(self.trial_types_total_counter)  # TODO delete
    #         if last_type_idx != cur_type_idx:
    #             self.trial_types_successive_counter[last_type_idx] = 0
    #             last_type_idx = cur_type_idx
    #         print(self.trial_types_successive_counter)
    #         # grant random reward if required here
    #         if len(idxs) > 0 and len(idxs) > rew_count and i == idxs[rew_count]:
    #             time.sleep(short_itis[rew_count])
    #             # rewards[rew_count].execute()
    #             print("rnd reward!!!!")
    #             time.sleep(iti_vals[i] - short_itis[rew_count])
    #             rew_count += 1
    #         else:
    #             time.sleep(iti_vals[i])
    #         # calculate success rate
    #         self.success_rate = 0  # TODO check what to do about this
    #         while self.repeat_trial:
    #             self.repeat_trial = False
    #             trials_to_run[i].run()
    #             # do successive count should grow? and total?
    #         i += 1
    #         # check ending condition is not satisfied
    #         self.validate_ending(i)
    #         # ran all trials for session
    #         if i >= len(trials_to_run):
    #             self.end_session = True
    #             print("ran all trials - end session")

    def is_input(self):
        return self.input_flag

    def repeat_same_trial(self):
        self.repeat_trial = True

    # def reading_task_queue_callback(self, task_idx, event_type, num_samples,
    #                                 callback_data):  # bufsize_callback is passed to num_samples
    #     if not self.end_session:
    #         # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
    #         # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
    #         self.buffer_in = np.zeros((len(self.input_ports), num_samples))  # double definition ???
    #         self.stream_in.read_one_sample(self.buffer_in, timeout=WAIT_INFINITELY)
    #         self.input_to_read.put(self.buffer_in)  # appends buffered data to total variable data
    #     return 0

    def get_write_out_task(self):
        write_task = nidaqmx.Task()
        for port in self.output_ports:
            write_task.do_channels.add_do_chan(port, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            # set sampling rate per channel per second!
            # write_task.timing.cfg_samp_clk_timing(self.sampling_rate, source="", active_edge=Edge.RISING,
            #                                     sample_mode=AcquisitionType.CONTINUOUS)

        return write_task

    def check_input(self):
        input_read_index = 0
        while 1:
            if input_read_index >= len(self.data[0]):
                continue
            for i in range(len(self.input_ports)):
                self.input_flags[i] = self.data[i, input_read_index] > 3
            input_read_index += 1

    def check_contigent_satisfaction(self, event_to_run):
        pass

    def manage_counters(self, cur_type_idx, last_type_idx):
        tmp_total = self.trial_types_total_counter
        tmp_successive = self.trial_types_successive_counter
        if cur_type_idx != last_type_idx:
            tmp_successive = np.zeros(len(self.trial_types_successive_counter))
        tmp_successive[cur_type_idx] += 1
        # self.trial_types_successive_counter[cur_type_idx] += 1
        self.trial_types_successive_counter = tmp_successive
        tmp_total[cur_type_idx] += 1
        self.trial_types_total_counter = tmp_total
        if last_type_idx != cur_type_idx:
            self.trial_types_successive_counter[last_type_idx] = 0
            last_type_idx = cur_type_idx
            return True
        return False

    def reset_run(self, write_task, read_task):
        read_task.stop()
        self.output_vals = [False] * len(self.output_vals)
        write_task.write(self.output_vals)

    def is_delta_more_than_time(self, delta, time_stamp):
        time_stamp = str(time_stamp).split(":")
        print("")
        hour, minute, second, microsec = int(time_stamp[0]), int(time_stamp[1]), int(time_stamp[2].split(".")[0]), int(
            time_stamp[2].split(".")[1])
        timer = timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsec)
        if delta - timer > timedelta(milliseconds=0):
            return True
        return False

    def add_int_delta_to_time(self, delta, time_stamp):
        time_stamp = str(time_stamp).split(":")
        hour, minute, second, microsec = int(time_stamp[0]), int(time_stamp[1]), int(time_stamp[2].split(".")[0]), int(
            time_stamp[2].split(".")[1])
        timer = timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsec)

        return timer + timedelta(milliseconds=delta)

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

    def session_ending(self, writing_output_task, reading_input_task, ending_reason, end_time, paused_time):
        self.reset_run(writing_output_task, reading_input_task)
        self.log_queue.put(str(end_time) + "   - Session ended: " + ending_reason + "\n")
        total_dur = self.add_times(end_time, self.timer, True)
        self.log_queue.put("\ntotal duration: " + str(total_dur) + "\n")
        self.log_queue.put("total duration minus pausing times: " + str(
            total_dur - paused_time) + "\n")
        reading_input_task.close()
        writing_output_task.close()
        self.end_session = True
        pass

    def write_logging(self):
        while 1:
            try:
                write_str = self.log_queue.get(block=True, timeout=100)
                self.log_file.write(write_str)
                self.log_file.flush()
            except Exception as e:
                # meaning timeout
                if self.end_session:
                    while not self.log_queue.empty():
                        write_str = self.log_queue.get(block=True, timeout=100)
                        self.log_file.write(write_str)
                        self.log_file.flush()
                    return

    def write_input_data(self):
        max_num_lines_in_file = 1000000
        number_of_lines_per_write = 1000
        cur_file_lines_count = 0
        original_file_name = self.data_log_file.name.split(".")[0]
        file_count = 1
        global LOG_DATA_IDX
        writer = csv.writer(self.data_log_file)
        writer.writerow(self.input_events_name_list)
        time.sleep(3)
        while 1:
            # write x lines every 2 seconds if they exist.
            # if written almost max num, create new file
            if cur_file_lines_count + number_of_lines_per_write > max_num_lines_in_file:
                file_count += 1
                file_name_new = original_file_name + str(file_count) + ".csv"
                self.data_log_file.close()
                self.data_log_file = open(file_name_new, 'w', encoding='utf-8', newline='')
                writer = csv.writer(self.data_log_file)
                writer.writerow(self.input_events_name_list)
                cur_file_lines_count = 0
            if LOG_DATA_IDX < len(self.data.T) + number_of_lines_per_write:
                writer.writerows(self.data.T[LOG_DATA_IDX:LOG_DATA_IDX + number_of_lines_per_write])
                LOG_DATA_IDX += number_of_lines_per_write
                cur_file_lines_count += number_of_lines_per_write
            time.sleep(2)
            # if end session - write remaining lines
            if self.end_session:
                last_idx = len(self.data.T)
                while LOG_DATA_IDX + number_of_lines_per_write < last_idx:
                    if cur_file_lines_count + number_of_lines_per_write > max_num_lines_in_file:
                        file_count += 1
                        file_name_new = original_file_name + str(file_count) + ".csv"
                        self.data_log_file.close()
                        self.data_log_file = open(file_name_new, 'w', encoding='utf-8', newline='')
                        writer = csv.writer(self.data_log_file)
                        writer.writerow(self.input_events_name_list)
                        cur_file_lines_count = 0
                    writer.writerows(self.data.T[LOG_DATA_IDX:LOG_DATA_IDX + number_of_lines_per_write])
                    LOG_DATA_IDX += number_of_lines_per_write
                    cur_file_lines_count += number_of_lines_per_write

                return

    def is_contigent(self, event):
        return False

    def try_run(self, trials_to_run, total_num, log_file, max_trial_length, iti_flag_is_random):
        write_log = threading.Thread(target=self.write_logging)
        write_log.start()
        write_data = threading.Thread(target=self.write_input_data)
        write_data.start()
        paused_time = timedelta(milliseconds=0)

        success_count, trial_idx, event_idx, next_interval, iti_idx, read_input_idx = 0, 0, 0, 0, 0, 0
        given_rnd_interval, start_iti, stopped_flag = False, False, False
        i, rew_count, trial_index, time_from_pause = 0, 0, 0, 0
        output_times = [timedelta(milliseconds=0)] * len(self.output_vals)  # for now reward is 0 and tone is 1
        self.buffer_in = np.zeros((len(self.input_ports), BUFFER_SIZE))
        self.data = np.zeros((len(self.input_ports), 1))
        self.input_to_read = np.zeros((len(self.input_ports), 1))
        iti_vals, rewards, idxs, short_itis = None, None, None, None
        self.number_of_inputs_to_skip = 0
        # get specific iti times
        if iti_flag_is_random:
            iti_vals = self.iti.get_iti_vec(2 * len(trials_to_run))
            # get iti's , indexes and reward for random reward
            rewards, idxs, short_itis = self.get_rnd_reward_itis(total_num, iti_vals)
        # get index of input event required for trial start
        else:
            iti_input_index = self.input_events_name_list.index(self.iti.definition)
        repeated_trial_count = 0
        # create read and write tasks
        reading_input_task = self.get_read_in_task()
        writing_output_task = self.get_write_out_task()
        # set all outputs to 0
        writing_output_task.write(self.output_vals)
        # start data acquisition
        reading_input_task.start()
        self.log_queue.put(str(datetime.now()) + "   - Session start\n")
        self.timer = self.interval_start_time = datetime.now().time()
        trial_start_time = datetime.now().time()

        last_type_idx = cur_type_idx = self.get_trial_type_idx(trials_to_run[0])
        while not self.end_session:
            # pause is pressed
            if self.pause:
                pause_start = datetime.now().time()
                # reset input and outputs
                self.reset_run(writing_output_task, reading_input_task)
                # add logging
                self.log_queue.put(str(pause_start) + "   - Session pause\n")
                # set the next trial to be next to run, immediately when resume is pressed
                if event_idx != 0:
                    trial_index += 1
                    event_idx = 0
                    next_interval = 0
                # wait until resume or stop
                while not self.end_session and self.pause:
                    continue
                key_pressed_time = datetime.now().time()
                paused_time += self.add_times(key_pressed_time, pause_start, True)
                # is session is stopped - stop tasks and write to log
                if self.end_session:
                    self.session_ending(writing_output_task, reading_input_task, "by user, ", key_pressed_time,
                                        paused_time)
                    stopped_flag = True
                    break
                # write resume time to log file and start
                self.log_queue.put(str(key_pressed_time) + "   - Session resume\n")

                reading_input_task.start()
            # verify session ending
            if self.validate_ending(trial_idx, event_idx == 0):
                self.session_ending(writing_output_task, reading_input_task, "end definition satisfied, ",
                                    datetime.now().time(), paused_time)
                stopped_flag = True
                break
            # turn off all finished outputs
            for j in range(len(self.output_vals)):
                if output_times[j] != timedelta(0) and not self.is_delta_more_than_time(output_times[j],
                                                                                        datetime.now().time()):
                    self.output_vals[j] = False
                    output_times[j] = timedelta(milliseconds=0)
            writing_output_task.write(self.output_vals)
            # if maximum length of trial is reached, go to next trial
            if event_idx != 0 and not self.is_delta_more_than_time(
                    self.add_int_delta_to_time(max_trial_length, trial_start_time), datetime.now().time()):
                self.log_queue.put(str(datetime.now()) + "   - Trial reached maximum time. moving to next trial\n")

                event_idx = len(trials_to_run[trial_idx].events) - 1
                dur = int(trials_to_run[trial_idx].events[event_idx].getDuration())
                read_input_idx += int((dur + 50) * self.sampling_rate / 1000)

                trial_idx += 1
                event_idx = 0
                if iti_flag_is_random:
                    next_interval = iti_vals[iti_idx]
                else:
                    next_interval = 0
                iti_idx += 1
                # when finishing a trial, update trial types counters
                if self.manage_counters(cur_type_idx, last_type_idx):
                    last_type_idx = cur_type_idx
                if trial_idx >= len(trials_to_run):
                    self.end_session = True
                    break
                cur_type_idx = self.get_trial_type_idx(trials_to_run[trial_idx])
                given_rnd_interval = False
            # give reward if pressed:
            if self.is_give_reward:
                self.is_give_reward = False
                output_idx = self.output_events_name_list.index(self.reward_to_give)

                event_to_give = None
                for r in self.reward_list_in_sess:
                    if r.get_type_str() == self.reward_to_give:
                        event_to_give = r
                        break
                if event_to_give is not None:
                    self.output_vals[output_idx] = True
                    output_times[output_idx] = self.add_int_delta_to_time(int(r.getDuration()),
                                                                          datetime.now().time())
                    writing_output_task.write(self.output_vals)

            # read the input
            if read_input_idx < len(self.input_to_read.T):
                # input = self.input_to_read[:, read_input_idx]
                input = self.input_to_read[:, read_input_idx]
                read_input_idx += 10
                if not iti_flag_is_random and input[iti_input_index] > 3:
                    self.input_flag = True

            # run the next event for one of the following options -
            # 1. middle of trial and interval between events passed
            # 2. beginning of trial and random ITI is finished
            # 3. beginning of trial and behavior input for behave cue happened
            if ((event_idx != 0 or iti_flag_is_random) and not self.is_delta_more_than_time(
                    self.add_int_delta_to_time(next_interval, self.interval_start_time), datetime.now().time())) or (
                    event_idx == 0 and not iti_flag_is_random and self.input_flag):
                self.input_flag = False
                stop_events_flag = True
                if event_idx == 0:
                    self.log_queue.put(
                        str(datetime.now().time()) + "   - Trial #" + str(trial_idx + 1) + " starting: " +
                        trials_to_run[
                            trial_idx].name + "\n")
                    trials_start_time = datetime.now().time()
                while stop_events_flag:
                    if event_idx >= len(trials_to_run[trial_idx].events):
                        stop_events_flag = False
                        break
                    event_to_run = trials_to_run[trial_idx].events[event_idx]
                    output_event_idx = self.output_events_name_list.index(
                        event_to_run.get_type_str())  # TODO get event index
                    # if event is simple or contingent requirements satisfied
                    if not self.is_contigent(event_to_run) or self.check_contigent_satisfaction(event_to_run):
                        self.output_vals[output_event_idx] = True
                        output_times[output_event_idx] = self.add_int_delta_to_time(int(event_to_run.getDuration()),
                                                                                    datetime.now().time())

                        writing_output_task.write(self.output_vals)
                        self.log_queue.put(str(datetime.now().time()) +
                                           "   - Output Event, " + event_to_run.get_type_str() + "\n")

                        event_idx += 1
                        if event_to_run.is_reward():
                            success_count += 1
                            self.success_rate = (success_count / (len(trials_to_run) + repeated_trial_count)) * 100
                    # continue to all next events that are set to begin with the current
                    if not (event_idx < len(trials_to_run[trial_idx].events) and not self.is_contigent(
                            trials_to_run[trial_idx].events[event_idx]) and
                            trials_to_run[trial_idx].intervals[event_idx - 1] == 0):
                        stop_events_flag = False

                # get interval start clock from the beginning of the last output
                self.interval_start_time = datetime.now().time()

                # check if ran all events for current session
                if event_idx >= len(trials_to_run[trial_idx].events):
                    if not iti_flag_is_random:
                        # skip the duration of output, until checking for next trigger for trial
                        read_input_idx += int((int(event_to_run.getDuration()) + 50) * self.sampling_rate / 1000)
                    # check whether repeat trial request is on
                    if not self.repeat_trial:
                        # go to next trial
                        trial_idx += 1
                    else:
                        repeated_trial_count += 1
                        self.repeat_trial = False
                    event_idx = 0
                    if iti_flag_is_random:
                        next_interval = iti_vals[iti_idx]
                    else:
                        next_interval = 0
                    iti_idx += 1
                    # when finishing a trial, update trial types counters
                    if self.manage_counters(cur_type_idx, last_type_idx):
                        last_type_idx = cur_type_idx
                    if trial_idx >= len(trials_to_run):
                        self.end_session = True
                        break
                    cur_type_idx = self.get_trial_type_idx(trials_to_run[trial_idx])
                    given_rnd_interval = False
                    trial_start_time = datetime.now().time()
                else:
                    interval = trials_to_run[trial_idx].intervals[event_idx - 1]
                    next_interval = np.random.randint(int(interval[0]), int(interval[1]) + 1)
            # TODO validate
            if iti_flag_is_random and len(self.reward_list_in_sess) > 0 and len(
                    idxs) > rew_count and not given_rnd_interval:
                if iti_idx == idxs[rew_count]:
                    if self.is_delta_more_than_time(
                            self.add_int_delta_to_time(short_itis[rew_count], self.interval_start_time),
                            datetime.now().time()):
                        rnd_idx = random.randint(0, len(self.reward_list_in_sess) - 1)
                        output_event_idx = self.output_events_name_list.index(
                            self.reward_list_in_sess[rnd_idx].get_type_str())
                        self.output_vals[output_event_idx] = True
                        output_times[output_event_idx] = self.add_int_delta_to_time(int(event_to_run.getDuration()),
                                                                                    datetime.now().time())
                        writing_output_task.write(self.output_vals)

                        given_rnd_interval = True
                        rew_count += 1

            # while self.repeat_trial:
            #     self.repeat_trial = False
            #     trials_to_run[i].run()
            #     # do successive count should grow? and total?
            # i += 1

        if not stopped_flag:
            self.session_ending(writing_output_task, reading_input_task, "finished trials, ", datetime.now().time(),
                                paused_time)

        finish_all_output = True
        while not finish_all_output:
            finish_all_output = True
            for j in range(len(self.output_vals)):
                if self.output_vals[j] != timedelta(0):
                    finish_all_output = False
            if not finish_all_output:
                # turn off all finished outputs
                for j in range(len(self.output_vals)):
                    if output_times[j] != timedelta(0) and not self.is_delta_more_than_time(output_times[j],
                                                                                            datetime.now().time()):
                        self.output_vals[j] = False
                        output_times[j] = timedelta(milliseconds=0)

                writing_output_task.write(self.output_vals)

        write_log.join()
        write_data.join()

    # def run_any_session(self, trials_to_run, total_num, log_file, max_trial_length, iti_flag_is_random):
    #
    #     self.buffer_in = np.zeros((len(self.input_ports), 5000))
    #     self.data = np.zeros((len(self.input_ports), 1))
    #     if iti_flag_is_random:
    #         iti_vals = self.iti.get_iti_vec()
    #         # get iti's , indexes and reward for random reward
    #         rewards, idxs, short_itis = self.get_rnd_reward_itis(total_num, iti_vals)
    #     else:
    #         iti_input_index = 0  # Todo a function to get input index from comparing required bhvor with list of input events.
    #     # create read channels
    #     reading_input_task = self.get_read_in_task()
    #
    #     reading_input_task.start()
    #     # run until session end
    #     i, rew_count = 0, 0
    #     # keep starting time
    #     self.interval_start_time = datetime.now()
    #     last_type_idx = None
    #
    #     threading.Thread(target=self.check_input).start()
    #     while not self.end_session:
    #         if self.pause:
    #             time.sleep(1)
    #             continue
    #
    #         cur_type_idx = self.get_trial_type_idx(trials_to_run[i])
    #         if last_type_idx is None:
    #             last_type_idx = cur_type_idx
    #         # run current trial
    #         trials_to_run[i].run()
    #         # update counters
    #         tmp_total = self.trial_types_total_counter
    #         tmp_successive = self.trial_types_successive_counter
    #         if cur_type_idx != last_type_idx:
    #             tmp_successive = np.zeros(len(self.trial_types_successive_counter))
    #         tmp_successive[cur_type_idx] += 1
    #         # self.trial_types_successive_counter[cur_type_idx] += 1
    #         self.trial_types_successive_counter = tmp_successive
    #         tmp_total[cur_type_idx] += 1
    #         self.trial_types_total_counter = tmp_total
    #         if last_type_idx != cur_type_idx:
    #             self.trial_types_successive_counter[last_type_idx] = 0
    #             last_type_idx = cur_type_idx
    #         print(self.trial_types_successive_counter)
    #         if iti_flag_is_random:
    #             # grant random reward if required here
    #             if len(idxs) > 0 and len(idxs) > rew_count and i == idxs[rew_count]:
    #                 time.sleep(short_itis[rew_count])
    #                 print("rnd reward!!!!")
    #                 time.sleep(iti_vals[i] - short_itis[rew_count])
    #                 rew_count += 1
    #             else:
    #                 time.sleep(iti_vals[i])
    #         else:
    #             while not self.input_flags[iti_input_index]:
    #                 continue  # TODO this will not be good
    #         # calculate success rate
    #         self.success_rate = 0  # TODO check what to do about this
    #         while self.repeat_trial:
    #             self.repeat_trial = False
    #             trials_to_run[i].run()
    #             # do successive count should grow? and total?
    #         i += 1
    #         # check ending condition is not satisfied
    #         self.validate_ending(i)
    #         # ran all trials for session
    #         if i >= len(trials_to_run):
    #             self.end_session = True
    #             print("ran all trials - end session")
    #
    # def run_bhv_iti_session(self, trials_to_run, total_num, log_file, max_trial_length):
    #     # do we start the trials immidiately or wait to cue?
    #
    #     # get iti's , indexes and reward for random reward - maybe, but differnet func
    #     # rewards, idxs, short_itis = self.get_rnd_reward_itis(total_num, iti_vals)
    #     # run until session end
    #     i, rew_count = 0, 0
    #     # keep starting time
    #     self.interval_start_time = datetime.now()
    #     last_type_idx = None
    #
    #     while not self.end_session:
    #
    #         cur_type_idx = self.get_trial_type_idx(trials_to_run[i])
    #         if last_type_idx is None:
    #             last_type_idx = cur_type_idx
    #         # run current trial
    #         trials_to_run[i].run()
    #         # update counters
    #         self.trial_types_successive_counter[cur_type_idx] += 1
    #         self.trial_types_total_counter[cur_type_idx] += 1
    #         print(self.trial_types_total_counter)  # TODO delete
    #         if last_type_idx != cur_type_idx:
    #             self.trial_types_successive_counter[last_type_idx] = 0
    #             last_type_idx = cur_type_idx
    #         print(self.trial_types_successive_counter)
    #         # grant random reward if required here
    #         # if len(idxs) > 0 and len(idxs) > rew_count and i == idxs[rew_count]:
    #         #     time.sleep(short_itis[rew_count])
    #         #     rewards[rew_count].execute()
    #         #     print("rnd reward!!!!")
    #         #     time.sleep(iti_vals[i] - short_itis[rew_count])
    #         #     rew_count += 1
    #         # else:
    #         #     time.sleep(iti_vals[i])
    #         # wait(lambda: self.is_input(), timeout_seconds=100, waiting_for="waiting for input")
    #         # print("got input")
    #         print("wait for i")
    #         while not self.input_flag:
    #             time.sleep(3)
    #         # self.input_has_come.wait()
    #         print("got input")
    #         # calculate success rate
    #         self.success_rate = 0  # TODO check what to do about this
    #         i += 1
    #         # check ending condition is not satisfied
    #         self.validate_ending(i)
    #         # ran all trials for session
    #         if i >= len(trials_to_run):
    #             self.end_session = True
    #             print("ran all trials - end session")
    #
    #     pass

    # TODO validate function
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
        # if iti_t == "random":
        #     self.run_rnd_iti_session(trials_to_run, total_num, log_file, max_trial_length)
        # else:
        #     self.run_bhv_iti_session(trials_to_run, total_num, log_file, max_trial_length)
        # # wait for all log to be written to file before finishing
        self.log_queue.join()

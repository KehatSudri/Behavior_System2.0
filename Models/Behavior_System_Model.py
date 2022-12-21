import threading
from collections import OrderedDict
from datetime import datetime
from importlib import import_module
from pathlib import Path

import numpy as np


import Models.Trial_Model as Trial
from Models.DB_INIT import DB
from Models.INotifyPropertyChanged import INotifyPropertyChanged
from Models.Session_Model import SessionModel, BehaviourInterval, SessionTemplate
from Models.Trial_Model import TrialModel, RandInterval


# function to create list of intervals from a given string in specific format
def create_intervals_list(intervals_str: str):
    intervals = []
    tmp = intervals_str.split("\"")[1:-1]
    for i in range(len(tmp)):
        if tmp[i] != ',':
            r = tmp[i].strip("()").split(",")
            intervals.append((int(r[0]), int(r[1])))
    return intervals


def create_str_from_dict(params_dict):
    params_str = ""
    p_keys = list(params_dict.keys())
    p_vals = list(params_dict.values())
    for i in range(len(p_keys)):
        params_str += p_keys[i] + ":" + str(p_vals[i]) + ","
    return params_str


class BehaviorSystemModel(INotifyPropertyChanged):
    def __init__(self, settings_file=None):
        super(BehaviorSystemModel, self).__init__()
        # settings
        self.settings_file = str(Path(__file__).parent.parent / 'config_files' / 'settings.txt')
        self._db_config_file_path = str(Path(__file__).parent.parent/'config_files'/'database.ini')
        self.db_section = None
        if settings_file is not None:
            self.settings_file = settings_file

        # other
        self.input_ports = ['Dev1/ai0', 'Dev1/ai3', 'Dev1/ai9', 'Dev1/ai15']
        self.input_events_names = ['Lick', 'RoterA', 'RoterB', 'Tone-input']
        self.output_ports = ["Dev1/port1/line4", "Dev1/port1/line2"]
        self.output_events_names = ['Tone', 'Reward']
        # data for each: name, port, input/output, digital/analog, is reward
        self.event_config = [('Tone', 'Dev1/port1/line4', 'Output', 'Digital', 'False'),
                             ('Reward', "Dev1/port1/line2", 'Output', 'Digital', 'True'),
                             ('Lick', 'Dev1/ai0', 'Input', 'Analog', 'False'),
                             ('RoterA', 'Dev1/ai3', 'Input', 'Analog', 'False'),
                             ('RoterB', 'Dev1/ai9', 'Input', 'Analog', 'False')]
        self.digital_params = ['duration']
        self.analog_params = ['duration', 'frequency', 'amplitude']

        self._max_successive_trials = 1000
        self._log_file_path = ""
        self._max_trial_length = 60000
        self._log_file = None
        self.parse_settings(self.settings_file)

        # session
        self._is_running_session = False
        self._curr_session = SessionModel()  # give it all the devices

        # DB
        self._DB = DB(self.db_config_file_path)  # add connection to the DB

        self._trial_types = None
        self._session_templates = None
        self._session_trials = None
        self._subject_sessions = None
        self._session_events = None
        # get data from DB
        self.connect_to_DB()
        self.get_templates_from_DB()
        for i in range(len(self.event_config)):
            self.DB.insert_hardware_event(self.event_config[i][0], self.event_config[i][1], self.event_config[i][2],
                                          self.event_config[i][3], self.event_config[i][4])
        self.get_trial_types_from_DB()
        self.get_hardware_events_from_DB()

    def get_hardware_events_from_DB(self):
        self.event_config = self.DB.get_hardware_events()
        self.parse_ports()
        pass

    def insert_hardware_event_to_DB(self, name, port, in_out, dig_an, is_rew):
        self.DB.insert_hardware_event(name, port, in_out, dig_an, is_rew)
        self.get_hardware_events_from_DB()

    def parse_settings(self, settings_file):
        f = open(settings_file, 'r', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                pass
            # other
            split_line = line.split("=")
            header, val = split_line[0], split_line[1].strip("\n")
            if header == "log file location":
                self.log_file_path = val
            elif header == "database configuration file location":
                self.db_config_file_path = val
            elif header == "max trial length":
                self.max_trial_length = int(val)
            elif header == "max number of successive trials":
                self.max_successive_trials = int(val)
            elif header == "database section":
                self.db_section = val
        f.close()

    def parse_ports(self):
        self.input_ports, self.input_events_names, self.output_ports, self.output_events_names = [], [], [], []
        for i in range(len(self.event_config)):
            e_id, name, port, in_out, dig_an, is_rew = self.event_config[i]
            if in_out == 'Input':
                self.input_ports.append(port)
                self.input_events_names.append(name)
            else:
                self.output_ports.append(port)
                self.output_events_names.append(name)
        pass

    @property
    def db_config_file_path(self):
        return self._db_config_file_path

    @db_config_file_path.setter
    def db_config_file_path(self, value):
        if self._db_config_file_path != value:
            self._db_config_file_path = value
            self.notifyPropertyChanged("db_config_file_path")

    # @property
    # def db_config_file_path(self):
    #     return self._db_config_file_path
    #
    # @db_config_file_path.setter
    # def db_config_file_path(self, value):
    #     if self._db_config_file_path != value:
    #         # if self.DB is None:
    #         #     self.DB = DB(value)
    #         #     self.connect_to_DB()
    #         self._db_config_file_path = value
    #     # self._log_file_path = "log.txt"
    #     self.notifyPropertyChanged("db_config_file_path")

    @property
    def max_trial_length(self):
        return self._max_trial_length

    @max_trial_length.setter
    def max_trial_length(self, value):
        if self._max_trial_length != value:
            self._max_trial_length = value
            self.notifyPropertyChanged("max_trial_length")

    @property
    def max_successive_trials(self):
        return self._max_successive_trials

    @max_successive_trials.setter
    def max_successive_trials(self, value):
        if self._max_successive_trials != value:
            self._max_successive_trials = value
            self.notifyPropertyChanged("max_successive_trials")

    @property
    def DB(self):
        return self._DB

    @DB.setter
    def DB(self, value):
        if self._DB != value:
            self._DB = value
            self.notifyPropertyChanged("DB")

    @property
    def subject_sessions(self):
        return self._subject_sessions

    @subject_sessions.setter
    def subject_sessions(self, value):
        if self._subject_sessions != value:
            self._subject_sessions = value
            self.notifyPropertyChanged("subject session update")

    @property
    def session_events(self):
        return self._session_events

    @session_events.setter
    def session_events(self, value):
        if self._session_events != value:
            self._session_events = value
            self.notifyPropertyChanged("session events changed")

    @property
    def curr_session(self):
        return self._curr_session

    @curr_session.setter
    def curr_session(self, value):
        if self._curr_session == value:
            return
        self._curr_session = value

    @property
    def trial_types(self):
        return self._trial_types

    @trial_types.setter
    def trial_types(self, value):
        if self._trial_types != value:
            self._trial_types = value
            # probably not needed
            self.notifyPropertyChanged("trial_types")

    @property
    def session_templates(self):
        return self._session_templates

    @session_templates.setter
    def session_templates(self, value):
        if self._session_templates != value:
            self._session_templates = value
            self.notifyPropertyChanged("session_templates")

    @property
    def session_trials(self):
        return self._session_templates

    @session_trials.setter
    def session_trials(self, value):
        if self._session_trials != value:
            self._session_trials = value
            self.notifyPropertyChanged("session_trials")

    @property
    def log_file_path(self):
        return self._log_file_path

    @log_file_path.setter
    def log_file_path(self, value):
        if self._log_file_path != value:
            self._log_file_path = value
            self.notifyPropertyChanged("log_file_path")

    @property
    def log_file(self):
        return self._log_file

    @log_file.setter
    def log_file(self, value):
        if self._log_file != value:
            self._log_file = value
            self.notifyPropertyChanged("log_file")

    def set_settings(self, log_file_path, db_file_path, db_section, max_successive_trials, max_length_trials,
                     events_config):
        # if a change occurred
        if log_file_path != self.log_file_path or db_file_path != self.db_config_file_path or \
                db_section != self.db_section or max_successive_trials != self.max_successive_trials or \
                max_length_trials != self.max_trial_length:
            file_str = "log file location=" + log_file_path + "\ndatabase configuration file location=" + \
                       db_file_path + "\ndatabase section=" + db_section + "\nmax number of successive trials=" + \
                       str(max_successive_trials) + "\nmax trial length=" + str(max_length_trials)
            f = open(self.settings_file, 'w', encoding='utf-8')
            f.write(file_str)
            f.close()
        if db_file_path != self.db_config_file_path or self.db_section != db_section:
            self.DB = DB(db_file_path, db_section)
            self.connect_to_DB()
        self.log_file_path = log_file_path
        self.db_config_file_path = db_file_path
        self.db_section = db_section
        self.max_trial_length = max_length_trials
        self.max_successive_trials = max_successive_trials
        if events_config is not None:
            for e in events_config:
                self.DB.insert_hardware_event(e[0], e[1], e[2], e[3], e[4])
        self.get_hardware_events_from_DB()
        pass

    def create_log_file(self):
        f_log, f_data = None, None
        try:
            f_log = open(self.log_file_path + "-log.txt", 'w', encoding='utf-8')
            f_data = open(self.log_file_path + "-input_data.csv", 'w', encoding='utf-8', newline='')
        except FileNotFoundError:
            self.notifyPropertyChanged("path not valid")
            # TODO raise error that this path doesn't exist

        self.log_file = f_log
        self.curr_session.log_file = f_log
        self.curr_session.data_log_file = f_data

    # find the trial type id by a name
    def find_trial_id_by_name(self, name: str):
        if self.trial_types is None:
            self.trial_types = self._DB.get_trial_types()
        # go over the trial types if exists
        if self.trial_types is not None:
            for trial in self.trial_types:
                # if the name of current type is the given name, return the id
                if trial.name == name:
                    return trial.trial_id
                # else notify no such trial
        else:
            # TODO error message that there are no types existing
            pass

    # find the trial type id by a name
    def find_trial_name_by_id(self, t_id: str):
        # go over the trial types if exists
        if self.trial_types is None:
            self.trial_types = self._DB.get_trial_types()
        if self.trial_types is not None:
            for trial in self.trial_types:
                # if the name of current type is the given name, return the id
                if trial[0] == t_id:
                    return trial[1]
            # else notify no such trial
        else:
            # extract from DB or send message that no such exist
            # TODO error message that there are no types existing
            pass

    # find the session template that matches the given data. if no match found, return -1
    def find_template(self, sess_name, exp_name, trials_def, iti_type, end_def, trials_order, iti_min, iti_max, iti_def,
                      total_num, block_size, blocks_ord, rnd_rew_prcnt):
        # first get list of templates from the DB
        if self.session_templates is None:
            self.get_templates_from_DB()

        # go over the templates
        for tmp in self.session_templates:
            # extract all data of current template
            t_sess_id, t_sess_name, t_exp_name, t_iti_type, t_iti_min, t_iti_max, t_iti_behave, t_end_def, t_end_val, \
            t_trials_order, t_total, t_block_sizes, t_blocks_ord, t_rnd_rew, date = tmp
            # if there is a template with the exact data, proceed to validate it's trials
            if t_exp_name == exp_name and t_sess_name == sess_name and t_iti_type == iti_type and (
                    t_end_def, t_end_val) == end_def and t_trials_order == trials_order and \
                    t_iti_min == iti_min and t_iti_max == iti_max and t_iti_behave == iti_def and \
                    t_total == total_num and t_block_sizes == str(block_size) and t_blocks_ord == str(blocks_ord) \
                    and t_rnd_rew == rnd_rew_prcnt:
                # get the trials of the given session_id
                trials = self._DB.get_session_trials(t_sess_id)
                # if the number of trials doesn't match - proceed to next template
                if len(trials) != len(trials_def.trials):
                    continue
                # validate that at least one trial exists
                if len(trials) != 0:
                    # set flag for match on
                    flag_found_match = True
                    # go over the trials
                    for i in range(len(trials)):
                        t = trials_def.trials[i]
                        # create a string list of the events in the trial
                        list_events = ""
                        for e in t.events:
                            list_events += str(self.find_event_id(type(e).__name__,
                                                                  e.get_params())) + ","
                        # create list of intervals for the trial
                        intvs = None
                        if trials[i][7] is not None:
                            intvs = create_intervals_list(trials[i][7])
                        # if the trial id, events and intervals match - proceed to next trial
                        # if t.trial_id == trials[i][2] and intvs == t.intervals and trials[i][6] == list_events:
                        if t.trial_id == trials[i][2] and intvs == [(int(a[0]), int(a[1])) for a in t.intervals] and \
                                trials[i][6] == list_events:
                            continue
                        # turn off the flag as a mismatch is found
                        flag_found_match = False
                        break  # TODO validate this
                    # if a total match was found return the template id
                    if flag_found_match:
                        return tmp[0]
        # no match was found - return -1
        return -1

    # fill out the given trials_def fields from the trial_types data
    def fill_trials_def(self, trials_def):
        types = self.trial_types
        if types is None:
            types = self.get_trial_types()

        type_events = None
        # validate integrity of value given
        for t in trials_def.trials:
            # validate id matches to name
            if t.name is not None:
                if t.trial_id is not None:
                    for i in types:
                        if i[1] == t.name:
                            if i[0] != t.trial_id:
                                # TODO error
                                pass
                            else:
                                type_events = i[2]
                                break
                        # TODO error not existing or create new type?

                        pass
                else:
                    # get trial_id by name
                    for i in types:
                        if i[1] == t.name:
                            t.trial_id = i[0]
                            type_events = i[2]
                            break
                    if t.trial_id is None:
                        # TODO error
                        pass
            elif t.trial_id is not None:
                # get name by id
                for i in types:
                    if t.trial_id == i.trial_id:
                        t.name = i.name
                        type_events = i.events
                if t.name is None:
                    # TODO error
                    pass
            else:
                # TODO error, no name and no id
                pass
            # convert type_events string to list
            type_events = type_events.split(",")[:-1]
            # validate intervals
            if len(t.events) != 1 and len(t.intervals) != (len(t.events) - 1):
                # TODO error
                pass
            # validate events
            if len(t.events) != len(type_events):
                # TODO error
                pass
            else:
                for i in range(len(t.events)):
                    if t.events[i].get_type_str() != type_events[i]:
                        # TODO error
                        pass

    def save_new_trial_type(self, name, events):
        if self.trial_types is None:
            self.get_trial_types_from_DB()
        # TODO maybe should validate events before
        # go over each type to check not existing
        for t_type in self.trial_types:
            # get data of current trial type
            t_id, t_name, t_events = t_type
            # if it matches the new trial type, ignore insertion
            if t_name == name and t_events == events:
                return
        type_id = self.DB.insert_trial_type(name, events)
        if type_id is None:
            # TODO error
            pass  # didnt work
        else:
            # update the local list of trial types
            self.trial_types.append((type_id, name, events))

    # save the template of the current created session
    def save_new_template(self):
        # make sure data is extracted from DB already
        if self.session_templates is None:
            self.get_templates_from_DB()
            self.get_trial_types_from_DB()

        # get parameters of current session
        sub_id, trials_def, iti, end_def, trials_order, sess_name, exp_name, rnd_rew_percent = \
            self.curr_session.get_params()
        # get iti data
        iti_type = "behaviour"
        iti_min, iti_max, iti_def = None, None, None
        if type(iti) == RandInterval:
            iti_type = "random"
            iti_min = iti.min_interval
            iti_max = iti.max_interval
        else:
            iti_def = iti.definition
        # get trial_def data
        total_trials, block_sizes, block_order = None, None, None
        if type(trials_def) == Trial.Trials_def_blocks:
            block_sizes = trials_def.block_sizes
            block_order = trials_def.blocks_order
        else:
            total_trials = trials_def.total_num
        # fill fields of trials_def
        self.fill_trials_def(trials_def)
        # validate no such template in the DB before inserting. if there is - only update the last_update for it
        sess_id = self.find_template(sess_name, exp_name, trials_def, iti_type, end_def, trials_order, iti_min, iti_max,
                                     iti_def, total_num=total_trials, block_size=block_sizes, blocks_ord=block_order,
                                     rnd_rew_prcnt=rnd_rew_percent)
        # if session not existing, insert into DB, and into the list of templates
        if sess_id == -1:
            # insert template session into db
            sess_id = self._DB.insert_session(iti_type, end_def[0], end_def[1], trials_order, iti_min, iti_max, iti_def,
                                              total_num=total_trials, block_size=block_sizes, blocks_ord=block_order,
                                              sess_name=sess_name, exp_name=exp_name, rnd_rew_percent=rnd_rew_percent)

            # insert trials_def with the given session_id
            i = 0
            for trial in trials_def.trials:
                trial_type_id = trial.trial_id
                event_list = ""  # maybe first insert the event list, then the trials with the created list
                for event in trial.events:
                    event_type = event.get_type_str()
                    params = event.get_params()  # string out the parameters of event
                    event_id = self._DB.insert_event(event_type, params)
                    event_list += str(event_id) + ","
                # insert current trial
                percent_in_session, percent_in_block, block_number = None, None, None  # get by type of def
                if type(trials_def) == Trial.Trials_def_blocks:
                    percent_in_block = np.array(trials_def.percent_per_block)[i].tolist()
                    block_number = trials_def.block_list
                else:
                    percent_in_session = trials_def.percent_list[i]
                # get the interval list
                interval_list = trial.intervals

                self._DB.insert_session_trials(sess_id, trial_type_id, percent_in_session,
                                               percent_in_block, block_number, event_list, interval_list)
                i += 1
        else:
            # session already exists, update the last date
            self.DB.update_session_date(sess_id)
        # insert subject session
        self.DB.insert_subject_session(sub_id, sess_id)
        # update lists from the DB insertion
        self.get_templates_from_DB()

    # set the current session to be as the following temp id
    def choose_template_from_list(self, temp_id):
        for tmp in self.session_templates:
            if tmp[0] == temp_id:
                # extract all data
                t_sess_id, t_sess_name, t_exp_name, t_iti_type, t_iti_min, t_iti_max, t_iti_behave, t_end_def, \
                    t_end_val, t_trials_order, t_total, t_block_sizes, t_blocks_ord, t_rnd_rew, date = tmp
                # set data into curr_session fields
                self.curr_session.session_id = t_sess_id
                self.curr_session.session_name = t_sess_name
                self.curr_session.experimenter_name = t_exp_name
                self.curr_session.rnd_reward_percent = t_rnd_rew
                break

    def choose_template(self, temp: SessionTemplate):
        # set the current session to be the given one
        self.curr_session.super = temp

    # connect to the path, info is located in the given file path
    def connect_to_DB(self, path=None):
        if self.DB is None:
            # establish connection with the given info in path
            self.DB = DB(path)
        self.DB.connect(self._DB.db_conf)

    def get_templates_from_DB(self):
        self.session_templates = self._DB.get_session_templates()
        self.session_trials = self._DB.get_all_session_trials()
        self.session_events = self._DB.get_all_events()
        self.subject_sessions = self._DB.get_all_subject_sessions()

    def get_trial_types_from_DB(self):
        self._trial_types = self._DB.get_trial_types()

    def get_trial_types(self):
        if self.trial_types is None:
            self.get_trial_types_from_DB()
        return self.trial_types

    # find id of event of given type and parameters
    def find_event_id(self, event_type, parameters):
        # get events
        all_events = self.DB.get_all_events()
        for i in range(len(all_events)):
            if all_events[i][2] == parameters:
                if all_events[i][1] == event_type:
                    return all_events[i][0]

    # get the type of the given event id
    def get_event_type_by_id(self, event_id):
        # get events
        all_events = self._DB.get_all_events()
        for i in range(len(all_events)):
            if all_events[i][0] == int(event_id):
                return all_events[i][1]

    def get_events(self, event_list):
        # get events
        all_events = self._DB.get_all_events()
        event_list = event_list.split(",")[:-1]
        list_TrialEvents = []
        for e in event_list:
            for i in range(len(all_events)):
                if all_events[i][0] == int(e):
                    class_str = "Models.TrialEvents." + all_events[i][1]
                    try:
                        module_path, class_name = class_str.rsplit('.', 1)
                        module = import_module(module_path)
                        kclass = getattr(module, class_name)
                        event = kclass()
                    except (ImportError, AttributeError):
                        raise ImportError(class_str)
                    params = all_events[i][2]
                    event.set_params(params)

                    list_TrialEvents.append(event)
                    break
        return list_TrialEvents

    # get trials def for the given session id
    def get_trials_def_for_sess(self, sess_id, order):
        # TODO make sure working for blocks!!!!!
        # get the trials for the given session id
        trials_for_sess = self.DB.get_session_trials(sess_id)
        list_trials, list_percent, block_list, percent_per_block, block_sizes, block_ord = [], [], [], [], [], []
        block_names = None
        # go over the trials
        for t in trials_for_sess:
            # extract data of the current trial
            s_t_id, sess_id, trial_type_id, percent_in_sess, percent_in_block, block_num, event_list, intervals = t
            # parse intervals
            intervs = None
            if intervals is not None:
                intervs = create_intervals_list(intervals)
            # crate the trial object
            t_model = TrialModel(t_id=trial_type_id, name=self.find_trial_name_by_id(trial_type_id),
                                 events=self.get_events(event_list),
                                 inters=intervs)
            # add trial to the list
            list_trials.append(t_model)
            # add specific data for order
            if order == "random":
                list_percent.append(percent_in_sess)
            else:
                prcnt_list = list(percent_in_block.replace("{", "").replace("}", "").split(","))
                percent_per_block.append([int(val) for val in prcnt_list])
                block_names = block_num  # this is same for all trials, so only once is necessary
        # crete the appropriate trials_def
        if order == "random":
            return Trial.Trials_def_rand(trial_list=list_trials, percent_list=list_percent)
        block_list = block_names.replace("{", "").replace("}", "").split(",")
        return Trial.Trials_def_blocks(trial_list=list_trials, block_list=block_list, prcnt_per_block=percent_per_block)

    def get_list_trials_types_def(self):  # TODO change
        trials = OrderedDict()
        if self._trial_types is None:
            self.get_trial_types_from_DB()
        for trial in self._trial_types:
            # trial_id = trial[0]
            name = trial[1]
            events = trial[2].split(",")[:-1]
            event_dict = OrderedDict()
            # param_list = []
            intervals_count = 0
            intervals_params = ["min", "max"]
            for e in events:
                # get event type, then get it's parameters
                class_str = "Models.TrialEvents." + e
                try:
                    module_path, class_name = class_str.rsplit('.', 1)
                    module = import_module(module_path)
                    kclass = getattr(module, class_name)

                    # param_list.extend(kclass.get_list_params())
                    param_list = kclass.get_list_params()
                    # check if same type exists:
                    if e in event_dict.keys():  # this kind of event already exists
                        # find the maximum of this kind of event
                        max_num = 1
                        for key in event_dict.keys():
                            if e in key:
                                # split string to get number
                                tmp = key.split("#")
                                if len(tmp) == 1:
                                    continue
                                # get the maximum
                                if int(tmp[1]) > max_num:
                                    max_num = int(tmp[1])
                        max_num += 1
                        e = e + "#" + str(max_num)
                    if intervals_count > 0:
                        if intervals_count == 1:
                            event_dict["interval"] = intervals_params
                        else:
                            event_dict["interval#" + str(intervals_count)] = intervals_params
                    event_dict[e] = param_list
                    intervals_count += 1

                except (ImportError, AttributeError):
                    raise ImportError(class_str)

            trials[name] = event_dict
        return trials

    def get_trial_names(self):
        trials = []
        for trial in self._trial_types:
            trials.append(trial[1])
        return trials

    def get_last_session_for_subject(self, sub_id):
        for temp in self._session_templates:
            if temp.subject_id == sub_id:
                return temp

    def disconnect_from_DB(self):
        self.DB.disconnect()

    def connect_to_devices(self):
        # go over devices and establish connection
        # raise error if connection fails
        pass

    def connect_to_systems(self):
        # for system in self._connected_systems:
        #     # establish connection
        #     # raise error if fails
        #     pass
        pass

    def check_connection(self, device):
        pass

    def pause_sess(self):
        self.curr_session.pause = True
        self.notifyPropertyChanged("pause")

    def resume_sess(self):
        self.curr_session.pause = False
        self.notifyPropertyChanged("pause")

    def repeat_trial(self):
        self.curr_session.repeat_same_trial()

    # def collect_input_data(self):
    #     hardware_communication.collect_input_data(self.input_ports)

    def get_reward_list_for_session(self):
        list_reward = []
        for t in self.curr_session.trials_def.trials:
            for e in t.events:
                if e.is_reward():
                    list_reward.append(e)
        list_reward = list(set(list_reward))
        return list_reward

    def get_reward_name_list_for_session(self):
        list_reward = []
        for t in self.curr_session.trials_def.trials:
            for e in t.events:
                if e.is_reward():
                    list_reward.append(e.get_type_str())
        list_reward = list(set(list_reward))
        return list_reward

    def give_reward(self, name):
        self.curr_session.give_reward(name)

    # start the current session
    def start_Session(self):
        if self._curr_session is None:
            return
        self.curr_session.end_session = False
        self.log_file_path = self.log_file_path + "/" + datetime.now().strftime(
            "%m_%d_%Y, %H_%M_%S") + "," + self.curr_session.experimenter_name + "," + self.curr_session.subject_id
        while self.log_file is None:
            self.create_log_file()
        self.curr_session.input_ports = self.input_ports
        self.curr_session.output_ports = self.output_ports
        self.curr_session.output_events_name_list = self.output_events_names
        self.curr_session.input_events_name_list = self.input_events_names

        # get list of rewards in session
        self.curr_session.reward_list_in_sess = self.get_reward_list_for_session()

        # create and start running the different threads
        # save template
        save_tmp = threading.Thread(target=self.save_new_template())
        save_tmp.start()
        # run trials
        run_trials = threading.Thread(target=self.curr_session.run_session,  # run the trials
                                      args=(self.log_file, self.max_successive_trials, self.max_trial_length))
        run_trials.start()

        #     # start sending TTL to all connected systems
        #     self._curr_session.run_session()
        #     # start the running session object
        #     # maybe create threads - one for keeping track of time,
        #     #   other to collect data from devices
        #     #   other to send data to devices
        #     #   other send data to log file
        #     # if end requirement fulfilled
        #     # stop TTL to devices
        #     # save end timer
        #     #    sess.is_end = True
        #     # thread sleep for a few milliseconds:?
        #     pass

        save_tmp.join()  # make sure that template was saved before finishing
        run_trials.join()  # wait for all trials to be finished
        # close data aquiring and log file
        self.log_file.close()
        self.curr_session.data_log_file.close()
        self.is_running_session = False
        self.notifyPropertyChanged("is_running_session")

    def end_Session(self):
        self._curr_session.end_session = True
        self.is_running_session = False
        self.notifyPropertyChanged("end_session")
        # manually stop session
        # stop sending TTl signal to all connected systems
        pass

    def log_data(self):
        # use the path to save all details in the specific format
        pass

    def add_trial_type(self, name, events):
        # before adding the trial type, check that name or list of events is not already in it
        events_str = ""
        for e in events:
            events_str += e + ","
        type_id = self._DB.insert_trial_type(name, events_str)
        if type_id is None:
            pass  # didnt work
        else:
            self.get_trial_types_from_DB()

    def get_behaviors_list(self):
        return self.input_events_names

    def get_end_def_list(self):
        return ["Time passed (seconds)", "Number of trials", "Success rate"]

    def set_iti(self, iti_type, iti_min, iti_max, behave):
        if iti_type == "random":
            self.curr_session.iti = RandInterval((iti_min, iti_max))
        else:
            self.curr_session.iti = BehaviourInterval(behave)

    def set_end_def(self, description, value):
        self.curr_session.end_def = (description, value)

    def set_trials_list(self, trials):
        self.curr_session.trials_def.trials = trials

    def set_trials_def(self, some_stuff):
        # TODO once the data from user is full
        pass

    def get_template_list_by_date_exp_sess_names(self):
        if self._session_templates is None:
            self.get_templates_from_DB()

        sess_dict = OrderedDict()
        for tmp in self.session_templates:
            sess_id, exp_name, sess_name, last_use = tmp[0], tmp[2], tmp[1], tmp[14]
            label = ""
            label += str(sess_id) + ": "
            label += exp_name + ", "
            label += sess_name + ", "
            label += str(last_use)
            sess_dict[sess_id] = label
        return sess_dict

    def get_template_list_by_subject(self, sub_id):
        # when getting this, should last used showing is last run of experiment in general, or for specific animal?
        if self._session_templates is None:
            self.get_templates_from_DB()
        # get list of session id's for the subject
        subject_list = self._DB.get_all_sess_for_subject(sub_id)
        subject_list = [tmp[1] for tmp in subject_list]
        sess_dict = OrderedDict()
        tmplts = [tmp for tmp in self.session_templates if tmp[0] in subject_list]
        for tmp in tmplts:
            sess_id, exp_name, sess_name, last_use = tmp[0], tmp[2], tmp[1], tmp[14]
            label = ""
            label += str(sess_id) + ": "
            label += exp_name + ", "
            label += sess_name + ", "
            label += str(last_use)
            sess_dict[sess_id] = label
        return sess_dict

    def get_list_of_subjects(self):
        # check if not Null
        self.subject_sessions = self._DB.get_all_subject_sessions()
        return list(set([sub[0] for sub in self.subject_sessions]))

    def get_data_for_template_id(self, sess_id):
        if self._session_templates is None:
            self.get_templates_from_DB()
        chosen_tmp = None
        for tmp in self.session_templates:
            if tmp[0] == sess_id:
                chosen_tmp = tmp
        return chosen_tmp

    def create_trial_list(self, trial_list: list):
        trial_type_idx = 0
        t_list = []
        # run over list of trials
        for t in trial_list:
            t_name = list(t.keys())[0]
            t_events = list(t.values())[0]
            events = []
            intervs = []
            # find trial type
            for i in range(len(self.trial_types)):
                # if self.trial_types[i][1] == list(t.keys())[0]:
                if self.trial_types[i][1] == t_name:
                    trial_type_idx = i
                    break
            try:
                for e_type, e_params in t_events.items():
                    e_type = e_type.split("#")[0]
                    # e_params = self.create_str_from_dict(e_params)
                    if e_type == "interval":
                        intervs.append((e_params["min"], e_params["max"]))
                        continue
                    else:
                        e_params = create_str_from_dict(e_params)
                    # create object of type e_type
                    class_str = "Models.TrialEvents." + e_type
                    try:
                        module_path, class_name = class_str.rsplit('.', 1)
                        module = import_module(module_path)
                        kclass = getattr(module, class_name)
                        event = kclass()
                    except (ImportError, AttributeError) as e:
                        raise ImportError(class_str)
                    event.set_params(e_params)
                    events.append(event)
                    # set parameters
            except Exception as e:  # didnt find a matching trial
                pass
            t_list.append(TrialModel(t_id=self.trial_types[trial_type_idx][0], name=self.trial_types[trial_type_idx][1],
                                     events=events, inters=intervs))
            # create a new trial of such type
            # go over events and set parameters
        return t_list

    def delete_templates_by_subject_name(self, sub_name):
        if self.session_templates is None:
            self.get_templates_from_DB()
        relevant_sessions = self.DB.get_all_sess_for_subject(sub_name)
        # check for each session that it is not used for different subject
        for sess in relevant_sessions:
            found_another_subj = False
            for subject in self.subject_sessions:
                sub_id, sess_id, count, last_used = subject
                # if not the current session, skip it
                if sess_id != sess[0]:
                    continue
                # if different subject, then skip it.
                if sub_id == sub_name:
                    continue
                if sub_id != sub_name:
                    found_another_subj = True
                    break
            if found_another_subj:
                # delete only the subject_session row
                self.DB.delete_subject_session(sub_name, sess[0])
                pass
            else:
                self.delete_template_from_DB_by_id(sess[0])

    # TODO verify
    def delete_templates_by_experimenter_name(self, exp_name):
        if self.session_templates is None:
            self.get_templates_from_DB()
        # go over each template and delete it if matches experimenter_name
        for tmp in self.session_templates:
            t_sess_id, t_sess_name, t_exp_name, t_iti_type, t_iti_min, t_iti_max, t_iti_behave, t_end_def, t_end_val, t_trials_order, t_total, t_block_sizes, t_blocks_ord, t_rnd_rew, date = tmp
            if t_exp_name == exp_name:
                self.delete_template_from_DB_by_id(t_sess_id)
        # update the local data
        self.get_templates_from_DB()
        pass

    # TODO verify
    def delete_template_from_DB_by_id(self, temp_id):
        # maybe verify authorization before?
        self.DB.delete_template(temp_id)

    # validate this
    def insert_trial_type(self, name, events):
        # find trial id
        type_id = self.DB.insert_trial_type(name, events)

    # validate this
    def update_trial_type(self, name, new_name, new_events):
        # find trial id
        for t in self.trial_types:
            t_id, t_name, t_events = t
            if t_name == name:
                self.DB.update_trial_type(t_id, new_name, new_events)

    def delete_trial_type(self, name):
        val = -1
        # find trial id
        for t in self.trial_types:
            t_id, t_name, t_events = t
            if t_name == name:
                val = self.DB.delete_trial_type(t_id)
        return val

    def get_event_list_for_sess(self):
        list_events = []
        # get output events
        # for t in self.curr_session.trials_def.trials:
        #     events_list = t.events_str().split(",")[:-1]
        #     for e in events_list:
        #         list_events.append(e)
        # # get input events
        # # for now - this is hardcoded
        # list_events.append("Lick")
        # list_events.append("Run")
        for e in self.input_events_names:
            list_events.append(e)
        for e in self.output_events_names:
            list_events.append(e)
        # return list(set(list_events))
        return list_events

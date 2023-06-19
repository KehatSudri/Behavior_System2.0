import os.path
import sys
from pathlib import Path
import threading
from collections import OrderedDict
from datetime import datetime
from importlib import import_module

import numpy as np
import logging

import Models.Trial_Model as Trial
from Models.DB_INIT import DB
from Models.Session_Model import BehaviourInterval, SessionTemplate
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


class BehaviorSystemModel:
    def __init__(self, settings_file=None):
        super(BehaviorSystemModel, self).__init__()
        # settings
        self.settings_file = None
        self.db_config_file_path = None
        if settings_file is not None:
            self.settings_file = settings_file
        else:
            config_path = str(Path(__file__).parent.parent / 'config_files')
            log_path = str(Path(__file__).parent.parent / 'logs')
            database_path = config_path + '/database.ini'
            settings_path = config_path + '/settings.txt'
            if not os.path.exists(config_path):
                os.makedirs(config_path)
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            if not os.path.exists(database_path):
                with open(database_path, 'x') as f:
                    f.write('[postgresql]\nhost=localhost\ndatabase=Behavior_sys\nuser=postgres\npassword=doc417')
            if not os.path.exists(settings_path):
                with open(settings_path, 'x') as f:
                    f.write(
                        f'log file location={log_path}\nmax number of successive trials=100\nmax trial length=60000')
            self.settings_file = settings_path
            self.db_config_file_path = database_path

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
        self.max_successive_trials = 0
        self.max_trial_length = 0
        self.logs_path = ""
        self.parse_settings_file()

        # DB
        self.db = DB(self.db_config_file_path)  # add connection to the DB

        self._trial_types = None
        self._session_templates = None
        self._session_trials = None
        self._subject_sessions = None
        self._session_events = None
        self.get_templates_from_db()
        self.get_trial_types_from_db()
        self.get_hardware_events_from_DB()

    # we need this
    def parse_settings_file(self):
        with open(self.settings_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line == "\n":
                    pass
                split_line = line.split("=")
                header, val = split_line[0], split_line[1].strip("\n")
                if header == "log file location":
                    self.logs_path = val
                elif header == "max trial length":
                    try:
                        self.max_trial_length = int(val)
                    except Exception:
                        logging.error(f'value "{val}" in "max trial length" is not a number')
                        sys.exit()
                elif header == "max number of successive trials":
                    try:
                        self.max_successive_trials = int(val)
                    except Exception:
                        logging.error(f'value "{val}" in "max number of successive trials" is not a number')
                        sys.exit()

    def get_hardware_events_from_DB(self):
        self.event_config = self.db.get_hardware_events()
        # self.parse_ports()
        return self.event_config

    def get_all_events_by_name(self):
        events_names = self.db.get_hardware_events_byname()
        return events_names

    def insert_hardware_event_to_DB(self, port, name, type, format, is_reward):
        return self.db.insert_hardware_event(port, name, type, format, is_reward)
        # self.get_hardware_events_from_DB()

    @property
    def subject_sessions(self):
        return self._subject_sessions

    @subject_sessions.setter
    def subject_sessions(self, value):
        if self._subject_sessions != value:
            self._subject_sessions = value

    @property
    def session_events(self):
        return self._session_events

    @session_events.setter
    def session_events(self, value):
        if self._session_events != value:
            self._session_events = value

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

    @property
    def session_templates(self):
        return self._session_templates

    @session_templates.setter
    def session_templates(self, value):
        if self._session_templates != value:
            self._session_templates = value

    @property
    def session_trials(self):
        return self._session_templates

    @session_trials.setter
    def session_trials(self, value):
        if self._session_trials != value:
            self._session_trials = value

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
            self.get_templates_from_db()

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

    # save the template of the current created session
    def save_new_template(self):
        # make sure data is extracted from DB already
        if self.session_templates is None:
            self.get_templates_from_db()
            self.get_trial_types_from_db()

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
            self.db.update_session_date(sess_id)
        # insert subject session
        self.db.insert_subject_session(sub_id, sess_id)
        # update lists from the DB insertion
        self.get_templates_from_db()

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

    def get_templates_from_db(self):
        self.session_templates = self.db.get_session_templates()
        self.session_trials = self.db.get_all_session_trials()
        self.session_events = self.db.get_all_events()
        self.subject_sessions = self.db.get_all_subject_sessions()

    def get_trial_types_from_db(self):
        return self.db.get_trial_types()

    def is_contingent(self, event, trial):
        return self.db.is_contingent(event, trial)

    def is_input_event(self, event):
        return self.db.is_input_event(event)

    def get_trial_types(self):
        if self.trial_types is None:
            self.get_trial_types_from_db()
        return self.trial_types

    # find id of event of given type and parameters
    def find_event_id(self, event_type, parameters):
        # get events
        all_events = self.db.get_all_events()
        for i in range(len(all_events)):
            if all_events[i][2] == parameters:
                if all_events[i][1] == event_type:
                    return all_events[i][0]

    # get the type of the given event id
    def get_event_type_by_id(self, event_id):
        # get events
        all_events = self.db.get_all_events()
        for i in range(len(all_events)):
            if all_events[i][0] == int(event_id):
                return all_events[i][1]

    def get_events(self, event_list):
        # get events
        all_events = self.db.get_all_events()
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
        trials_for_sess = self.db.get_session_trials(sess_id)
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
        trials = self.get_trial_types_from_db()
        trials_name_list = []
        for trial in trials:
            trials_name_list.append(trial[1])
        return trials_name_list

    def insert_session_to_DB(self, session_name, subject_id, experimenter_name, last_used, min_iti,
                             max_iti, is_fixed_iti, max_trial_time, notes):
        return self.db.insert_session(session_name, subject_id, experimenter_name, last_used, min_iti,
                                      max_iti, is_fixed_iti, max_trial_time, notes)

    def insert_session_to_trials(self, session_name, trial_name):
        return self.db.insert_session_to_trials(session_name, trial_name)

    def get_trials_names(self):
        return self.db.get_trial_names()

    def get_ports(self, trial_name):
        return self.db.get_ports(trial_name)

    def get_dependencies(self, trial_name):
        return self.db.get_dependencies(trial_name)

    def get_events_by_trial_name(self, trial):
        return self.db.get_events_by_trial_name(trial)

    def get_last_session_for_subject(self, sub_id):
        for temp in self._session_templates:
            if temp.subject_id == sub_id:
                return temp

    def disconnect_from_DB(self):
        self.db.disconnect()

    def pause_sess(self):
        self.curr_session.pause = True

    def resume_sess(self):
        self.curr_session.pause = False

    def get_reward_list_for_session(self):
        list_reward = []
        for t in self.curr_session.trials_def.trials:
            for e in t.events:
                if e.is_reward():
                    list_reward.append(e)
        list_reward = list(set(list_reward))
        return list_reward

    def give_reward(self, name):
        self.curr_session.give_reward(name)

    def end_Session(self):
        self._curr_session.end_session = True
        self.is_running_session = False
        pass

    def insert_new_trial(self, name):
        self.db.insert_new_trial(name)

    def insert_new_events_to_trials(self, trial_name, event_name, is_contingent, contingent_on, isRandom,
                                    isEndCondition):
        self.db.insert_new_events_to_trials(trial_name, event_name, is_contingent, contingent_on, isRandom,
                                            isEndCondition)

    def verify_trial_insert(self, name, events):
        # before adding the trial type, check that name or list of events is not already in it
        events_str = ""
        for e in events:
            events_str += e + ","
        trials_names = self.db.get_trial_types_names(name)
        if trials_names is not None:
            return -1
        trials_events = self.db.get_trial_name_by_events(events_str)
        return trials_events

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
            self.get_templates_from_db()

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
            self.get_templates_from_db()
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
        self.subject_sessions = self.db.get_all_subject_sessions()
        return list(set([sub[0] for sub in self.subject_sessions]))

    def get_data_for_template_id(self, sess_id):
        if self._session_templates is None:
            self.get_templates_from_db()
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
            self.get_templates_from_db()
        relevant_sessions = self.db.get_all_sess_for_subject(sub_name)
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
                self.db.delete_subject_session(sub_name, sess[0])
                pass
            else:
                self.delete_template_from_db_by_id(sess[0])

    # TODO verify
    def delete_templates_by_experimenter_name(self, exp_name):
        if self.session_templates is None:
            self.get_templates_from_db()
        # go over each template and delete it if matches experimenter_name
        for tmp in self.session_templates:
            t_sess_id, t_sess_name, t_exp_name, t_iti_type, t_iti_min, t_iti_max, t_iti_behave, t_end_def, t_end_val, t_trials_order, t_total, t_block_sizes, t_blocks_ord, t_rnd_rew, date = tmp
            if t_exp_name == exp_name:
                self.delete_template_from_db_by_id(t_sess_id)
        # update the local data
        self.get_templates_from_db()
        pass

    # TODO verify
    def delete_template_from_db_by_id(self, temp_id):
        # maybe verify authorization before?
        self.db.delete_template(temp_id)

    def insert_new_trial(self, name):
        self.db.insert_new_trial(name)

    # validate this
    def update_trial_type(self, name, new_name, new_events):
        # find trial id
        for t in self.trial_types:
            t_id, t_name, t_events = t
            if t_name == name:
                self.db.update_trial_type(t_id, new_name, new_events)

    def delete_trial_type(self, name):
        self.db.delete_trial_type(name)

        # val = -1
        # # find trial id
        # for t in self.trial_types:
        #     t_id, t_name, t_events = t
        #     if t_name == name:
        #         val = self.db.delete_trial_type(t_id)
        # return val

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

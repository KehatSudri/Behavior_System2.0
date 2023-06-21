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
        return self.event_config

    def get_all_events_by_name(self):
        events_names = self.db.get_hardware_events_by_name()
        return events_names

    def insert_hardware_event_to_DB(self, port, name, type, format, is_reward):
        return self.db.insert_hardware_event(port, name, type, format, is_reward)

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


    def choose_template_from_list(self, temp_id):
        for tmp in self.session_templates:
            if tmp[0] == temp_id:
                t_sess_id, t_sess_name, t_exp_name, t_iti_type, t_iti_min, t_iti_max, t_iti_behave, t_end_def, \
                    t_end_val, t_trials_order, t_total, t_block_sizes, t_blocks_ord, t_rnd_rew, date = tmp
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
        self.subject_sessions = []

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

    def get_list_trials_types_def(self):
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

    def get_reward_list_for_session(self):
        list_reward = []
        for t in self.curr_session.trials_def.trials:
            for e in t.events:
                if e.is_reward():
                    list_reward.append(e)
        list_reward = list(set(list_reward))
        return list_reward

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
        self.subject_sessions = []
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

    def get_event_list_for_sess(self):
        list_events = []
        for e in self.input_events_names:
            list_events.append(e)
        for e in self.output_events_names:
            list_events.append(e)
        return list_events

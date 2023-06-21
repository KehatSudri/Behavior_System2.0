import time
from Models.Behavior_System_Model import BehaviorSystemModel
from ViewModels.Session_VM import SessionViewModel


class BehaviorSystemViewModel:
    def __init__(self):
        super(BehaviorSystemViewModel, self).__init__()
        self.model = BehaviorSystemModel()
        self.sessionVM = SessionViewModel()

    @property
    def is_running_session(self):
        return self.model.is_running_session

    @is_running_session.setter
    def is_running_session(self, value):
        self.model.is_running_session = value

    @property
    def curr_session(self):
        return self.model.curr_session

    @curr_session.setter
    def curr_session(self, value):
        self.model.curr_session = value

    @property
    def trial_types(self):
        return self.model.trial_types

    @trial_types.setter
    def trial_types(self, value):
        self.model.trial_types = value

    @property
    def output_events_names(self):
        return self.model.output_events_names

    @output_events_names.setter
    def output_events_names(self, value):
        self.model.output_events_names = value

    @property
    def input_events_names(self):
        return self.model.input_events_names

    @input_events_names.setter
    def input_events_names(self, value):
        self.model.input_events_names = value

    @property
    def event_config(self):
        return self.model.event_config

    @event_config.setter
    def event_config(self, value):
        self.model.event_config = value

    @property
    def input_ports(self):
        return self.model.input_ports

    @input_ports.setter
    def input_ports(self, value):
        self.model.input_ports = value

    @property
    def session_templates(self):
        return self.model.session_templates

    @session_templates.setter
    def session_templates(self, value):
        self.model.session_templates = value

    @property
    def session_trials(self):
        return self.model.session_templates

    @session_trials.setter
    def session_trials(self, value):
        self.model.session_trials = value

    @property
    def log_file_path(self):
        return self.model.log_file_path

    @log_file_path.setter
    def log_file_path(self, value):
        self.model.log_file_path = value

    @property
    def db_section(self):
        return self.model.db_section

    @db_section.setter
    def db_section(self, value):
        self.model.db_section = value

    @property
    def db_config_file_path(self):
        return self.model.db_config_file_path

    @db_config_file_path.setter
    def db_config_file_path(self, value):
        self.model.db_config_file_path = value

    @property
    def max_trial_length(self):
        return self.model.max_trial_length

    @max_trial_length.setter
    def max_trial_length(self, value):
        self.model.max_trial_length = value

    @property
    def max_successive_trials(self):
        return self.model.max_successive_trials

    @max_successive_trials.setter
    def max_successive_trials(self, value):
        self.model.max_successive_trials = value

    def choose_template_from_list(self, tmp_id):
        self.model.choose_template_from_list(tmp_id)

    def get_reward_list_for_session(self):
        return self.model.get_reward_list_for_session()

    def get_trial_names(self):
        return self.model.get_trials_names()

    def get_ports(self, trial_mame):
        return self.model.get_ports(trial_mame)

    def get_dependencies(self, trial_mame):
        return self.model.get_dependencies(trial_mame)

    def get_list_trials_types_def(self):
        return self.model.get_list_trials_types_def()

    def get_list_trials_names(self):
        return self.model.get_trials_names()

    def get_events_by_trial_name(self, trial):
        return self.model.get_events_by_trial_name(trial)

    def get_behaviors_list(self):
        return self.model.get_behaviors_list()

    def get_end_def_list(self):
        return self.model.get_end_def_list()

    def set_iti(self, type, min, max, behave):
        self.model.set_iti(type, min, max, behave)

    def set_end_def(self, description, value):
        self.model.set_end_def(description, value)

    def set_trials_list(self, trials):
        self.model.set_trials_list(trials)

    def get_template_list_by_date_exp_sess_names(self):
        return self.model.get_template_list_by_date_exp_sess_names()

    def get_template_list_by_subject(self, sub_id):
        return self.model.get_template_list_by_subject(sub_id)

    def get_data_for_template_id(self, sess_id):
        return self.model.get_data_for_template_id(sess_id)

    def get_list_of_subjects(self):
        return self.model.get_list_of_subjects()

    def create_trial_list(self, trial_list: list):
        return self.model.create_trial_list(trial_list)

    def get_event_list_for_sess(self):
        return self.model.get_event_list_for_sess()

    def insert_new_trial(self, name):
        self.insert_new_trial(name)

    def set_settings(self, log_file_path, db_file_path, db_section, max_successive_trials, max_length_trials,
                     e_2_p=None):
        self.model.set_settings(log_file_path, db_file_path, db_section, max_successive_trials, max_length_trials,
                                e_2_p)

    def insert_hardware_event_to_DB(self, port, name, type, format, is_reward):
        return self.model.insert_hardware_event_to_DB(port, name, type, format, is_reward)

    def insert_session_to_DB(self, session_name, subject_id, experimenter_name, last_used, min_iti,
                             max_iti, is_fixed_iti, max_trial_time, notes):
        return self.model.insert_session_to_DB(session_name, subject_id, experimenter_name, last_used, min_iti,
                                               max_iti, is_fixed_iti, max_trial_time, notes)

    def insert_session_to_trials(self, session_name, trial_name):
        return self.model.insert_session_to_trials(session_name, trial_name)

    def insert_new_trial(self, name):
        self.model.insert_new_trial(name)

    def insert_new_events_to_trials(self, trial_name, event_name, is_contingent, contingent_on, isRandom,
                                    isEndCondition):
        self.model.insert_new_events_to_trials(trial_name, event_name, is_contingent, contingent_on, isRandom,
                                               isEndCondition)

    def verify_trial_insert(self, name, events):
        return self.model.verify_trial_insert(name, events)

    # validate this
    def update_trial_type(self, name, new_name, new_events):
        self.model.update_trial_type(name, new_name, new_events)

    def delete_trial_type(self, name):
        return self.model.delete_trial_type(name)

    def delete_templates_by_subject_name(self, sub_name):
        self.model.delete_templates_by_subject_name(sub_name)

    def delete_templates_by_experimenter_name(self, exp_name):
        self.model.delete_templates_by_experimenter_name(exp_name)

    def is_contingent(self, event, trial):
        return self.model.is_contingent(event, trial)

    def is_input_event(self, event):
        return self.model.is_input_event(event)

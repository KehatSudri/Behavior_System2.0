import random
import time

from Models.Behavior_System_Model import BehaviorSystemModel
from Models.INotifyPropertyChanged import INotifyPropertyChanged
from ViewModels.Session_VM import SessionViewModel


# changed in Model currently changes properties in VM. make sure this change go through into view
class BehaviorSystemViewModel(INotifyPropertyChanged):
    def __init__(self):
        super(BehaviorSystemViewModel, self).__init__()
        self.model = BehaviorSystemModel()
        self.sessionVM = SessionViewModel()
        self.timer = None

    @property
    def is_running_session(self):
        return self.model.is_running_session

    @is_running_session.setter
    def is_running_session(self, value):
        self.model.is_running_session = value

    # @property
    # def data(self):
    #     return self.model.data
    #
    # @data.setter
    # def data(self, value):
    #     self.model.data = value

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
    def output_ports(self):
        return self.model.output_ports

    @output_ports.setter
    def output_ports(self, value):
        self.model.output_ports = value

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

    def give_reward(self, name):
        self.model.give_reward(name)

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

    def get_input(self):
        for i in range(5):
            time.sleep(5)
            self.model.curr_session.input_flag = True
            time.sleep(3)
            self.model.curr_session.input_flag = False

    def choose_template_from_list(self, tmp_id):
        self.model.choose_template_from_list(tmp_id)

    def get_reward_list_for_session(self):
        return self.model.get_reward_list_for_session()

    def get_reward_name_list_for_session(self):
        return self.model.get_reward_name_list_for_session()

    def start_Session(self):
        self.model.start_Session()
        if self.curr_session is not None:
            # notify all connected system with TTL signal
            # create timer for session etc.
            pass

    def end_Session(self):
        self.model.end_Session()
        # send TTl signal to all connected systems
        pass

    def pause_sess(self):
        self.model.pause_sess()

    def resume_sess(self):
        self.model.resume_sess()

    def repeat_trial(self):
        self.model.repeat_trial()

    def log_data(self):
        # use the path to save all details in the specific format
        pass

    def get_trial_names(self):
        return self.model.get_trials_names()

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

    def connect_to_DB(self):
        self.model.connect_to_DB()

    def get_template_list_by_date_exp_sess_names(self):
        return self.model.get_template_list_by_date_exp_sess_names()

    def get_template_list_by_subject(self, sub_id):
        return self.model.get_template_list_by_subject(sub_id)

    def get_data_for_template_id(self, sess_id):
        return self.model.get_data_for_template_id(sess_id)

    def get_list_of_subjects(self):
        return self.model.get_list_of_subjects()

    def get_trials_def_for_sess(self, sess_id, order):
        return self.model.get_trials_def_for_sess(sess_id, order)

    def create_trial_list(self, trial_list: list):
        return self.model.create_trial_list(trial_list)

    def get_event_list_for_sess(self):
        return self.model.get_event_list_for_sess()

    def insert_trial_type(self, name, events):
        self.insert_trial_type(name, events)

    def set_settings(self, log_file_path, db_file_path, db_section, max_successive_trials, max_length_trials,
                     e_2_p=None):
        self.model.set_settings(log_file_path, db_file_path, db_section, max_successive_trials, max_length_trials,
                                e_2_p)

    def insert_hardware_event_to_DB(self, name, port, in_out, dig_an, is_rew):
        self.model.insert_hardware_event_to_DB(name, port, in_out, dig_an, is_rew)

    def verify_insert_hardware_event(self, name, port, in_out, dig_an, is_rew):
        return self.model.verify_insert_hardware_event(name, port, in_out, dig_an, is_rew)

    def add_trial_type(self, name, events):
        self.model.add_trial_type(name, events)

    def events_to_trials(self, trial_name, event_name, is_contingent, contingent_on):
        self.model.events_to_trials(trial_name, event_name, is_contingent, contingent_on)

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

    # select to notify only events that are relevant
    def SystemVMEventHandler(self, sender, *event_args):
        if type(sender) != BehaviorSystemModel:
            self.is_running_session = sender.is_running_session
        if event_args[0][0] == "is_running_session":
            # change the property
            # self.is_running_session = self.model.is_running_session #is this necessary or it updates on its own
            self.notifyPropertyChanged("VM_" + event_args[0][0])
    def is_contingent(self, event,trial):
        return self.model.is_contingent(event,trial)


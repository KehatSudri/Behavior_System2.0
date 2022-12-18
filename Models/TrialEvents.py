import time
from abc import ABC, abstractmethod


class InputEvent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_type_str(self):
        pass


class Lick(InputEvent):
    def __init__(self):
        super(Lick, self).__init__()

    @classmethod
    def get_type_str(cls):
        return "Lick"


class Run(InputEvent):
    def __init__(self):
        super(Run, self).__init__()

    @classmethod
    def get_type_str(cls):
        return "Run"


class TrialEvent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def is_reward(self):
        return False

    @abstractmethod
    def getDuration(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_type_str(self):
        pass

    @abstractmethod
    def get_params(self):
        pass


class ContingentEvent(TrialEvent):
    def __init__(self=None, interval_from_input=None,con_event=None, want_event=None, want_time_rng=None, no_want_event=None,

                 no_want_time_rng=None):
        super(ContingentEvent, self).__init__()
        self.interval_from_input = interval_from_input
        self.conditioned_e = con_event
        self.want_e = want_event
        self.want_t_rng = want_time_rng
        self.n_want_e = no_want_event
        self.n_want_t_rng = no_want_time_rng


    @abstractmethod
    def get_type_str(self):
        return "contingent " + self.conditioned_e.get_type_str()

    @abstractmethod
    def get_params(self):
        "conditioned-" + self.conditioned_e.get_params() + ",wanted-" + self.want_e.get_params() + ",in-" + str(
            self.want_t_rng) + ",not_wanted-" + self.n_want_e.get_params() + ",in-" + str(self.n_want_t_rng)
        pass

    @abstractmethod
    def is_reward(self):
        return self.conditioned_e.is_reward()

    @abstractmethod
    def getDuration(self):
        return self.conditioned_e.getDuration()

    @abstractmethod
    def execute(self):
        pass


class Light(TrialEvent):
    def __init__(self, dur=None):
        super(Tone, self).__init__()
        self.light_duration = dur  # ms

    @classmethod
    def is_reward(cls):
        return False

    def getDuration(self):
        return self.light_duration

    def setValues(self, light_dur=None):
        if light_dur is not None:
            self.light_duration = light_dur

    @classmethod
    def execute(cls):
        print("Light start")
        time.sleep(1)
        print("Light end")
        pass

    @classmethod
    def get_type_str(cls):
        return "Light"

    @classmethod
    def get_list_params(cls):
        return ['light_duration']


class Tone(TrialEvent):
    def __init__(self, dur=None, amp=None, freq=None, num_rep=None, time_between_rep=None):
        super(Tone, self).__init__()
        self.tone_duration = dur  # ms
        self.tone_amplitude = amp  # db
        self.tone_frequency = freq  # hz
        self.tone_num_of_repetitions = num_rep
        self.tone_time_between_repetitions = time_between_rep  # hz TODO convert to ms time between reps

    @classmethod
    def is_reward(cls):
        return False

    def getDuration(self):
        return self.tone_duration

    def setValues(self, tone_dur=None, tone_amp=None, tone_freq=None, num_rep=None, between_reps=None):
        if tone_dur is not None:
            self.tone_duration = tone_dur  # ms
        if tone_amp is not None:
            self.tone_amplitude = tone_amp  # db
        if tone_freq is not None:
            self.tone_frequency = tone_freq  # hz
        if num_rep is not None:
            self.tone_num_of_repetitions = num_rep
        if between_reps is not None:
            self.tone_time_between_repetitions = between_reps  # hz

    @classmethod
    def execute(cls):
        print("Tone start")
        time.sleep(1)
        print("Tone end")
        pass

    @classmethod
    def get_type_str(cls):
        return "Tone"

    def get_params(self):
        params = ""
        if self.tone_duration is not None:
            params += "tone_duration:" + str(self.tone_duration) + ","
        if self.tone_amplitude is not None:
            params += "tone_amplitude:" + str(self.tone_amplitude) + ","
        if self.tone_frequency is not None:
            params += "tone_frequency:" + str(self.tone_frequency) + ","
        if self.tone_num_of_repetitions is not None:
            params += "tone_num_of_repetitions:" + str(self.tone_num_of_repetitions) + ","
        if self.tone_time_between_repetitions is not None:
            params += "tone_time_between_repetitions:" + str(self.tone_time_between_repetitions) + ","
        return params

    @classmethod
    def get_list_params(cls):
        return ['tone_duration', 'tone_amplitude', 'tone_frequency', 'tone_num_of_repetitions',
                'tone_time_between_repetitions']

    def set_params(self, params_str: str):
        params_str = params_str.split(",")[:-1]
        dur, amp, freq, rep, btwn = None, None, None, None, None
        for i in range(len(params_str)):
            tmp = params_str[i].split(":")
            if tmp[0] == 'tone_duration':
                dur = tmp[1]
            elif tmp[0] == 'tone_amplitude':
                amp = tmp[1]
            elif tmp[0] == 'tone_frequency':
                freq = tmp[1]
            elif tmp[0] == 'tone_num_of_repetitions':
                rep = tmp[1]
            else:
                btwn = tmp[1]

        self.setValues(tone_dur=dur, tone_amp=amp, tone_freq=freq, num_rep=rep, between_reps=btwn)
        pass


class Reward(TrialEvent):
    def __init__(self, when_given=None, dur=None, percent=None):
        super(Reward, self).__init__()
        self.reward_state = None  # is valve open or close
        self.reward_when_given = when_given  # when will the reward be given
        self.reward_duration = dur  # duration of giving reward
        self.reward_percent_in_trials = percent  # the number is the percentage of trials where reward will be given

    @classmethod
    def is_reward(cls):
        return True

    def getDuration(self):
        return self.reward_duration

    def setValues(self, when_given=None, dur=None, percent=None, state=None):
        if state is not None:
            self.reward_state = state
        if when_given is not None:
            self.reward_when_given = when_given
        if dur is not None:
            self.reward_duration = dur
        if percent is not None:
            self.reward_percent_in_trials = percent

    def openValve(self):
        self.reward_state = True

    def closeValve(self):
        self.reward_state = False

    def execute(self):
        print("Reward start")
        time.sleep(1)
        print("Reward end")
        pass

    @classmethod
    def get_type_str(cls):
        return "Reward"

    def get_params(self):
        params = ""
        if self.reward_state is not None:
            params += "reward_state:" + self.reward_state + ","
        if self.reward_when_given is not None:
            params += "reward_when_given:" + self.reward_when_given + ","
        if self.reward_duration is not None:
            params += "reward_duration:" + str(self.reward_duration) + ","
        if self.reward_percent_in_trials is not None:
            params += "reward_percent_in_trials:" + str(self.reward_percent_in_trials) + ","
        return params

    @classmethod
    def get_list_params(cls):
        return ['reward_state', 'reward_when_given', 'reward_duration', 'reward_percent_in_trials']

    def set_params(self, params_str: str):
        params_str = params_str.split(",")[:-1]
        state, when, dur, per = None, None, None, None
        for i in range(len(params_str)):
            tmp = params_str[i].split(":")
            if tmp[0] == 'reward_state':
                state = tmp[1]
            elif tmp[0] == 'reward_when_given':
                when = tmp[1]
            elif tmp[0] == 'reward_duration':
                dur = tmp[1]
            else:
                per = tmp[1]
        self.setValues(when_given=when, dur=dur, percent=per, state=state)

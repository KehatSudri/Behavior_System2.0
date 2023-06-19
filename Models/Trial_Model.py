import random
import time
from abc import ABC, abstractmethod
import numpy as np

MAX_NUM_TRIALS_IN_SESS = 200
max_successive_trials = 30  # TODO this should be changable from system somehow


class Interval(ABC):
    @abstractmethod
    def get_iti_type(self):
        pass


class RandInterval(Interval):
    def __init__(self, interval_range):
        super(RandInterval, self).__init__()
        self.min_interval, self.max_interval = interval_range
        # self.iti_vec = np.random.randint(self.min_interval, self.max_interval, MAX_NUM_TRIALS_IN_SESS)
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
        # self.parameters = None  # is this relevant anymore? # dictionary that holds necessary parameters

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

    def run(self):

        intvs = self.get_intervals()
        for i in range(len(self.events)):
            if i == 0:
                self.events[i].execute()
                continue
            time.sleep(intvs[i - 1])
            self.events[i].execute()


class Trials_def(ABC):
    def __init__(self, trial_list: list):
        self.trials = trial_list

    @abstractmethod
    def get_trials_order(self):
        pass

    @abstractmethod
    def get_total_num(self):
        pass


def get_counters(percent_list, total):
    raw = [element * total / 100 for element in percent_list]
    counters = [int(element) for element in raw]
    reminder = np.subtract(raw, counters)
    left = total - sum(counters)
    for i in range(left):
        idx = np.where(reminder == max(reminder))
        counters[idx[0][0]] += 1
        reminder[idx[0]] = float("inf") * -1

    return counters


def find_idx_to_fit(trial_list, trial_idx, trial_ord_list, max_successive_trials=30):
    flag_not_found = True
    while flag_not_found:  # TODO maybe change to while 1
        rnd_idx = random.randint(0, len(trial_ord_list) - 1)
        count = 0
        # validate MAX_NUM before and after
        i = rnd_idx - 1
        while i >= 0 and trial_ord_list[i].name == trial_list[trial_idx].name:
            count += 1
            i -= 1
        i = rnd_idx
        while i < len(trial_ord_list) and trial_ord_list[i] == trial_list[trial_idx]:
            count += 1
            i += 1
        if count < max_successive_trials:
            return rnd_idx


def create_trial_def_rand(trial_list: list, percent_list: list = None, total=None):
    trial_def = None
    return trial_def


class Trials_def_rand(Trials_def):
    def __init__(self, trial_list: list, percent_list: list = None, total=None):
        super().__init__(trial_list)
        self.trial_list = trial_list
        self.total_num = total
        if percent_list is not None:
            if len(percent_list) != len(trial_list):
                # TODO raise an error
                pass
            if sum(percent_list) != 100:
                # TODO raise some error
                pass
        self.percent_list = percent_list

    def get_total_num(self):
        return self.total_num

    def get_trials_order(self, max_successive_trials=30):
        # create a list of counters for each trial by the given percentage
        counters = get_counters(self.percent_list, self.total_num)
        trials = []  # list of the trials for session
        valid_idxs = np.arange(len(self.trial_list))
        last_trial_idx = None
        trials_in_row_counter = 0
        # shouldn't be such, but remove unnecessary indexes
        for j in range(len(self.trial_list)):
            if counters[j] == 0:
                valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == j))

        # create a list of trials in total_num length
        for i in range(self.total_num):
            flag_add_trial = True
            stop_search = False  # stop flag for getting the next trial for list
            # generate a random index in the range
            rnd_idx = random.randint(0, len(valid_idxs) - 1)
            idx = valid_idxs[rnd_idx]
            # first trial is chosen
            if last_trial_idx is None:
                last_trial_idx = idx
            # not first, but same as last
            elif idx == last_trial_idx:
                # if arrived maximum of trials in a row
                if trials_in_row_counter >= max_successive_trials:
                    if len(valid_idxs) == 1:
                        # TODO validate that this can't get into infinite loop
                        to_fit = find_idx_to_fit(self.trial_list, idx, trials, max_successive_trials)
                        trials.insert(to_fit, self.trial_list[idx])
                        counters[idx] -= 1
                        if counters[idx] == 0:
                            valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == idx))
                        flag_add_trial = False
                    else:
                        while idx == last_trial_idx:
                            rnd_idx = random.randint(0, len(valid_idxs) - 1)
                            idx = valid_idxs[rnd_idx]
                        last_trial_idx = idx
                        trials_in_row_counter = 0
            else:
                last_trial_idx = idx
                trials_in_row_counter = 0
            if flag_add_trial:
                trials_in_row_counter += 1
                trials.append(self.trial_list[idx])
                counters[idx] -= 1
                if counters[idx] == 0:
                    valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == idx))

        return trials


class Trials_def_blocks(Trials_def):
    def __init__(self, trial_list: list, block_list: list = None, prcnt_per_block: list = None,
                 block_sizes: list = None, blocks_ord: list = None):
        super().__init__(trial_list)
        self.trial_list = trial_list
        # check that we have all required data
        if block_list is not None:
            if len(trial_list) != len(prcnt_per_block):
                # TODO error
                pass
            for i in range(len(prcnt_per_block)):
                if len(block_list) != len(prcnt_per_block[i]):
                    # TODO error
                    pass
        self.block_list = block_list  # holds for each block the trial types
        self.percent_per_block = prcnt_per_block  # holds percent of each trial for each block
        self.block_sizes = block_sizes  # total number of trials in a block
        self.blocks_order = blocks_ord  # the order of blocks to run in the session

    def get_total_num(self):
        sum = 0
        for block in self.blocks_order:
            # find index of blcok in block list
            for i in range(len(self.block_list)):
                if self.block_list[i] == block:
                    sum += self.block_sizes[i]
        return sum

    def get_trials_order(self, max_successive_trials=30):
        # create a list of lists. each list is a block, and inside are the trials for it
        trials = []  # list of list of trials for session
        last_trial_idx = None
        trials_in_row_counter = 0
        # go over each block
        for i in range(len(self.blocks_order)):
            # get index of the current block in the list of blocks
            block_idx = None
            for j in range(len(self.block_list)):
                if self.block_list[j] == self.blocks_order[i]:
                    block_idx = j
                    break
            if block_idx is None:
                # TODO exception
                pass
            # create list for the trials in the block
            trials_for_block = []
            # get a list of indexes for trials
            valid_idxs = np.arange(0, len(self.trial_list))
            # get number for each trial type
            # counters = get_counters(self.percent_per_block[block_idx], self.block_sizes[block_idx])
            counters = get_counters([self.percent_per_block[i][block_idx] for i in range(len(self.percent_per_block))],
                                    self.block_sizes[block_idx])
            # counters = [int(element * self.block_sizes[block_idx]/100) for element in self.percent_per_block[block_idx]]

            # run over the required quantities and delete indexes of non-relevant trials
            for j in range(len(counters)):
                if counters[j] == 0:
                    valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == j))
            # TODO should also take care of when same trial falls to many times in a row
            # create the list of trials
            for j in range(self.block_sizes[block_idx]):
                flag_add_trial = True
                # get a random index, in the range of valid indexes
                rand_idx = random.randint(0, len(valid_idxs) - 1)
                # the chosen trial index is as follows
                chosen_idx = valid_idxs[rand_idx]
                # first trial is chosen
                if last_trial_idx is None:
                    last_trial_idx = chosen_idx
                # not first, but same as last
                elif chosen_idx == last_trial_idx:
                    # if arrived maximum of trials in a row
                    if trials_in_row_counter >= max_successive_trials:
                        if len(valid_idxs) == 1:
                            # TODO validate that this can't get into infinite loop
                            # TODO validate that not a problem in seperated blocks
                            to_fit = find_idx_to_fit(self.trial_list, chosen_idx, trials_for_block,
                                                     max_successive_trials)
                            trials_for_block.insert(to_fit, self.trial_list[chosen_idx])
                            counters[chosen_idx] -= 1
                            if counters[chosen_idx] == 0:
                                valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == chosen_idx))
                            flag_add_trial = False
                        else:
                            while chosen_idx == last_trial_idx:
                                rnd_idx = random.randint(0, len(valid_idxs) - 1)
                                chosen_idx = valid_idxs[rnd_idx]
                            last_trial_idx = chosen_idx
                            trials_in_row_counter = 0
                else:
                    last_trial_idx = chosen_idx
                    trials_in_row_counter = 0
                if flag_add_trial:
                    trials_in_row_counter += 1
                    # append the chosen trial
                    trials_for_block.append(self.trial_list[chosen_idx])
                    # decrease counter of the chosen trial
                    counters[chosen_idx] -= 1
                    # if this trial is no longer necessary delete its index
                    if counters[chosen_idx] == 0:
                        valid_idxs = np.delete(valid_idxs, np.where(valid_idxs == chosen_idx))
            # append the list for block to the overall list
            trials.extend(trials_for_block)
        return trials

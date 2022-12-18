
from Models.Session_Model import SessionModel
from Models.TrialEvents import Tone, Reward
from Models.Trial_Model import TrialModel, RandInterval, Trials_def_rand, Trials_def_blocks
from ViewModels.Bahavior_System_VM import BehaviorSystemViewModel
from Models.Behavior_System_Model import BehaviorSystemModel
from Models.Session_Model import BehaviourInterval

def create_3_events():
    A = Tone(dur=5, amp=10, freq=50, num_rep=1, time_between_rep=0)
    B = Tone(dur=9, amp=30, freq=200, num_rep=3, time_between_rep=20)
    C = Reward(when_given='jump', dur=5, percent=100)
    return A, B, C


def create_5_trial_types():
    A = TrialModel(name='t', events=[Tone])
    B = TrialModel(name='r', events=[Reward])
    C = TrialModel(name='tr', events=[Tone, Reward])
    D = TrialModel(name="trt", events=[Tone, Reward, Tone])
    E = TrialModel(name='t', events=[Reward, Tone])
    F = TrialModel(name='x', events=[Tone])
    G = TrialModel(name='r', events=[Reward])
    H = TrialModel(name='rt', events=[Reward, Tone])
    return A, B, C, D, E, F, G, H


def create_trial_types(model):
    trial1, trial2, trial3, trial4, trial5, trial6, trial7, trial8 = create_5_trial_types()
    model.add_trial_type(trial1)
    model.add_trial_type(trial2)
    model.add_trial_type(trial3)
    model.add_trial_type(trial4)
    model.add_trial_type(trial5)
    model.add_trial_type(trial6)
    model.add_trial_type(trial7)
    model.add_trial_type(trial8)


def create_session1(model: BehaviorSystemModel):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.session_name = "אנטומי"
    sess.experimenter_name = "אנטולי"
    sess.subject_id = 'שלום העכבר'
    sess.iti = RandInterval((8, 12))
    sess.trials_order = 'random'
    sess.end_def = ('trials', 20)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_rand(trial_list=[t1, t2, t3], percent_list=[50, 50, 0], total=10)
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    # sess.session_id = model.save_new_template()

def create_session2(model):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.subject_id = 'A1'
    sess.session_name = "operant 2 tone"
    sess.experimenter_name = "tal levy"
    sess.iti = BehaviourInterval("lick")
    sess.trials_order = 'blocks'
    sess.end_def = ('time', 100)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_blocks(trial_list=[t1, t2, t3], block_list=['A','B'], prcnt_per_block=[[1, 33, 66], [50, 25, 25]], block_sizes=[10, 8], blocks_ord=['A', 'B', 'B', 'A'])
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    #sess.session_id = model.save_new_template()
def create_session22(model):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.subject_id = 'A1'
    sess.session_name = "operant 2 tone"
    sess.experimenter_name = "tal levy"
    sess.rnd_reward_percent = 50
    sess.iti = RandInterval((8, 30))
    sess.trials_order = 'blocks'
    sess.end_def = ('time', 100)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_blocks(trial_list=[t1, t2, t3], block_list=['A','B'], prcnt_per_block=[[1, 33, 66], [50, 25, 25]], block_sizes=[10, 8], blocks_ord=['A', 'B', 'B', 'A'])
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    #sess.session_id = model.save_new_template()
def create_session3(model: BehaviorSystemModel):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.session_name = "associative 2 choise"
    sess.experimenter_name ="Dana C"
    sess.subject_id = 'שלום העכבר'
    sess.iti = RandInterval((8, 12))
    sess.trials_order = 'blocks'
    sess.end_def = ('Success rate', 100)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(20, 25), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(30, 13)])
    sess.trials_def = Trials_def_rand(trial_list=[t1, t2, t3], percent_list=[50, 50, 0], total=10)
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    # sess.session_id = model.save_new_template()
def create_session4(model: BehaviorSystemModel):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.session_name = "no_rnd_rew"
    sess.experimenter_name = "Nici"
    sess.subject_id = 'B123'
    sess.rnd_reward_percent = 60
    sess.iti = RandInterval((100, 200))
    sess.trials_order = 'random'
    sess.end_def = ('Time passed', 1000)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_rand(trial_list=[t1, t2, t3], percent_list=[50, 25, 25], total=10)
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    # sess.session_id = model.save_new_template()

def create_session5(model: BehaviorSystemModel):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.session_name = "אנטומי"
    sess.experimenter_name = "אנטולי"
    sess.subject_id = 'שלום העכבר'
    sess.iti = RandInterval((8, 12))
    sess.trials_order = 'random'
    sess.end_def = ('trials', 20)
    t1 = TrialModel(name='t', events=[eventA])
    t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_rand(trial_list=[t1, t2, t3], percent_list=[50, 50, 0], total=10)
    # sess.trials_def.get_trials_order()
    # temps = model.get_list_templates()
    # sess.session_id = model.save_new_template()
def create_session6(model: BehaviorSystemModel):
    eventA, eventB, eventC = create_3_events()
    sess = model.curr_session
    sess.session_name = "XTones"
    sess.experimenter_name = "Dan El"
    sess.subject_id = 'שלום העכבר'
    sess.iti = RandInterval((8, 50))
    sess.trials_order = 'random'

    sess.end_def = ('trials', 20)
    t1 = TrialModel(name='t', events=[eventA])
    #t2 = TrialModel(name='trt', events=[eventA, eventC, eventB], inters=[(5, 10), (15, 20)])
    t3 = TrialModel(name='rt', events=[eventC, eventB], inters=[(12, 13)])
    sess.trials_def = Trials_def_rand(trial_list=[t1, t3], percent_list=[50, 50], total=10)
if __name__ == '__main__':
    systemM = BehaviorSystemModel()  # maybe should give path to DB connection file
    systemM.connect_to_DB()
    systemM._DB.create_tables()

    # create_session4(systemM)
    # systemM.start_Session()


   #temps = systemM.get_list_templates()
    #systemM.start_Session()
    # systemM.get_template_list_by_date_exp_sess_names()
    # systemM.get_template_list_by_subject()
    # #create_trial_types(systemM)
    # #systemM._DB.delete_all_rows()
    # create_session1(systemM)
    # #create_session2(systemM)
    # systemM.start_Session()
    # #blocks try later
    # # create_session2()
    # # systemM.start_Session()
    # # validate updating of last_used in session_subejct and in sessions accordingly
    # # create_session3(systemM) #TODO when blocks ok
    # # systemM.start_Session()
    # create_session4(systemM)
    # systemM.start_Session()
    # create_session5(systemM)
    # systemM.start_Session()
    #
    # i = 4
    # create main window and give it the necessary VM's
    # show the window to start app

import os
from pathlib import Path
from Models.DB_INIT import DB


def prepare_session_information(session_name, ports, dependencies, trial_name, index, trials_in_session, is_fixed_iti,
                                repeats, isRandomOrder,MaxTime,Percent):
    input_ports = []
    output_ports = []
    dependencies_arr = []
    for port, port_type, name in ports:
        if port_type == 'Input':
            input_ports.append(port)
        elif port_type == 'Output':
            output_ports.append(port)
    if dependencies:
        for pair in dependencies:
            separator = ","
            output_string = separator.join(pair)
            dependencies_arr.append(output_string)
    configs_path = str(Path(__file__).parent.parent / 'config_files' / 'session_config.txt')

    with open(configs_path, "a") as file:
        db = DB()
        # max_session_time = db.get_max_trial_time(session_name)
        # file.write(str(max_session_time[0]) + ",")
        iti_vals = db.get_iti_vals(session_name)
        if is_fixed_iti:
            file.write("(" + str(iti_vals[0]) + "),")
        else:
            file.write(str(iti_vals) + ",")
        file.write(str(isRandomOrder) + "\n")
        if(isRandomOrder):
            file.write("Trial_name:" + trial_name + "\n" + repeats[int(index / 2)] + "," + MaxTime[int(index / 2)]+ "," + Percent[int(index / 2)]+ "\n")
        else:
            file.write("Trial_name:" + trial_name + "\n" + repeats[int(index / 2)] + "," + MaxTime[int(index / 2)]+ "\n")
        file.write("$Input Ports\n")
        if len(input_ports) > 0:
            for port in input_ports:
                file.write(
                    port + "," + str(db.isEndConditionEvent(db.get_event_name_by_port(port)[0], trial_name)[0]) + "\n")
        else:
            file.write("None\n")
        file.write("$Output Ports\n")
        for dep in dependencies_arr:
            file.write(dep + "\n")
            parameters = trials_in_session[index + 1][db.get_event_name_by_port(dep.split(",")[0])[0]]
            file.write(','.join(parameters) + "\n")
        for port in [item for item in output_ports ]:
            isRandom = db.is_random_event_in_a_given_trial(trial_name,db.get_event_name_by_port(port)[0])[0]
            file.write(port + "\n")
            parameters = trials_in_session[index + 1][db.get_event_name_by_port(port)[0]]
            isReward = db.isReward(db.get_event_name_by_port(port)[0])
            if isReward[0]:
                file.write("1,")
            else:
                file.write("0,")
            if isRandom:
                file.write("1,")
            else:
                file.write("0,")
            file.write(','.join(parameters) + "\n")

        file.write("\n")

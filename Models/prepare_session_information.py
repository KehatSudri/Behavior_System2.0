from pathlib import Path
from Models.DB_INIT import DB
from Views.utils import get_base_path, get_file_path_from_configs


def prepare_session_information(ports, dependencies, trial_name, index, trials_in_session,
                                repeats, isRandomOrder, MaxTime, Percent):
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
    configs_path = get_file_path_from_configs('session_config.txt')

    with open(configs_path, "a") as file:
        db = DB()
        if isRandomOrder:
            file.write(
                "Trial name: " + trial_name + "\n" + repeats[int(index / 2)] + "," + MaxTime[int(index / 2)] + "," +
                Percent[int(index / 2)] + "\n")
        else:
            file.write(
                "Trial name: " + trial_name + "\n" + repeats[int(index / 2)] + "," + MaxTime[int(index / 2)] + "\n")
        file.write("$Input Ports\n")
        if len(input_ports) > 0:
            for port in input_ports:
                file.write(
                    port + "," + str(
                        db.isEndConditionEvent(db.get_event_name_by_port_and_trial(port, trial_name)[0], trial_name)[
                            0]) + "\n")
        else:
            file.write("None\n")
        file.write("$Output Ports\n")
        if len(output_ports) == 0:
            file.write("None\n")
        else:
            for port in [item for item in output_ports if item not in [tup[0] for tup in dependencies]]:
                isRandom = \
                    db.is_random_event_in_a_given_trial(trial_name,
                                                        db.get_event_name_by_port_and_trial(port, trial_name)[0])[0]
                if "Tone" in db.get_event_name_by_port_and_trial(port, trial_name)[0]:
                    file.write(db.get_event_name_by_port_and_trial(port, trial_name)[0] + "\n")
                else:
                    file.write(port + "\n")
                file.write(
                     str(
                        db.isEndConditionEvent(db.get_event_name_by_port_and_trial(port, trial_name)[0], trial_name)[
                            0]) + "\n")
                parameters = trials_in_session[index + 1][db.get_event_name_by_port_and_trial(port, trial_name)[0]]
                isReward = db.isReward(db.get_event_name_by_port_and_trial(port, trial_name)[0])
                if isReward[0]:
                    file.write("1,")
                else:
                    file.write("0,")
                if isRandom:
                    file.write("1,")
                else:
                    file.write("0,")

                file.write(','.join(parameters) + "\n")
        for dep in dependencies_arr:
            preCond = db.getPreCondition(db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0],trial_name)
            preCond=preCond[0][0]
            if "Tone" in db.get_event_name_by_port_and_trial(dep.split(",")[1],trial_name)[0]:
                dep = dep.split(",")[0]+",Tone"
            if not preCond:
                file.write(dep + ",None\n")
            else:
                if "Tone" in preCond:
                    file.write(dep + "," + preCond + "\n")
                else:
                    preCond_port = db.get_port_by_event_name_and_trial(preCond, trial_name)[0]
                    file.write(dep + ","+preCond_port+"\n")

            parameters = trials_in_session[index + 1][
                db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0]]
            isReward = db.isReward(db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0])
            isRandom = \
                db.is_random_event_in_a_given_trial(trial_name,
                                                    db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[
                                                        0])[0]
            file.write(
                str(
                    db.isEndConditionEvent(db.get_event_name_by_port_and_trial(port, trial_name)[0], trial_name)[
                        0]) + "\n")
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

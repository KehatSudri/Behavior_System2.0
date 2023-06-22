from pathlib import Path
from Models.DB_INIT import DB


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
    configs_path = str(Path(__file__).parent.parent / 'config_files' / 'session_config.txt')

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
        for dep in dependencies_arr:
            file.write(dep + "\n")
            parameters = trials_in_session[index + 1][
                db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0]]
            isReward = db.isReward(db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0])
            isRandom = \
                db.is_random_event_in_a_given_trial(trial_name,
                                                    db.get_event_name_by_port_and_trial(dep.split(",")[0], trial_name)[0])[0]
            if isReward[0]:
                file.write("1,")
            else:
                file.write("0,")
            if isRandom:
                file.write("1,")
            else:
                file.write("0,")
            file.write(','.join(parameters) + "\n")
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

        file.write("\n")

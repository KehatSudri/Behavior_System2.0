import os
from pathlib import Path
from Models.DB_INIT import DB


def prepare_session_information(ports, dependencies, trial_name, index, trials_in_session):
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
        file.write("Trial name : " + trial_name + "\n")
        file.write("$Input Ports\n")
        if len(input_ports) > 0:
            for port in input_ports:
                file.write(port + "\n")
        else:
            file.write("None\n")
        file.write("$Output Ports\n")
        for dep in dependencies_arr:
            file.write(dep + "\n")
            parameters = trials_in_session[index + 1][db.get_event_name_by_port(dep.split(",")[0])[0]]
            file.write(','.join(parameters) + "\n")
        for port in [item for item in output_ports if item not in [tup[0] for tup in dependencies]]:
            file.write(port + "\n")
            parameters = trials_in_session[index + 1][db.get_event_name_by_port(port)[0]]
            file.write(str(db.isEndConditionEvent(db.get_event_name_by_port(port)[0], trial_name)[0])+',')
            file.write(','.join(parameters) + "\n")
            # for port, port_type, name in ports:
            #     file.write(str(db.isEndConditionEvent(db.get_event_name_by_port(port)[0],trial_name)[0]))


        file.write("\n")

import os
from pathlib import Path


def prepare_session_information(ports, dependencies, trial_name, index, trials_in_session):
    input_ports = []
    output_ports = []
    dependencies_arr = []
    for port, type, name in ports:
        if type == 'Input':
            input_ports.append(port)
        elif type == 'Output':
            output_ports.append(port)
            parameters = trials_in_session[index + 1][name]
            parameters_string = str(parameters).replace(",", " ").replace("'", "")
            parameters_string = "[" + parameters_string[1:-1] + "]"
            output_ports.append(parameters_string)
    if dependencies:
        for pair in dependencies:
            separator = ","
            output_string = separator.join(pair)
            dependencies_arr.append(output_string)
    configs_path = str(Path(__file__).parent.parent / 'config_files' / 'session_config.txt')

    with open(configs_path, "a") as file:
        file.write("Trial name : " + trial_name + "\n")
        file.write("Dependencies\n")
        if len(dependencies_arr) > 0:
            for dep in dependencies_arr:
                file.write(dep + "\n")
        else:
            file.write("None\n")
        file.write("Input Ports\n")
        if len(input_ports) > 0:
            for input in input_ports:
                file.write(input + "\n")
        else:
            file.write("None\n")
        file.write("Output Ports\n")
        for output in output_ports:
            file.write(output + "\n")
        file.write("\n")

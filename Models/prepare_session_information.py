import os
def prepare_session_information(ports,dependencies,trials_in_session):
    print(trials_in_session)
    input_ports = []
    output_ports=[]
    dependencies_string="None"
    for port, type ,name in ports:
        if type == 'Input':
            input_ports.append(port)
        elif type == 'Output':
            output_ports.append(port)
    input_ports_string = ",".join(input_ports)
    output_ports_string = ",".join(output_ports)
    if dependencies != "":
        dependencies_string = ','.join(['('+','.join(pair)+')' for pair in dependencies])
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "session_info.txt"
    file_path = os.path.join(current_dir, filename)
    with open(file_path, "w") as file:
        file.write("Dependencies\n" + dependencies_string + "\n")
        file.write("Input Ports\n"+input_ports_string+"\n")
        file.write("Output Ports\n" + output_ports_string+"\n")



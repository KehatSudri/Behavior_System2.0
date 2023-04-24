import os
def prepare_session_information(ports,dependencies,trials_in_session):
    input_ports = []
    for port, type in ports:
        if type == 'Input':
            input_ports.append(port)
    input_ports_string = ",".join(input_ports)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "session_info.txt"
    file_path = os.path.join(current_dir, filename)
    with open(file_path, "w") as file:
        file.write("Input Ports\n"+input_ports_string+"Output Ports\n")

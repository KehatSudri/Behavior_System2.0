#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <string>

SessionConf::SessionConf(std::string path) : _confPath(path), _numOfTrials(0) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		std::string line;
		int category = 0;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				this->_numOfTrials++;
			}
			else {
				if (line[0] == '$')
					++category;
				switch (category) {
				case 1:
					this->_Dependencies.push_back(line);
				case 2:
					this->_AIPorts.push_back(line);
				case 3:
					this->_AOPorts.push_back(line);
				default:
					break;
				}
			}
		}
		inputFile.close();
	}
	else {
		std::cerr << "Failed to open file\n";
	}
}

std::vector<std::string> SessionConf::getPorts(int type) {
	switch (type) {
	case AI_PORTS:
		return std::vector<std::string>{"Dev1/ai11"};
		return this->_AIPorts;
	case DI_PORTS:
		return this->_DIPorts;
	case AO_PORTS:
		return std::vector<std::string>{"Dev1/ao1"};
		return this->_AOPorts;
	case DO_PORTS:
		return this->_DOPorts;
	default:
		return std::vector<std::string>();
	}
}

TaskHandle SessionConf::getInputTaskHandle() {
	TaskHandle task = NULL;
	DAQmxCreateTask("", &task);

	std::vector<std::string> ai_ports = getPorts(AI_PORTS);
	for (auto port : ai_ports) {
		const char* ai_port = port.c_str();
		DAQmxCreateAIVoltageChan(task, ai_port, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
	}
	return task;
}
std::vector<TaskHandle> SessionConf::getAnalogOutputTasks()
{
	std::vector<std::string> ao_ports = getPorts(AO_PORTS);
	std::vector<TaskHandle> tasks;
	for (auto port : ao_ports) {
		std::cout << port << std::endl;
		const char* ao_port = port.c_str();
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, ao_port, "", -5.0, 5.0, DAQmx_Val_Volts, "");
		tasks.push_back(AO_TaskHandle);
	}
	return tasks;
}
std::vector<Event> SessionConf::getInputEvents()
{
	std::vector<Event> events;
	std::vector<std::string> ai_ports = getPorts(AI_PORTS);
	for (auto port : ai_ports) {
		Event eve;
		events.push_back(eve);
	}
	return events;
}
/*#include "conf.h"
#include <fstream>
#include <iostream>
#include <string>


#define AI_PORTS 1
#define AO_PORTS 2
#define DI_PORTS 3
#define DO_PORTS 4

conf::conf(std::string path) : _confPath(path), _numOfTrials(0) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		std::string line;
		int category = 0;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				this->_numOfTrials++;
			}
			else {
				if (line[0] == '$')
					++category;		
				switch (category) {
				case 1:
					this->_Dependencies.push_back(line);
				case 2:
					this->_AIPorts.push_back(line);
				case 3:
					this->_AOPorts.push_back(line);
				default:
					break;
				}
				std::cout << line << '\n';
			}	
		}
		inputFile.close();
	}
	else {
		std::cerr << "Failed to open file\n";
	}
}

std::vector<std::string> conf::getPorts(int type) {
	switch (type) {
	case AI_PORTS:
		return std::vector<std::string>{"Dev1/ai11"};
		return this->_AIPorts;
	case AO_PORTS:
		return this->_AOPorts;
	case DO_PORTS:
		return this->_DOPorts;
	default:
		return std::vector<std::string>();
	}
}
*/
#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <string>

void SessionConf::initAnalogOutputTasks(){
	for (auto port : this->_AOPorts) {
		std::cout << port << std::endl;
		const char* ao_port = port.c_str();
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, ao_port, "", -5.0, 5.0, DAQmx_Val_Volts, "");
		this->_analogOutputTasks.push_back(AO_TaskHandle);
	}
}

void SessionConf::initInputTaskHandle(){
	DAQmxCreateTask("", &this->_inputEvents);
	for (auto port : this->_AIPorts) {
		const char* ai_port = port.c_str();
		DAQmxCreateAIVoltageChan(this->_inputEvents, ai_port, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
	}
}

void SessionConf::initInputEvents(){
	for (auto port : this->_AIPorts) {
		Event eve(port);
		this->_inputEvents.push_back(eve);
	}
}

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
					break;
				case 2:
					this->_AIPorts.push_back(line);
					break;
				case 3:
					this->_AOPorts.push_back(line);
					std::getline(inputFile, line);
					break;
				default:
					break;
				}
			}
		}
		inputFile.close();
		initInputEvents();
		initAnalogOutputTasks();
	}
	else {
		std::cerr << "Failed to open file\n";
	}
}

TaskHandle SessionConf::getInputTaskHandle() {
	return this->_inputEvents;
}

std::vector<TaskHandle> SessionConf::getAnalogOutputTasks(){
	return this->_analogOutputTasks;
}

std::vector<Event> SessionConf::getInputEvents(){
	return this->_inputEvents;
}

SessionConf::~SessionConf(){
	for(auto task: this->_analogOutputTasks)
		DAQmxClearTask(task);
	for (auto task : this->_digitalOutputTasks)
		DAQmxClearTask(task);
	DAQmxClearTask(this->_inputEvents);
}

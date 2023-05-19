#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

std::map<std::string, int>  getAttributes(std::string port, const std::vector<int>& params) {
	// TODO Switch case on port
	// TODO Check if only 'it' can be passed here
	std::map<std::string, int> attributes;
	auto it = params.begin();
	attributes[DELAY_PARAM] = *it;
	attributes[DURATION_PARAM] = *(it+1);
	attributes[FREQUENCY_PARAM] = *(it+2);
	return attributes;
}

void SessionConf::initAnalogOutputTasks() {
	for (const auto& pair : this->_AOPorts) {
		const std::string& portName = pair.first;
		const std::vector<int>& params = pair.second;

		std::string delimiter = ",";
		std::string token1 = portName, token2;
		size_t pos = portName.find(delimiter);
		if (pos != std::string::npos) {
			token1 = portName.substr(0, pos);
			token2 = portName.substr(pos + delimiter.length());
		}
		const char* ao_port = token1.c_str();
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, ao_port, "", -5.0, 5.0, DAQmx_Val_Volts, "");
		this->_analogOutputTasks.push_back(AO_TaskHandle);
		SimpleOutputer* sm = new SimpleOutputer(AO_TaskHandle, getAttributes(portName, params));
		// TODO Check if this can be in line constructed
		this->_simpleOutputers.push_back(sm);
		if (!token2.empty()) {
			for (auto& eve : this->getInputEvents()) {
				if (eve->getPort() == token2) {
					eve->attachListener(new ContingentOutputer(sm));
					break;
				}
			}
		}
	}
}

void SessionConf::initInputTaskHandle(){
	DAQmxCreateTask("", &this->_inputTaskHandle);
	for (auto port : this->_AIPorts) {
		const char* ai_port = port.c_str();
		DAQmxCreateAIVoltageChan(this->_inputTaskHandle, ai_port, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
	}
}

std::vector<int> getParams(std::string line){
	line = line.substr(1, line.size() - 2);
	std::stringstream ss(line);
	std::vector<int> params;
	int num;
	while (ss >> num) {
		params.push_back(num);
		if (ss.peek() == ',')
			ss.ignore();
	}
	return params;
}

void SessionConf::initInputEvents() {
	for (auto port : this->_AIPorts) {
		this->_inputEvents.push_back(new Event(port));
	}
}

SessionConf::SessionConf(std::string path) : _numOfTrials(0), _validFlag(true) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		int category = 0;
		std::string line;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				++this->_numOfTrials;
			}
			else {
				if (line[0] == '$') {
					++category;
					continue;
				}
				std::string portName = line;
				switch (category) {
				case 1:
					this->_AIPorts.push_back(portName);
					break;
				case 2:
					std::getline(inputFile, line);
					this->_AOPorts[portName] = getParams(line);
					break;
				default:
					break;
				}
			}
		}
		inputFile.close();
		initInputTaskHandle();
		initInputEvents();
		initAnalogOutputTasks();
		if (this->_AIPorts.empty()) {
			this->_validFlag = false;
		}
	}
	else {
		this->_validFlag = false;
	}
}

TaskHandle SessionConf::getInputTaskHandle() {
	return this->_inputTaskHandle;
}

std::vector<TaskHandle> SessionConf::getAnalogOutputTasks(){
	return this->_analogOutputTasks;
}

std::vector<Event*> SessionConf::getInputEvents(){
	return this->_inputEvents;
}

SessionConf::~SessionConf() {
	for (auto task : this->_analogOutputTasks) {
		DAQmxClearTask(task);
	}
	for (auto task : this->_digitalOutputTasks) {
		DAQmxClearTask(task);
	}
	DAQmxClearTask(this->_inputTaskHandle);
}

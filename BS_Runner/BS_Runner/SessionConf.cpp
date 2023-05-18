#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <string>

void SessionConf::initAnalogOutputTasks(){
	for (auto port : this->_AOPorts) {
		std::string delimiter = ",";
		std::string token1 = port, token2;
		size_t pos = port.find(delimiter);
		if (pos != std::string::npos) {
			token1 = port.substr(0, pos);
			token2 = port.substr(pos + delimiter.length());
		}
		const char* ao_port = token1.c_str();
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, ao_port, "", -5.0, 5.0, DAQmx_Val_Volts, "");
		this->_analogOutputTasks.push_back(AO_TaskHandle);
		SimpleOutputer* sm = new SimpleOutputer(AO_TaskHandle, 30, 10);
		this->_simpleOutputers.push_back(sm);
		if (!token2.empty())
			for (auto& eve : this->getInputEvents()) {
				if (eve->getPort() == token2) {
					eve->attachListener(new ContingentOutputer(sm));
					break;
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

void SessionConf::initInputEvents() {
	for (auto port : this->_AIPorts) {
		this->_inputEvents.push_back(new Event(port));
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
				if (line[0] == '$') {
					++category;
					continue;
				}
				switch (category) {
				case 1:
					this->_AIPorts.push_back(line);
					break;
				case 2:
					this->_AOPorts.push_back(line);
					std::getline(inputFile, line);
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
	}
	else {
		std::cerr << "Failed to open file\n";
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

SessionConf::~SessionConf(){
	for(auto task: this->_analogOutputTasks)
		DAQmxClearTask(task);
	for (auto task : this->_digitalOutputTasks)
		DAQmxClearTask(task);
	DAQmxClearTask(this->_inputTaskHandle);
}

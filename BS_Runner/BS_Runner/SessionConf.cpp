#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

std::map<std::string, int>  getAttributes(std::string port, const std::vector<int>& params) {
	// TODO Switch case on port
	std::map<std::string, int> attributes;
	auto it = params.begin();
	attributes[DELAY_PARAM] = *it;
	attributes[DURATION_PARAM] = *(it+1);
	attributes[FREQUENCY_PARAM] = *(it+2);
	return attributes;
}

std::vector<int> getParams(std::string line) {
	std::stringstream ss(line);
	std::string token;
	std::vector<int> params;
	while (std::getline(ss, token, ',')) {
		params.push_back(std::stoi(token));
    }
	return params;
}

SessionConf::SessionConf(std::string path) : _numOfTrials(0), _validFlag(true) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		int category = 0;
		std::string line;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				this->_trials[this->_numOfTrials].initInputTaskHandle();
				this->_trials[this->_numOfTrials].initInputEvents();
				this->_trials[this->_numOfTrials].initAnalogOutputTasks();
				if (this->_trials[this->_numOfTrials]._AIPorts.empty()) {
					this->_validFlag = false;
					break;
				}
				++this->_numOfTrials;
			}
			else {
				if (line[0] == '$') {
					++category;
					continue;
				}
				std::string name = line;
				switch (category) {
				case 0:
					this->_trials.push_back({ name });
					break;
				case 1:
					this->_trials[this->_numOfTrials]._AIPorts.push_back(name);
					break;
				case 2:
					std::getline(inputFile, line);
					this->_trials[this->_numOfTrials]._AOPorts[name] = getParams(line);
					break;
				default:
					break;
				}
			}
		}
		inputFile.close();
	}
	else {
		this->_validFlag = false;
	}
}

void SessionConf::changeCurrentTrial(){
	// TODO Implement logic on next trial
	return;
}

void SessionConf::finishSession() {
	this->_sessionComplete = true;
}

TaskHandle SessionConf::getInputTaskHandle() {
	return this->_trials[this->_currentTrial].getInputTaskHandle();
}

std::vector<TaskHandle> SessionConf::getAnalogOutputTasks() {
	return this->_trials[this->_currentTrial].getAnalogOutputTasks();
}

std::vector<EnvironmentOutputer*> SessionConf::getEnvironmentOutputer() {
	return this->_trials[this->_currentTrial].getEnvironmentOutputer();
}

std::vector<Event*> SessionConf::getInputEvents() {
	return this->_trials[this->_currentTrial].getInputEvents();
}

void Trial::initInputEvents() {
	for (auto port : this->_AIPorts) {
		this->_inputEvents.push_back(new Event(port));
	}
}

void Trial::initAnalogOutputTasks() {
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
		this->_simpleOutputers.push_back(sm);
		if (!token2.empty()) {
			for (auto& eve : this->getInputEvents()) {
				if (eve->getPort() == token2) {
					std::cout << "contigiantt ";
					eve->attachListener(new ContingentOutputer(sm));
					break;
				}
			}
		}
		else {
			this->_environmentOutputer.push_back(new EnvironmentOutputer(sm));
		}
	}
}

void Trial::initInputTaskHandle() {
	DAQmxCreateTask("", &this->_inputTaskHandle);
	for (auto port : this->_AIPorts) {
		const char* ai_port = port.c_str();
		DAQmxCreateAIVoltageChan(this->_inputTaskHandle, ai_port, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
	}
}

TaskHandle Trial::getInputTaskHandle() {
	return this->_inputTaskHandle;
}

std::vector<TaskHandle> Trial::getAnalogOutputTasks() {
	return this->_analogOutputTasks;
}

std::vector<Event*> Trial::getInputEvents() {
	return this->_inputEvents;
}

Trial::~Trial() {
	for (auto task : this->_analogOutputTasks) {
		DAQmxClearTask(task);
	}
	for (auto task : this->_digitalOutputTasks) {
		DAQmxClearTask(task);
	}
	DAQmxClearTask(this->_inputTaskHandle);
}

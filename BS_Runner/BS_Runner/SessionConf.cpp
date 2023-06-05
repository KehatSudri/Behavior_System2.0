#include "SessionConf.h"
#include "Consts.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <random>


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

void SessionConf::performITIWait() {
	auto start_time = std::chrono::high_resolution_clock::now();
	if (_maxITI) {
		std::random_device rd;
		std::mt19937 gen(rd());
		std::uniform_real_distribution<double> dis(_minITI, _maxITI);
		while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < dis(gen)) {
			continue;
		}
	}
	else {
		while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _minITI) {
			continue;
		}
	}
}

SessionConf::SessionConf(std::string path) : _numOfTrials(0), _validFlag(true) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		int category = 0;
		std::string line, delimiter = ",";
		std::getline(inputFile, line);
		std::string iti = line.substr(1, line.length() - 2);
		size_t pos = iti.find(delimiter);
		if (pos != std::string::npos) {
			setMinITI(std::stod(iti.substr(0, pos)));
			setMaxITI(std::stod(iti.substr(pos + delimiter.length())));
		}
		else {
			setMinITI(std::stod(iti));
		}
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				_trials[_numOfTrials].initInputTaskHandle();
				_trials[_numOfTrials].initInputEvents();
				_trials[_numOfTrials].initAnalogOutputTasks();
				_trials[_numOfTrials].initTrialKillers();
				if (_trials[_numOfTrials]._AIPorts.empty()) {
					_validFlag = false;
					break;
				}
				++_numOfTrials;
			}
			else {
				if (line[0] == '$') {
					++category;
					continue;
				}
				std::string name = line, token2;
				switch (category % 3) {
				case 0:
					_trials.push_back({ name });
					break;
				case 1:
					pos = line.find(delimiter);
					name = line.substr(0, pos);
					token2 = line.substr(pos + delimiter.length());
					_trials[_numOfTrials]._AIPorts.push_back(name);
					// TODO Implement support for end condition
					if (token2 == "True") {
						_trials[_numOfTrials]._trialKillers.push_back(name);
					}
					break;
				case 2:
					std::getline(inputFile, line);
					_trials[_numOfTrials]._AOPorts.push_back({ name ,getParams(line) });
					break;
				default:
					break;
				}
			}
		}
		inputFile.close();
	}
	else {
		_validFlag = false;
	}
}

int SessionConf::changeCurrentTrial() {
	performITIWait();
	return END_OF_SESSION;
}

void SessionConf::finishSession() {
	this->_sessionComplete = true;
}

TaskHandle SessionConf::getInputTaskHandle() {
	return _trials[_currentTrial].getInputTaskHandle();
}

std::vector<EnvironmentOutputer*> SessionConf::getEnvironmentOutputer() {
	return _trials[_currentTrial].getEnvironmentOutputer();
}

std::vector<Event*> SessionConf::getInputEvents() {
	return _trials[_currentTrial].getInputEvents();
}

void Trial::initInputEvents() {
	for (auto& port : _AIPorts) {
		_events.push_back(new Event(port));
	}
}

Outputer* getOutputer(TaskHandle taskHandle, std::string port, std::map<std::string, int> attr) {
	// TODO Implement logic
	return new SimpleOutputer(taskHandle, port, attr);
}

void Trial::initAnalogOutputTasks() {
	for (auto& it : _AOPorts) {
		const std::string& portName = std::get<0>(it);
		const std::vector<int>& params = std::get<1>(it);
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
		Outputer* sm = getOutputer(AO_TaskHandle, token1, getAttributes(portName, params));
		_events.push_back(sm);
		if (!token2.empty()) {
			for (auto& eve : _events) {
				if (eve->getPort() == token2) {
					eve->attachListener(new ContingentOutputer(sm));
					break;
				}
			}
		}
		else {
			_environmentOutputer.push_back(new EnvironmentOutputer(sm));
		}
	}
}

void Trial::initInputTaskHandle() {
	DAQmxCreateTask("", &_inputTaskHandle);
	for (auto& port : _AIPorts) {
		const char* ai_port = port.c_str();
		DAQmxCreateAIVoltageChan(_inputTaskHandle, ai_port, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
	}
}

void Trial::initTrialKillers() {
	TrialKiller* killer = new TrialKiller();
	for (auto& it : _trialKillers) {
		for (auto& eve : getInputEvents()) {
			if (eve->getPort() == it) {
				eve->attachListener(killer);
				break;
			}
		}
	}
}

TaskHandle Trial::getInputTaskHandle() {
	return _inputTaskHandle;
}

std::vector<Event*> Trial::getInputEvents() const {
	std::vector<Event*> inputEvents;
	for (auto it : _events) {
		if (it->getPort().find("ai") != std::string::npos) {
			inputEvents.push_back(it);
		}
	}
	return inputEvents;
}

Trial::~Trial() {
	for (auto& task : _digitalOutputTasks) {
		DAQmxClearTask(task);
	}
	DAQmxClearTask(_inputTaskHandle);
}

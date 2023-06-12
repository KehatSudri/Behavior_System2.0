#include "SessionConf.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <random>


std::map<std::string, int>  getAttributes(std::string port, const std::vector<int>& params) {
	std::map<std::string, int> attributes;
	auto it = params.begin();
	attributes[DELAY_PARAM] = *it;
	attributes[DURATION_PARAM] = *(it + 1);
	attributes[FREQUENCY_PARAM] = *(it + 2);
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
		std::string line, delimiter = ",";
		std::getline(inputFile, line);
		std::stringstream ss(line);
		std::string element;
		size_t pos;
		int type = 0;
		while (std::getline(ss, element, ',')) {
			std::string iti = line.substr(1, line.length() - 2);
			pos = iti.find(delimiter);
			if (type == 1) {
				iti = element.substr(1, element.length() - 2);
				pos = iti.find(delimiter);
			}
			switch (type) {
			case 0:
				setMaxTrialWaitTime(std::stoi(element));
				break;
			case 1:
				if (pos != std::string::npos) {
					setMinITI(std::stod(iti.substr(0, pos)));
					setMaxITI(std::stod(iti.substr(pos + delimiter.length())));
				}
				else {
					setMinITI(std::stod(iti));
				}
				break;
			case 2:
				if (element == "True") {
					setisSessionRandom(true);
				}
				break;
			default:
				break;
			}
			++type;
		}
		while (std::getline(inputFile, line)) {
			if (line[0] == '$' || line.empty()) {
				++category;
				if (line[0] == '$') {
					continue;
				}
			}
			std::string name = line, token2;
			switch (category) {
			case 0:
				_trials.push_back({ name });
				std::getline(inputFile, line);
				_trials[_numOfTrials]._numOfRuns = std::stoi(line);
				break;
			case 1:
				pos = line.find(delimiter);
				name = line.substr(0, pos);
				token2 = line.substr(pos + delimiter.length());
				_trials[_numOfTrials]._AIPorts.push_back(name);
				if (token2 == "True") {
					_trials[_numOfTrials]._trialKillers.push_back(name);
				}
				break;
			case 2:
				std::getline(inputFile, line);
				_trials[_numOfTrials]._AOPorts.push_back({ name ,getParams(line) });
				break;
			default:
				_trials[_numOfTrials].initInputTaskHandle();
				_trials[_numOfTrials].initInputEvents();
				int error = _trials[_numOfTrials].initAnalogOutputTasks();
				if (error < 0) {
					_validFlag = false;
					break;
				}
				_trials[_numOfTrials].initTrialKillers();
				if (_trials[_numOfTrials]._AIPorts.empty()) {
					_validFlag = false;
					break;
				}
				++_numOfTrials;
				category = 0;
			}
		}
		inputFile.close();
	}
	else {
		_validFlag = false;
	}
}

int SessionConf::changeCurrentTrial() {
	auto start_time = std::chrono::high_resolution_clock::now();
	int code = CONTINUE_SESSION;
	if (!_isSessionRandom) {
		if (--_trials[_numOfTrials]._numOfRuns == 0) {
			if (++_currentTrial == _numOfTrials) {
				code = END_OF_SESSION;
			}
		}
	}
	else {
		// TODO implement random trial change
	}
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
	return code;
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

void SessionConf::giveReward() {
	_trials[_currentTrial].giveReward();
}

void Trial::initInputEvents() {
	for (auto& port : _AIPorts) {
		_events.push_back(new Event(port));
	}
}

Outputer* getOutputer(std::string port, std::map<std::string, int> attr) {
	size_t isAnalog = port.find("ao");
	size_t isDigital = port.find("port0");
	if (isAnalog != std::string::npos) {
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, port.c_str(), "", -5.0, 5.0, DAQmx_Val_Volts, "");
		return new SimpleAnalogOutputer(AO_TaskHandle, port, attr);
	}
	else if (isDigital != std::string::npos) {
		TaskHandle DO_TaskHandle = NULL;
		DAQmxCreateTask("", &DO_TaskHandle);
		DAQmxCreateDOChan(DO_TaskHandle, port.c_str(), "", DAQmx_Val_ChanPerLine);
		return new SimpleDigitalOutputer(DO_TaskHandle, port, attr);
	}
	else {
		return NULL;
	}
}

int Trial::initAnalogOutputTasks() {
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
		Outputer* sm = getOutputer(token1, getAttributes(portName, params));
		if (sm == NULL) {
			return -1;
		}
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
	return 1;
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
		for (auto& eve : _events) {
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

void Trial::giveReward() {
	// TODO implement "give reward"
	return;
}

Trial::~Trial() {
	for (auto& task : _digitalOutputTasks) {
		DAQmxClearTask(task);
	}
	DAQmxClearTask(_inputTaskHandle);
}

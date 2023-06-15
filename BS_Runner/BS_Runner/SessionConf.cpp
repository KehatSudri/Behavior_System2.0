#include "SessionConf.h"
#include "Consts.h"
#include <random>
#include <numeric>

std::map<std::string, int>  getAttributes(std::string port, const std::vector<int>& params) {
	std::map<std::string, int> attributes;
	auto it = params.begin();
	attributes[DELAY_PARAM] = *it;
	attributes[DURATION_PARAM] = *(it + 1);
	attributes[FREQUENCY_PARAM] = *(it + 2);
	attributes[AMPLITUDE_PARAM] = *(it + 3);
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

int pickRandomTrial(const std::vector<int>& probabilities) {
	int sum = std::accumulate(probabilities.begin(), probabilities.end(), 0);
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distr(1, sum);
	int random_number = distr(gen);
	int current_sum = 0;
	for (size_t i = 0; i < probabilities.size(); ++i) {
		current_sum += probabilities[i];
		if (random_number <= current_sum) {
			return i;
		}
	}
	// Just a fallback, in case something goes wrong.
	return -1;
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
				if (element == TRUE) {
					setisSessionRandom(true);
				}
				break;
			default:
				break;
			}
			++type;
		}
		while (std::getline(inputFile, line)) {
			if (line[0] == NEW_LINE_CATEGORY || line.empty()) {
				++category;
				if (line[0] == NEW_LINE_CATEGORY) {
					continue;
				}
			}
			std::string name = line, token2;
			switch (category) {
			case 0:
				_trials.push_back({ name });
				std::getline(inputFile, line);
				_trials[_numOfTrials]._remainingRuns = std::stoi(line);
				break;
			case 1:
				pos = line.find(delimiter);
				name = line.substr(0, pos);
				token2 = line.substr(pos + delimiter.length());
				_trials[_numOfTrials]._AIPorts.push_back(name);
				if (token2 == TRUE) {
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
				if (_trials[_numOfTrials].initAnalogOutputTasks() == ERROR) {
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

std::string SessionConf::getCurrentRunningTrial(){
	if (_numOfTrials) {
		return _trials[_currentTrial]._trialName;
	}
	return std::string();
}

bool allZeros(const std::vector<int>& vec) {
	for (int value : vec) {
		if (value != 0) {
			return false;
		}
	}
	return true;
}

int SessionConf::changeCurrentTrial() {
	auto start_time = std::chrono::high_resolution_clock::now();
	int code = CONTINUE_SESSION;
	--_trials[_currentTrial]._remainingRuns;
	if (!_isSessionRandom) {
		if (_trials[_currentTrial]._remainingRuns == 0) {
			if (++_currentTrial == _numOfTrials) {
				code = END_OF_SESSION;
			}
		}
	}
	else {
		if (_trials[_currentTrial]._remainingRuns == 0) {
			_trialProbabilities[_currentTrial] = 0;
		}
		if (allZeros(_trialProbabilities)) {
			code = END_OF_SESSION;
		}
		else {
			int getNextTrial = pickRandomTrial(_trialProbabilities);
			while (getNextTrial < 0) {
				getNextTrial = pickRandomTrial(_trialProbabilities);
			}
			_currentTrial = getNextTrial;
		}
	}
	if (code == END_OF_SESSION) {
		return code;
	}
	if (_maxITI) {
		std::random_device rd;
		std::mt19937 gen(rd());
		std::uniform_real_distribution<double> dis(_minITI, _maxITI);
		int random_iti = dis(gen);
		while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < random_iti) {
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
	size_t isAnalog = port.find(ANALOG_OUTPUT);
	size_t isDigital = port.find(DIGITAL_OUTPUT);
	if (isAnalog != std::string::npos) {
		TaskHandle AO_TaskHandle = NULL;
		DAQmxCreateTask("", &AO_TaskHandle);
		DAQmxCreateAOVoltageChan(AO_TaskHandle, port.c_str(), "", MIN_WATTAGE, MAX_WATTAGE, DAQmx_Val_Volts, "");
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

		Outputer* sm = getOutputer(token1, getAttributes(portName, params));
		if (sm == NULL) {
			return ERROR;
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
	std::string combine_ports = "";
	for (auto& port : _AIPorts) {
		combine_ports = combine_ports + ", " + port;
	}
	DAQmxCreateAIVoltageChan(_inputTaskHandle, combine_ports.c_str(), "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
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
		if (it->getPort().find(ANALOG_INPUT) != std::string::npos) {
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
	DAQmxClearTask(_inputTaskHandle);
}

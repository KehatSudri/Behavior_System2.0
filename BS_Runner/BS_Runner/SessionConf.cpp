#include "SessionConf.h"
#include "Consts.h"

std::map<std::string, int>  getAttributes(const std::vector<int>& params) {
	std::map<std::string, int> attributes;
	auto it = params.begin();
	attributes[IS_REWARD_PARAM] = *(it++);
	attributes[IS_RANDOM_PARAM] = *(it++);
	if (attributes[IS_RANDOM_PARAM] == 1) {
		attributes[MIN_DELAY_PARAM] = *(it++);
		attributes[MAX_DELAY_PARAM] = *(it++);
		attributes[DURATION_PARAM] = *(it++);
	}
	else {
		attributes[DELAY_PARAM] = *(it++);
		attributes[DURATION_PARAM] = *(it++);
	}
	if (it != params.end()) {
		attributes[FREQUENCY_PARAM] = *(it++);
		attributes[AMPLITUDE_PARAM] = *(it++);
	}
	return attributes;
}

std::vector<int> getParams(std::string line) {
	std::stringstream ss(line);
	std::string token;
	std::vector<int> params;
	while (std::getline(ss, token, ',')) { params.push_back(std::stoi(token)); }
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
		if (random_number <= current_sum) { return i; }
	}
	// Just a fallback, in case something goes wrong.
	return -1;
}

SessionConf::SessionConf(std::string path) : _numOfTrials(0), _validFlag(true) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		std::string line, delimiter = ",";
		std::getline(inputFile, line);
		setMaxSessionWaitTime(std::stod(line));
		std::getline(inputFile, line);
		std::stringstream ss(line);
		std::string element;
		size_t pos;
		std::getline(ss, element, ',');
		pos = element.find(";");
		if (pos != std::string::npos) {
			setMinITI(std::stoi(element.substr(0, pos)));
			setMaxITI(std::stoi(element.substr(pos + delimiter.length())));
		}
		else {
			setMinITI(std::stoi(element));
		}
		std::getline(ss, element, ',');
		if (element == "True") { setisSessionRandom(true); }
		int category = 0;
		int flag = 2;
		while (flag) {
			std::getline(inputFile, line);
			if (line.empty()) {
				if (flag == 2) {
					_trials[_numOfTrials].initInputTaskHandle();
					_trials[_numOfTrials].initInputEvents();
					if (_trials[_numOfTrials].initAnalogOutputTasks() == INIT_ERROR) {
						_validFlag = false;
						break;
					}
					_trials[_numOfTrials].initTrialKillers();
					++_numOfTrials;
					category = 0;
				}
				--flag;
				continue;
			}
			if (line[0] == NEW_LINE_CATEGORY) {
				++category;
				continue;
			}
			std::string name = line, token2;
			if (category == 0) {
				std::getline(inputFile, line);
			}
			if (line == NONE) {
				continue;
			}
			std::stringstream ss(line);
			switch (category) {
			case NEW_TRIAL_CASE:
				flag = 2;
				_trials.push_back({ name });
				std::getline(ss, element, ',');
				_trials[_numOfTrials]._remainingRuns = std::stoi(element);
				std::getline(ss, element, ',');
				_trials[_numOfTrials].setMaxTrialWaitTime(std::stod(element));
				if (_isSessionRandom) {
					std::getline(ss, element, ',');
					_trialProbabilities.push_back(stoi(element));
				}
				break;
			case NEW_INPUT_CASE:
				pos = line.find(delimiter);
				name = line.substr(0, pos);
				token2 = line.substr(pos + delimiter.length());
				_trials[_numOfTrials]._inputPorts.push_back(name);
				if (token2 == "True") { _trials[_numOfTrials]._trialKillers.push_back(name); }
				break;
			case NEW_OUTPUT_CASE:
				// TODO test new logic
				std::getline(inputFile, line);
				token2 = line;
				if (token2 == "True") {
					std::stringstream ss(name);
					std::getline(ss, element, ',');
					_trials[_numOfTrials]._trialKillers.push_back(element);
				}
				std::getline(inputFile, line);
				_trials[_numOfTrials]._outputPorts.push_back({ name ,getParams(line) });
				break;
			default:
				break;
			}
		}
		inputFile.close();
	}
	else {
		_validFlag = false;
	}
}

std::string SessionConf::getCurrentRunningTrial() {
	if (_numOfTrials) { return _trials[_currentTrial]._trialName; }
	return std::string();
}

bool allZeros(const std::vector<int>& vec) {
	for (int value : vec) { if (value != 0) { return false; } }
	return true;
}

int SessionConf::changeCurrentTrial() {
	if (_sessionComplete) { return END_OF_SESSION; }
	LogFileWriter::getInstance().write(TRIAL_END_INDICATOR, getCurrentRunningTrial());
	auto start_time = std::chrono::high_resolution_clock::now();
	int code = CONTINUE_SESSION;
	--_trials[_currentTrial]._remainingRuns;
	_trials[_currentTrial].setDefaultState();
	if (!_isSessionRandom) {
		if (_trials[_currentTrial]._remainingRuns == 0) {
			if (++_currentTrial == _numOfTrials) {
				code = END_OF_SESSION;
			}
		}
	}
	else {
		if (_trials[_currentTrial]._remainingRuns == 0) { _trialProbabilities[_currentTrial] = 0; }
		if (allZeros(_trialProbabilities)) { code = END_OF_SESSION; }
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
		double random_iti = dis(gen);
		while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start_time).count() < random_iti) { continue; }
	}
	else {
		while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _minITI) { continue; }
	}
	return code;
}

TaskHandle SessionConf::getInputTaskHandle() {
	return _trials[_currentTrial].getInputTaskHandle();
}

double SessionConf::getMaxTrialWaitTime() {
	return _trials[_currentTrial].getMaxTrialWaitTime();
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
	for (auto& port : _inputPorts) { _events.push_back(new Event(port)); }
}

Outputer* getOutputer(std::string port, std::map<std::string, int> attr) {
	size_t isTone = port.find(TONE);
	if (isTone != std::string::npos) {
		return new SimpleToneOutputer(port, attr);
	}
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
	else { return NULL; }
}

int Trial::initAnalogOutputTasks() {
	for (auto& it : _outputPorts) {
		const std::string& portName = std::get<0>(it);
		const std::vector<int>& params = std::get<1>(it);
		std::string delimiter = ",";
		std::string token1 = portName, token2, contingentOn, preCondition;
		size_t pos = portName.find(delimiter);
		if (pos != std::string::npos) {
			token1 = portName.substr(0, pos);
			token2 = portName.substr(pos + delimiter.length());
		}

		Outputer* sm = getOutputer(token1, getAttributes(params));
		if (sm == NULL) {
			return INIT_ERROR;
		}
		if (params[0]) {
			_rewardOutputers.push_back(sm);
		}
		_events.push_back(sm);
		if (!token2.empty()) {
			pos = token2.find(delimiter);
			contingentOn = token2.substr(0, pos);
			preCondition = token2.substr(pos + delimiter.length());
			ContingentOutputer* con = new ContingentOutputer(sm, preCondition);
			_contingentOutputer.push_back(con);
			bool foundContingentOn = false;
			bool foundPreCondition = false;
			for (auto& eve : _events) {
				if (eve->getPort() == contingentOn) {
					eve->attachListener(con);
					foundContingentOn = true;
				}
				else if (eve->getPort() == preCondition) {
					eve->attachListener(con);
					foundPreCondition = true;
				}
				if (foundContingentOn && foundPreCondition) { break; }
			}
		}
		else { _environmentOutputer.push_back(new EnvironmentOutputer(sm)); }
	}
	return 1;
}

void Trial::initInputTaskHandle() {
	DAQmxCreateTask("", &_inputTaskHandle);
	std::string combine_ports = "";
	for (auto& port : _inputPorts) {
		DAQmxCreateAIVoltageChan(_inputTaskHandle, port.c_str(), "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
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
	// TODO add pick option for specific reward
	Outputer* chosenRewardOutput = _rewardOutputers[0];
	if (_rewardOutputers.size()) {
		LogFileWriter::getInstance().write(REWARD_INDICATOR, chosenRewardOutput->getPort());
		chosenRewardOutput->output();
	}
}

void Trial::setDefaultState() {
	for (auto outputer : _contingentOutputer) {
		outputer->setDefaultState();
	}
	for (auto eve : _events) {
		eve->setDefaultState();
	}
}

Trial::~Trial() {
	DAQmxClearTask(_inputTaskHandle);
}

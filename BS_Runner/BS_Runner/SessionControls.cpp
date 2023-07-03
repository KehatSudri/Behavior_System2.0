#include "SessionControls.h"
#include "Consts.h"

using namespace System;
using namespace System::Windows::Forms;

void SessionControls::run(char* configFilePath) {
	SessionConf conf(configFilePath);
	if (!conf.isValid()) {
		MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
		this->finishSession();
		return;
	}

	_conf = &conf;
	_sessionTimeoutIndicator = _conf->getMaxSessionWaitTime();
	_sessionStartTime = std::chrono::high_resolution_clock::now();
	do {
		TaskHandle inputTaskHandle = conf.getInputTaskHandle();
		std::vector<Event*> inputEvents = conf.getInputEvents();
		int inputPortsSize = conf.getInputEvents().size();
		std::vector<float64> data(inputPortsSize);
		int32 read;
		setIsTrialRuning(true);
		setIsPaused(false);
		_trialTimeoutIndicator = _conf->getMaxTrialWaitTime();
		LogFileWriter::getInstance().write(TRIAL_START_INDICATOR, getCurrentRunningTrial());
		_trialStartTime = std::chrono::high_resolution_clock::now();
		for (auto envOutputer : conf.getEnvironmentOutputer()) {
			envOutputer->output();
		}
		if (inputPortsSize) {
			do {
				if (!this->_isPaused) {
					DAQmxReadAnalogF64(inputTaskHandle, 1, 10.0, DAQmx_Val_GroupByChannel, data.data(), sizeof(data), &read, nullptr);
					for (int i = 0; i < read * inputPortsSize; ++i) {
						std::thread t(&Event::set, inputEvents[i], data[i]);
						t.detach();
					}
				}
				else { std::this_thread::sleep_for(std::chrono::milliseconds(300)); }
			} while (isTrialRunning());
		}
		while (_Outputing) { continue; }
		if (conf.changeCurrentTrial() == END_OF_SESSION) { conf.setSessionComplete(true); }
	} while (isSessionRunning());
	finishSession();
}

bool SessionControls::isTrialRunning() {
	if (_isTrialRunning && std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - _trialStartTime).count() >= _trialTimeoutIndicator) {
		setIsTrialRuning(false);
		LogFileWriter::getInstance().write(TRIAL_TIMEOUT_INDICATOR, "");
	}
	return _isTrialRunning;
}

bool SessionControls::isSessionRunning() {
	bool isSessionTimeout = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - _sessionStartTime).count() >= _sessionTimeoutIndicator;
	if (isSessionTimeout){
		LogFileWriter::getInstance().write(SESSION_TIMEOUT_INDICATOR, "");
		return false;
	}
	if (_conf->isSessionComplete()) {
		LogFileWriter::getInstance().write(SESSION_END_INDICATOR, "");
		return false;
	}
	return true;
}

void SessionControls::startSession(char* configFilePath) {
	if (_isSessionRunning) return;
	if (!configFilePath) {
		MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
		return;
	}
	if (_runThread.joinable()) { _runThread.join(); }
	LogFileWriter::getInstance().createLogFile();
	setIsSessionRunning(true);
	this->_runThread = std::thread(&SessionControls::run, this, configFilePath);
}

void SessionControls::pauseSession() {
	if (this->_isPaused) { return; }
	setIsPaused(true);
}

void SessionControls::resumeSession() {
	if (!this->_isPaused) { return; }
	setIsPaused(false);
}

void SessionControls::giveReward() {
	if (this->_isPaused) { return; }
	_conf->giveReward();
}

void SessionControls::finishSession() {
	if (!_isSessionRunning) return;
	if (_conf) { _conf->finishSession(); }
	setIsPaused(true);
	setIsSessionRunning(false);
	setIsTrialRuning(false);
	if (std::this_thread::get_id() != _runThread.get_id()) {
		_runThread.join();
	}
	MessageBox::Show("Session was finished");
}

std::string SessionControls::getCurrentRunningTrial() {
	if (_conf) { return _conf->getCurrentRunningTrial(); }
	return std::string();
}

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
	do {
		TaskHandle inputTaskHandle = conf.getInputTaskHandle();
		std::vector<Event*> inputEvents = conf.getInputEvents();
		int inputPortsSize = conf.getInputEvents().size();
		std::vector<float64> data(inputPortsSize * SAMPLE_PER_PORT);
		int32 read;
		setIsTrialRuning(true);
		setIsPaused(false);

		_trialTimeoutIndicator = _conf->getMaxTrialWaitTime();
		LogFileWriter::getInstance().write(TRIAL_START, getCurrentRunningTrial());
		_trialStartTime = std::chrono::high_resolution_clock::now();
		for (auto envOutputer : conf.getEnvironmentOutputer()) { envOutputer->output(); }
		do {
			if (!this->_isPaused) {
				DAQmxReadAnalogF64(inputTaskHandle, SAMPLE_PER_PORT, 5.0, DAQmx_Val_GroupByScanNumber, data.data(), SAMPLE_PER_PORT, &read, NULL);
				for (int portIndex = 0; portIndex < inputPortsSize; ++portIndex) {
					float64 sampleValue = data[portIndex * SAMPLE_PER_PORT];
					std::thread t(&Event::set, inputEvents[portIndex], sampleValue);
					t.detach();
				}
			}
			else { std::this_thread::sleep_for(std::chrono::milliseconds(300)); }
		} while (isTrialRunning());
		if (conf.changeCurrentTrial() == END_OF_SESSION) { conf.setSessionComplete(true); }
	} while (!conf.isSessionComplete());
	finishSession();
}

bool SessionControls::isTrialRunning() {
	if (_isTrialRunning && std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - _trialStartTime).count() >= _trialTimeoutIndicator) {
		_isTrialRunning = false;
		LogFileWriter::getInstance().write(TRIAL_TIMEOUT_INDICATOR, "");
	}
	return _isTrialRunning;
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
	setIsPaused(true);
}

void SessionControls::resumeSession() {
	setIsPaused(false);
}

void SessionControls::nextTrial() {
	setIsTrialRuning(false);
}

void SessionControls::giveReward() {
	_conf->giveReward();
}

void SessionControls::finishSession() {
	if (!_isSessionRunning) return;
	if (_conf) { _conf->finishSession(); }
	setIsPaused(true);
	setIsSessionRunning(false);
	setIsTrialRuning(false);
	if (std::this_thread::get_id() != _runThread.get_id()) { _runThread.join(); }
}

std::string SessionControls::getCurrentRunningTrial() {
	if (_conf) { return _conf->getCurrentRunningTrial(); }
	return std::string();
}

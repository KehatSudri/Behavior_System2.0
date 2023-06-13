#define _CRT_SECURE_NO_WARNINGS

#include "SessionControls.h"
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <sstream>

using namespace System;
using namespace std;
using namespace System::Windows::Forms;

void createSessionLogFile(std::string& sessionName) {
	std::time_t now_c = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
	std::stringstream ss;
	ss << sessionName << std::put_time(std::localtime(&now_c), "-%d-%m-%Y-%T") << ".txt";
	std::string filename = ss.str();
	std::replace(filename.begin(), filename.end(), ':', ';');
	std::ofstream file(filename.c_str());
}

void SessionControls::run(char* configFilePath) {
	SessionConf conf(configFilePath);
	if (!conf.isValid()) {
		MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
		this->finishSession();
		return;
	}

	_conf = &conf;
	_timeoutIndicator = _conf->getMaxTrialWaitTime();
	do {
		TaskHandle inputTaskHandle = conf.getInputTaskHandle();
		std::vector<Event*> inputEvents = conf.getInputEvents();

		int inputPortsSize = conf.getInputEvents().size();
		std::vector<float64> data(inputPortsSize * SAMPLE_PER_PORT);
		int32 read;

		setIsTrialRuning(true);
		setIsPaused(false);
		_trialStartTime = std::chrono::high_resolution_clock::now();
		for (auto envOutputer : conf.getEnvironmentOutputer()) {
			envOutputer->output();
		}
		do {
			if (!this->_isPaused) {
				DAQmxReadAnalogF64(inputTaskHandle, SAMPLE_PER_PORT, 5.0, DAQmx_Val_GroupByScanNumber, data.data(), SAMPLE_PER_PORT, &read, NULL);
				for (int portIndex = 0; portIndex < inputPortsSize; ++portIndex) {
					float64 sampleValue = data[portIndex * SAMPLE_PER_PORT];
					std::thread t(&Event::set, inputEvents[portIndex], sampleValue);
					t.detach();
				}
			}
			else {
				std::this_thread::sleep_for(std::chrono::milliseconds(300));
			}
		} while (isTrialRunning());
		if (conf.changeCurrentTrial() == END_OF_SESSION) {
			conf.setSessionComplete(true);
		}
	} while (!conf.isSessionComplete());
	this->finishSession();
}

bool SessionControls::isTrialRunning() {
	// TODO check impact
	if (_isTrialRunning && std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - _trialStartTime).count() >= _timeoutIndicator) {
		_isTrialRunning = false;
		// TODO maybe add indicator of timeout
	}
	return _isTrialRunning;
}

void SessionControls::startSession(char* configFilePath) {
	if (_isSessionRunning) return;
	if (!configFilePath) {
		MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
		return;
	}
	createSessionLogFile(_sessionName);
	setIsSessionRunning(true);
	this->_runThread = std::thread(&SessionControls::run, this, configFilePath);
	if (_runThread.joinable()) {
		_runThread.join();
	}
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
	if (_conf) {
		_conf->finishSession();
	}
	setIsPaused(true);
	setIsSessionRunning(false);
	setIsTrialRuning(false);
	if (_conf && !_conf->isSessionComplete()) {
		if (_runThread.joinable()) {
			_runThread.join();
		}
	}
}
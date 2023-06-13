#pragma once
#ifndef __SessionControls__
#define __SessionControls__
#include "SessionConf.h"
#include <string>

public class SessionControls {
	bool _isSessionRunning = false;
	bool _isTrialRunning = false;
	bool _isPaused = false;
	int _timeoutIndicator;
	std::chrono::time_point <std::chrono::steady_clock> _trialStartTime;
	//char* _currentTrialName = "Trial name";
	SessionConf* _conf;
	std::thread _runThread;
	void run(char* configFilePath);
	bool isTrialRunning();
	std::string _sessionName;
	SessionControls() {}
	~SessionControls() {}
	SessionControls(const SessionControls&) = delete;
	SessionControls& operator=(const SessionControls&) = delete;
public:
	static SessionControls& getInstance() {
		static SessionControls instance;
		return instance;
	}
	void startSession(char* configFilePath);
	void pauseSession();
	void resumeSession();
	void finishSession();
	//char* getCurrentTrialName();
	void setIsPaused(bool state) { this->_isPaused = state; }
	void setIsSessionRunning(bool state) { this->_isSessionRunning = state; }
	void setIsTrialRuning(bool state) { this->_isTrialRunning = state; }
	void setSessionName(std::string val) { _sessionName = val; }
	bool& getIsPaused() {
		return _isPaused;
	}
	bool& getIsSessionRunning() {
		return _isSessionRunning;
	}
	void nextTrial();
	void giveReward();
};
#endif // __SessionControls__

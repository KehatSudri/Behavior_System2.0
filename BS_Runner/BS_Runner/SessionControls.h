#pragma once
#ifndef __SessionControls__
#define __SessionControls__
#include "SessionConf.h"
#include <thread>

public class SessionControls {
	bool _isSessionRunning = false;
	bool _isTrialRunning = false;
	bool _isPaused = false;
	SessionConf* _conf;
	std::thread _runThread;
	void run();
	bool isTrialRunning();
	SessionControls() {};
	~SessionControls() {};
	SessionControls(const SessionControls&) = delete;
	SessionControls& operator=(const SessionControls&) = delete;
public:
	static SessionControls& getInstance() {
		static SessionControls instance;
		return instance;
	}
	void startSession();
	void pauseSession();
	void resumeSession();
	void finishSession();
	void setIsPaused(bool state) { this->_isPaused = state; }
	void setIsSessionRunning(bool state) { this->_isSessionRunning = state; }
	void setIsTrialRuning(bool state) { this->_isTrialRunning = state; }
	bool& getIsPaused() {
		return _isPaused;
	}
	bool& getIsSessionRunning() {
		return _isSessionRunning;
	}
	void nextTrial();
	//void giveRewardIntSession();
};
#endif // __SessionControls__

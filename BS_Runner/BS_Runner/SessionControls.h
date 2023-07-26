#pragma once
#ifndef __SessionControls__
#define __SessionControls__
#include "SessionConf.h"

public class SessionControls {
	bool _isSessionRunning;
	bool _isTrialRunning;
	int _Outputing;
	bool _isPaused;
	double _trialTimeoutIndicator;
	double _sessionTimeoutIndicator;
	std::chrono::duration<double> _elapsedTime;
	std::chrono::time_point <std::chrono::steady_clock> _trialStartTime;
	std::chrono::time_point <std::chrono::steady_clock> _sessionStartTime;
	char* _currentTrialName = "Trial name";
	SessionConf* _conf;
	std::thread _runThread;
	void run(char* configFilePath);
	bool isTrialRunning();
	bool isSessionRunning();
	std::string _sessionName;
	SessionControls() {
		_isSessionRunning = false;
		_isTrialRunning = false;
		_Outputing = 0;
		_isPaused = false;
	}
	~SessionControls() {}
	SessionControls(const SessionControls&) = delete;
	SessionControls& operator=(const SessionControls&) = delete;
public:
	static SessionControls& getInstance() {
		static SessionControls instance;
		return instance;
	}
	void temp(System::Action<System::String^>^ kak) {
		System::String^ currentTrialName = gcnew System::String(_currentTrialName);
		kak(currentTrialName);
	}
	void startSession(char* configFilePath);
	void pauseSession();
	void resumeSession();
	void finishSession();
	char* getCurrentTrialName() { return _currentTrialName; };
	void setIsPaused(bool state) { _isPaused = state; }
	std::string getCurrentRunningTrial();
	void setIsSessionRunning(bool state) { _isSessionRunning = state; }
	void setIsTrialRuning(bool state) { _isTrialRunning = state; }
	bool& getIsPaused() { return _isPaused; }
	bool& getIsSessionRunning() { return _isSessionRunning; }
	bool& getIsTrialRunning() { return _isTrialRunning; }
	void incOutputing() { ++_Outputing; }
	void decOutputing() { --_Outputing; }
	void giveReward();
};
#endif // __SessionControls__

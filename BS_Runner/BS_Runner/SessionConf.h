#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#include <vector>
#include <tuple>
#include <thread>
#include <NIDAQmx.h>
#include "IOEvents.h"

class Trial {
	double _maxTrialWaitTime;
	std::vector<Event*> _events;
	std::vector<EnvironmentOutputer*> _environmentOutputer;
	TaskHandle _inputTaskHandle;
public:
	int _remainingRuns = 0;
	const std::string _trialName;
	Trial(std::string trialName) :_trialName(trialName) {}
	std::vector<std::string> _AIPorts;
	std::vector<std::tuple<std::string, std::vector<int>>> _AOPorts;
	std::vector<std::string> _trialKillers;
	void initInputEvents();
	int initAnalogOutputTasks();
	void initInputTaskHandle();
	void initTrialKillers();
	double getMaxTrialWaitTime() { return _maxTrialWaitTime; }
	void setMaxTrialWaitTime(double val) { _maxTrialWaitTime = val; }
	TaskHandle getInputTaskHandle() { return _inputTaskHandle; }
	const std::vector<EnvironmentOutputer*>& getEnvironmentOutputer() const { return _environmentOutputer; }
	std::vector<Event*> getInputEvents() const;
	void giveReward();
	~Trial();
};

public class SessionConf {
	int _numOfTrials = 0;
	int _currentTrial = 0;
	double _minITI = 0;
	double _maxITI = 0;
	bool _validFlag = true;
	bool _sessionComplete = false;
	bool _isSessionRandom = false;
	int _maxSessionWaitTime;
	std::vector<Trial> _trials;
	std::vector<int> _trialProbabilities;
	void setMinITI(double val) { _minITI = val; }
	void setMaxITI(double val) { _maxITI = val; }
	void setisSessionRandom(bool val) { _isSessionRandom = val; }
	void setMaxSessionWaitTime(int val) { _maxSessionWaitTime = val; }
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return _numOfTrials; }
	bool isValid() { return _validFlag; }
	bool isSessionComplete() { return _sessionComplete; }
	double getMaxTrialWaitTime();
	int getMaxSessionWaitTime() { return _maxSessionWaitTime; }
	void setSessionComplete(bool state) { _sessionComplete = state; }
	std::string getCurrentRunningTrial();
	int changeCurrentTrial();
	void finishSession() { _sessionComplete = true; }
	TaskHandle getInputTaskHandle();
	std::vector<EnvironmentOutputer*> getEnvironmentOutputer();
	std::vector<Event*> getInputEvents();
	void giveReward();
};
#endif // __SessionConf__

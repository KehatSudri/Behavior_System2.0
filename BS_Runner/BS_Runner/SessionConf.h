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
	std::vector<ContingentOutputer*> _contingentOutputer;
	std::vector<Outputer*> _rewardOutputers;
	TaskHandle _inputTaskHandle;
public:
	int _remainingRuns = 0;
	const std::string _trialName;
	Trial(std::string trialName) :_trialName(trialName) {}
	std::vector<std::string> _inputPorts;
	std::vector<std::tuple<std::string, std::vector<int>>> _outputPorts;
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
	void setDefaultState();
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
	double _maxSessionWaitTime;
	std::vector<Trial> _trials;
	std::vector<int> _trialProbabilities;
	void setMinITI(double val) { _minITI = val; }
	void setMaxITI(double val) { _maxITI = val; }
	void setisSessionRandom(bool val) { _isSessionRandom = val; }
	void setMaxSessionWaitTime(double val) { _maxSessionWaitTime = val; }
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return _numOfTrials; }
	bool isValid() { return _validFlag; }
	bool isSessionComplete() { return _sessionComplete; }
	double getMaxTrialWaitTime();
	double getMaxSessionWaitTime() { return _maxSessionWaitTime; }
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

#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#define OUTPUT_PARAMS_SIZE 4
#include <string>
#include <vector>
#include <tuple>
#include <thread>
#include <NIDAQmx.h>
#include "IOEvents.h"

class Trial {
	std::vector<std::string> _DOPorts;
	std::vector<Event*> _events;
	std::vector<EnvironmentOutputer*> _environmentOutputer;
	std::vector<TaskHandle> _digitalOutputTasks;
	TaskHandle _inputTaskHandle;
public:
	std::string _trialName;
	Trial(std::string trialName) :_trialName(trialName){}
	std::vector<std::string> _AIPorts;
	std::vector<std::tuple<std::string, std::vector<int>>> _AOPorts;
	std::vector<std::string> _trialKillers;
	void initInputEvents();
	void initAnalogOutputTasks();
	void initInputTaskHandle();
	void initTrialKillers();
	TaskHandle getInputTaskHandle();
	const std::vector<EnvironmentOutputer*>& getEnvironmentOutputer() const { return _environmentOutputer; }
	std::vector<Event*> getInputEvents()const ;
	~Trial();
};

public class SessionConf {
	int _numOfTrials = 0;
	int _currentTrial = 0;
	double _minITI = 0;
	double _maxITI = 0;
	bool _validFlag;
	bool _sessionComplete = false;
	std::vector<Trial> _trials;
	void setMinITI(double val) { _minITI = val; }
	void setMaxITI(double val) { _maxITI = val; }
	void performITIWait();
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return _numOfTrials; }
	bool isValid() { return _validFlag; }
	bool isSessionComplete() { return _sessionComplete; }
	void setSessionComplete(bool state) { _sessionComplete = state; }
	int changeCurrentTrial();
	void finishSession();
	TaskHandle getInputTaskHandle();
	std::vector<EnvironmentOutputer*> getEnvironmentOutputer();
	std::vector<Event*> getInputEvents();
};
#endif // __SessionConf__

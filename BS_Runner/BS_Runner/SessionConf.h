#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#define OUTPUT_PARAMS_SIZE 4
#include <string>
#include <vector>
#include <map>
#include <NIDAQmx.h>
#include "IOEvents.h"

class Trial {
public:
	std::vector<std::string> _AIPorts;
	std::map<std::string, std::vector<int>> _AOPorts;
	std::vector<std::string> _DOPorts;
	std::vector<Event*> _inputEvents;
	std::vector<SimpleOutputer*> _simpleOutputers;
	std::vector<EnvironmentOutputer*> _environmentOutputer;
	std::vector<TaskHandle> _analogOutputTasks;
	std::vector<TaskHandle> _digitalOutputTasks;
	TaskHandle _inputTaskHandle;
	//void initInputEvents();
	//void initAnalogOutputTasks();
	//void initInputTaskHandle();
};

public class SessionConf {
	//
	int _numOfTrials;
	bool _validFlag;
	std::vector<std::string> _AIPorts;
	std::map<std::string, std::vector<int>> _AOPorts;
	std::vector<std::string> _DOPorts;
	std::vector<Event*> _inputEvents;
	std::vector<SimpleOutputer*> _simpleOutputers;
	std::vector<EnvironmentOutputer*> _environmentOutputer;
	std::vector<TaskHandle> _analogOutputTasks;
	std::vector<TaskHandle> _digitalOutputTasks;
	TaskHandle _inputTaskHandle;
	// TODO move all this in trial class

	std::vector<Trial> _trials; // TODO use trial class

	//
	void initInputEvents();
	void initAnalogOutputTasks();
	void initInputTaskHandle();
	// TODO implement all this in trial class
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return this->_numOfTrials; }
	bool isValid() { return this->_validFlag; }
	TaskHandle getInputTaskHandle();
	std::vector<TaskHandle> getAnalogOutputTasks();
	std::vector<EnvironmentOutputer*> getEnvironmentOutputer() { this->_environmentOutputer; }
	std::vector<Event*> getInputEvents();
	~SessionConf();
};
#endif // __SessionConf__

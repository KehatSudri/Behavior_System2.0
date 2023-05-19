#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#define OUTPUT_PARAMS_SIZE 4
#include <string>
#include <vector>
#include <map>
#include <NIDAQmx.h>
#include "IOEvents.h"

//class OutputPort {
//	int arr[OUTPUT_PARAMS_SIZE];
//	std::string _portName;
//public:
//	OutputPort(std::string portName);
//}

public class SessionConf {
	int _numOfTrials;
	bool _validFlag;
	std::vector<std::string> _Dependencies;
	std::vector<std::string> _AIPorts;
	std::map<std::string, std::vector<int>> _AOPorts;
	std::vector<std::string> _DOPorts;
	std::vector<Event*> _inputEvents;
	std::vector<SimpleOutputer*> _simpleOutputers;
	std::vector<TaskHandle> _analogOutputTasks;
	std::vector<TaskHandle> _digitalOutputTasks;
	TaskHandle _inputTaskHandle;
	void initInputEvents();
	void initAnalogOutputTasks();
	void initInputTaskHandle();
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return this->_numOfTrials; }
	bool isValid() { return this->_validFlag; }
	TaskHandle getInputTaskHandle();
	std::vector<TaskHandle> getAnalogOutputTasks();
	std::vector<Event*> getInputEvents();
	~SessionConf();
};
#endif // __SessionConf__

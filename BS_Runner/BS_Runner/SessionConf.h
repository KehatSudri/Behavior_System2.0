#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#include <string>
#include <vector>
#include <NIDAQmx.h>
#include "IOEvents.h"

public class SessionConf {
	int _numOfTrials;
	std::string _confPath;
	std::vector<std::string> _Dependencies;
	std::vector<std::string> _AIPorts;
	std::vector<std::string> _AOPorts;
	std::vector<std::string> _DIPorts;
	std::vector<std::string> _DOPorts;
public:
	SessionConf(std::string path);
	int getNumOfTrials() { return this->_numOfTrials; }
	std::vector<std::string> getPorts(int type);
	TaskHandle getInputTaskHandle();
	std::vector<TaskHandle> getAnalogOutputTasks();
	std::vector<Event> getInputEvents();
};
#endif // __SessionConf__

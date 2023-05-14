#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#include <string>
#include <vector>

public class SessionConf {
	int _numOfTrials;
	std::string confPath_;
	std::vector<std::string> _AIPorts;
	std::vector<std::string> _AOPorts;
	std::vector<std::string> _DIPorts;
	std::vector<std::string> _DOPorts;
public:
	SessionConf(std::string path);
	std::vector<std::string> getPorts(int type);
	int getNumOfTrials() { return this->_numOfTrials; }
};
#endif // __SessionConf__

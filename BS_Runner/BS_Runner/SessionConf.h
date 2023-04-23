#pragma once
#ifndef __SessionConf__
#define __SessionConf__
#include <string>
#include <vector>

public class SessionConf {
public:
	SessionConf(std::string path);
	std::string getInputPorts(int type);
private:
	std::string confPath_;
	std::vector<std::string> AIPorts_;
	std::vector<std::string> AOPorts_;
	std::vector<std::string> DIPorts_;
	std::vector<std::string> DOPorts_;
};
#endif // __SessionConf__

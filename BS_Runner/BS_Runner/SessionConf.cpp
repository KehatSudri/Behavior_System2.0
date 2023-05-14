#include "SessionConf.h"
#include "Consts.h"

SessionConf::SessionConf(std::string path): confPath_(path) {

}

std::vector<std::string> SessionConf::getPorts(int type) {
	switch (type) {
	case AI_PORTS:
		return std::vector<std::string>{"Dev1/ai11"};
		return this->_AIPorts;
	case DI_PORTS:
		return this->_DIPorts;
	case AO_PORTS:
		return this->_AOPorts;
	case DO_PORTS:
		return this->_DOPorts;
	default:
		return std::vector<std::string>();
	}
}

/*#include "conf.h"
#include <fstream>
#include <iostream>
#include <string>


#define AI_PORTS 1
#define AO_PORTS 2
#define DI_PORTS 3
#define DO_PORTS 4

conf::conf(std::string path) : _confPath(path), _numOfTrials(0) {
	std::ifstream inputFile(path);
	if (inputFile.is_open()) {
		std::string line;
		int category = 0;
		while (std::getline(inputFile, line)) {
			if (line.empty()) {
				this->_numOfTrials++;
			}
			else {
				if (line[0] == '$')
					++category;		
				switch (category) {
				case 1:
					this->_Dependencies.push_back(line);
				case 2:
					this->_AIPorts.push_back(line);
				case 3:
					this->_AOPorts.push_back(line);
				default:
					break;
				}
				std::cout << line << '\n';
			}	
		}
		inputFile.close();
	}
	else {
		std::cerr << "Failed to open file\n";
	}
}

std::vector<std::string> conf::getPorts(int type) {
	switch (type) {
	case AI_PORTS:
		return std::vector<std::string>{"Dev1/ai11"};
		return this->_AIPorts;
	case AO_PORTS:
		return this->_AOPorts;
	case DO_PORTS:
		return this->_DOPorts;
	default:
		return std::vector<std::string>();
	}
}
*/
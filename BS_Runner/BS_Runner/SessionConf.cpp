#include "SessionConf.h"
#include "Consts.h"

SessionConf::SessionConf(std::string path): confPath_(path) {

}

std::string SessionConf::getInputPorts(int type)
{
	std::string output = std::string();
	std::vector<std::string>::iterator it;
	switch (type)
	{
	case AI_PORTS:
		output = "Dev1/ai11";
		break;
		if (AIPorts_.size() == 0) {
			break;
		}
		it = AIPorts_.begin();
		for (; it != AIPorts_.end() - 1; ++it) {
			output += *it;
			output += ",";
		}
		output += *it;
		break;
	case DI_PORTS:
		if (DIPorts_.size() == 0) {
			break;
		}
		it = DIPorts_.begin();
		for (; it != DIPorts_.end() - 1; ++it) {
			output += *it;
			output += ",";
		}
		output += *it;
		break;
	default:
		break;
	}
	return output;
}

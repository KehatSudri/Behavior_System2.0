#include "LogFileWriter.h"

void LogFileWriter::createLogFile() {
	if (!_sessionName.empty()) {
		std::time_t now_c = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
		std::stringstream ss;
		ss << _sessionName << std::put_time(std::localtime(&now_c), "-%d-%m-%Y-%T") << ".txt";
		std::string filename = ss.str();
		std::replace(filename.begin(), filename.end(), ':', ';');
		_logFileName = filename;
		std::ofstream file(filename.c_str());
	}
}

void LogFileWriter::write(std::string port) {
	std::ofstream file(_logFileName, std::ios::app);
	auto now = std::chrono::system_clock::now();
	std::time_t now_c = std::chrono::system_clock::to_time_t(now);
	size_t isInput = port.find("ai");
	if (isInput != std::string::npos) {
		file<< port <<" got input on: " << std::put_time(std::localtime(&now_c), "%T") << std::endl;
	}
	else {
		file << port << " sent output on: " << std::put_time(std::localtime(&now_c), "%T") << std::endl;
	}
	file.close();

}

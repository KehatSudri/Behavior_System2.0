#define _CRT_SECURE_NO_WARNINGS

#include "LogFileWriter.h"
#include "Consts.h"

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


void LogFileWriter::write(int indicator, std::string port) {
	std::ofstream file(_logFileName, std::ios::app);
	auto now = std::chrono::system_clock::now();
	std::time_t now_c = std::chrono::system_clock::to_time_t(now);
	auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

	std::ostringstream message;
	switch (indicator) {
	case OUTPUT_INDICATOR:
		message << " Sent output at: ";
		break;
	case INPUT_INDICATOR:
		message << " Got input at: ";
		break;
	case TRIAL_END_CONDITION_INDICATOR:
		message << "Reached end condition at: ";
		break;
	case TRIAL_TIMEOUT_INDICATOR:
		message << "Trial Timeout at: ";
		break;
	case TRIAL_START:
		message << " started at: ";
		break;
	case SESSION_TIMEOUT_INDICATOR:
		message << "Session Timeout at: ";
		break;
	case SESSION_END:
		message << "Session Finished at: ";
		break;
	default:
		message << " Undefined indicator at: ";
		break;
	}

	message << std::put_time(std::localtime(&now_c), "%T") << "." << std::setfill('0') << std::setw(3) << ms.count() << std::endl;
	file << port << message.str();
	file.close();
}

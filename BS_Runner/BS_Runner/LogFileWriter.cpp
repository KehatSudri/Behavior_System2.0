#define _CRT_SECURE_NO_WARNINGS

#include "LogFileWriter.h"
#include "Consts.h"
#include <iostream>

void LogFileWriter::createLogFile() {
	if (!_sessionName.empty()) {
		std::time_t now_c = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
		std::stringstream ss;
		ss << std::put_time(std::localtime(&now_c), "-%d-%m-%Y-%T");
		std::string time = ss.str();
		std::replace(time.begin(), time.end(), ':', ';');
		_logFileName = _dir + "\\" + _sessionName +"_" + time + ".txt";
		std::ofstream MyFile(_logFileName);
		MyFile.close();
	}
}


void LogFileWriter::write(int indicator, std::string port) {
	std::ofstream file(_logFileName, std::ios::app);
	auto now = std::chrono::system_clock::now();
	std::time_t now_c = std::chrono::system_clock::to_time_t(now);
	auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

	std::ostringstream message;
	switch (indicator) {
	case OUTPUT_START_INDICATOR:
		message << " S output at: ";
		break;
	case OUTPUT_FINISH_INDICATOR:
		message << " F output at: ";
		break;
	case INPUT_START_INDICATOR:
		message << " G input at: ";
		break;
	case INPUT_FINISH_INDICATOR:
		message << " L input at: ";
		break;
	case TRIAL_END_CONDITION_INDICATOR:
		message << "Reached end condition at: ";
		break;
	case TRIAL_TIMEOUT_INDICATOR:
		message << "Trial Timeout at: ";
		break;
	case TRIAL_START_INDICATOR:
		message << " started at: ";
		break;
	case SESSION_TIMEOUT_INDICATOR:
		message << "Session Timeout at: ";
		break;
	case SESSION_END_INDICATOR:
		message << "Session Finished at: ";
		break;
	case TRIAL_END_INDICATOR:
		message << " Finished at: ";
		break;
	case REWARD_INDICATOR:
		message << "Gave reward at: ";
	default:
		message << " Undefined indicator at: ";
		break;
	}

	message << std::put_time(std::localtime(&now_c), "%T") << "." << std::setfill('0') << std::setw(3) << ms.count() << std::endl;
	file << port << message.str();
	file.close();
}

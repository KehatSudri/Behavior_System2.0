#pragma once
#ifndef __LogFileWriter__
#define __LogFileWriter__

#include <Windows.h>
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <string>
#include <thread>

public class LogFileWriter {
	std::string _sessionName;
	std::string _subjectId;
	std::string _experimenterName;
	std::string _dir;
	std::string _logFileName;

	std::ofstream _logFile;

	CRITICAL_SECTION _criticalSection;

	LogFileWriter() {
		InitializeCriticalSection(&_criticalSection);
	}

	~LogFileWriter() {
		if (_logFile.is_open()) {
			_logFile.close();
		}
		DeleteCriticalSection(&_criticalSection);
	}

	LogFileWriter(const LogFileWriter&) = delete;
	LogFileWriter& operator=(const LogFileWriter&) = delete;
public:
	static LogFileWriter& getInstance() {
		static LogFileWriter instance;
		return instance;
	}
	void setSessionName(std::string sessionName) { _sessionName = sessionName; }
	void setLogDirectory(std::string dir) { _dir = dir; }
	void setSubjectId(std::string subjectId) { _subjectId = subjectId; }
	void setExperimenterMame(std::string experimenterMame) { _experimenterName = experimenterMame; }

	void createLogFile();
	void write(int indicator, const std::string& port);
};

#endif // __LogFileWriter__
#pragma once
#ifndef __LogFileWriter__
#define __LogFileWriter__

#include <algorithm>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <string>
#include <thread>

public class LogFileWriter {
	std::string _sessionName;
	std::string _subjectId;
	std::string _experimenterMame;
	std::string _dir;
	std::string _logFileName;
	LogFileWriter() {}
	~LogFileWriter() {}
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
	void setExperimenterMame(std::string experimenterMame) { _experimenterMame = experimenterMame; }
	void createLogFile();
	void write(int indicator, std::string port);
};

#endif // __LogFileWriter__
#pragma once
#ifndef __SessionControls__
#define __SessionControls__
#include <thread>

public class SessionControls {
	bool _isRunning;
	bool _isPaused;
	std::thread _runThread;
	void run();

	SessionControls();
	~SessionControls() {};
	SessionControls(const SessionControls&) = delete;
	SessionControls& operator=(const SessionControls&) = delete;
public:
	static SessionControls& getInstance() {
		static SessionControls instance;
		return instance;
	}
	void startSession();
	void pauseSession();
	void resumeSession();
	void finishSession();
	bool& getIsPaused() {
		return _isPaused;
	}
	bool& getIsRunning() {
		return _isRunning;
	}
	//void giveRewardIntSession();
};
#endif // __SessionControls__

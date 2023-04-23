#pragma once
#ifndef __SessionControls__
#define __SessionControls__
#include <thread>

public class SessionControls {
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
		return isPaused_;
	}
	bool& getIsRunning() {
		return isRunning_;
	}
	//void giveRewardIntSession();
private:
	SessionControls();
	~SessionControls() {};
	SessionControls(const SessionControls&) = delete;
	SessionControls& operator=(const SessionControls&) = delete;
	void run();
	bool isRunning_;
	bool isPaused_;
	std::thread t_;
};
#endif // __SessionControls__

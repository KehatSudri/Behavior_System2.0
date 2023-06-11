#include "IOEvents.h"
#include "SessionControls.h"
#include "Consts.h"
#include <thread>
#include <iostream>


void writeDigitalOutput(TaskHandle taskHandle, int duration) {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	uInt32 data = 4;  // Value to write
	DAQmxWriteDigitalScalarU32(taskHandle, true, duration/1000, data, NULL);
}

void Event::attachListener(Listener* listener) {
	_listeners.push_back(listener);
}

void Event::detachListener(Listener* listener) {
	auto it = std::find(_listeners.begin(), _listeners.end(), listener);
	if (it != _listeners.end()) {
		_listeners.erase(it);
	}
}

void Event::notifyListeners() {
	for (auto& listener : _listeners) {
		listener->update(this);
	}
}

void Event::set(float64 value) {
	if (!_beenUpdated && value > 3.5) {
		_beenUpdated = true;
		notifyListeners();
	}
	else if (_beenUpdated && value < 3.5) {
		_beenUpdated = false;
	}
}

void SimpleAnalogOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	auto start_time = std::chrono::high_resolution_clock::now();
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DELAY_PARAM]) {
		continue;
	}
	start_time = std::chrono::high_resolution_clock::now();
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 3.7, NULL);
	notifyListeners();
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DURATION_PARAM]) {
		continue;
	}
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 0.0, NULL);
}

void SimpleDigitalOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	auto start_time = std::chrono::high_resolution_clock::now();
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DELAY_PARAM]) {
		continue;
	}
	uInt32 data = 4;
	start_time = std::chrono::high_resolution_clock::now();
	DAQmxWriteDigitalScalarU32(_handler, true, _attributes[DURATION_PARAM] / 1000, data, NULL);
	notifyListeners();
}

void EnvironmentOutputer::output() {
	std::thread t(&Outputer::output, _outputer);
	t.detach();
}

void ContingentOutputer::update(Event* event) {
	std::thread t(&Outputer::output, _outputer);
	t.detach();
}

void SerialOutputer::run() {
	bool& isRunning = SessionControls::getInstance().getIsSessionRunning();
	bool& isPaused = SessionControls::getInstance().getIsPaused();
	while (isRunning) {
		if (!isPaused) {
			_outputer->output();
		}
	}
}

void TrialKiller::update(Event* event) {
	SessionControls::getInstance().setIsTrialRuning(false);
}

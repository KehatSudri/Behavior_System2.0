#include "IOEvents.h"
#include "SessionControls.h"
#include "Consts.h"
#include <thread>
#include <iostream>


void writeOutput(TaskHandle taskHandle, int duration) {
    DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 3.7, NULL);
    auto start_time = std::chrono::high_resolution_clock::now();
    while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < duration) {
        continue;
    }
    DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 0.0, NULL);
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

void SimpleOutputer::output() {
    auto start_time = std::chrono::high_resolution_clock::now();
    while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DELAY_PARAM]) {
        continue;
    }
    notifyListeners();
    writeOutput(_handler, _attributes[DURATION_PARAM]);
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

void SessionKiller::update(Event* event) {
    SessionControls::getInstance().setIsSessionRunning(false);
}

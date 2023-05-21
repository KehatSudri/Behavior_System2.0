#include "IOEvents.h"
#include "SessionControls.h"
#include "Consts.h"
#include <thread>
#include <iostream>


void writeOutput(TaskHandle taskHandle, int duration, int delay = 0) {
    auto start_time = std::chrono::high_resolution_clock::now();
    while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < delay) {
        continue;
    }
    DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 3.7, NULL);
    start_time = std::chrono::high_resolution_clock::now();
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
    for (auto listener : this->_listeners) {
        listener->update(this);
    }
}

void Event::set(float64 value) {
    if (!this->_beenUpdated && value > 3.5) {       
        this->_beenUpdated = true;
        notifyListeners();
    }
    else if (this->_beenUpdated && value < 3.5) {
        this->_beenUpdated = false;
    }
}

void SimpleOutputer::output() {
    writeOutput(_handler, _attributes[DURATION_PARAM], _attributes[DELAY_PARAM]);
}

void EnvironmentOutputer::output() {
    std::thread t(&Outputer::output, this->_outputer);
    t.detach();
}

void ContingentOutputer::update(Event* event) {
    std::thread t(&Outputer::output, this->_outputer);
    t.detach();
}

void SerialOutputer::run() {
    bool& isRunning = SessionControls::getInstance().getIsSessionRunning();
    bool& isPaused = SessionControls::getInstance().getIsPaused();
    while (isRunning) {
        if (!isPaused) {
            this->_outputer->output();
        }
    }
}

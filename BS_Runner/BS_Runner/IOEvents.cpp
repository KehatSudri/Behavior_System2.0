#include "IOEvents.h"
#include "SessionControls.h"
#include <thread>

void writeOutput(TaskHandle taskHandle, int duration, int delay = 0) {
    auto start_time = std::chrono::high_resolution_clock::now();
    while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < delay) {
        continue;
    }
    DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 4.0, NULL);
    start_time = std::chrono::high_resolution_clock::now();
    while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < duration) {
        continue;
    }
    DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 0.0, NULL);
}

void Event::attachListener(Listener* listener) {
    listeners_.push_back(listener);
}

void Event::detachListener(Listener* listener) {
    auto it = std::find(listeners_.begin(), listeners_.end(), listener);
    if (it != listeners_.end()) {
        listeners_.erase(it);
    }
}

void Event::notifyListeners() {
    for (auto listener : listeners_) {
        listener->update(this);
    }
}

void Event::set(float64 value) {
    if (!this->beenUpdated_ && value > 3.5) {       
        this->beenUpdated_ = true;
        notifyListeners();
    }
    else if (this->beenUpdated_ && value < 3.5) {
        this->beenUpdated_ = false;
    }
}

void SimpleOutputer::output() {
    writeOutput(handler_, duration_, delay_);
}

void EnvironmentOutputer::output() {
    std::thread t(&Outputer::output, this->outputer_);
    t.detach();
}

void ContingentOutputer::update(Event* event) {
    std::thread t(&Outputer::output, this->outputer_);
    t.detach();
}

void SerialOutputer::run() {
    bool& isRunning = SessionControls::getInstance().getIsRunning();
    bool& isPaused = SessionControls::getInstance().getIsPaused();
    while (isRunning) {
        if (!isPaused) {
            this->outputer_->output();
        }
    }
}

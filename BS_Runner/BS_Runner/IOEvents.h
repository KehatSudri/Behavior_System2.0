#pragma once
#ifndef __IOEvents__
#define __IOEvents__
#include <vector>
#include <NIDAQmx.h>

void writeOutput(TaskHandle taskHandle, int delay, int duration);

class Listener;

class Event {
public:
    Event() {
        beenUpdated_ = false;
    }
    void attachListener(Listener* listener);
    void detachListener(Listener* listener);
    void notifyListeners();
    void update(float value);
private:
    std::vector<Listener*> listeners_;
    bool beenUpdated_;
};

class Listener {
public:
    virtual void update(Event* event) = 0;
};

class SimpleOutputer {
public:
    SimpleOutputer(TaskHandle handler, int delay, int duration, int frequency) : handler_(handler), delay_(delay), duration_(duration), frequency_(frequency) {
        isOutputing_ = false;
    }
    void run();
    bool getIsOutputing_() {
        return isOutputing_;
    }
private:
    TaskHandle handler_;
    int delay_;
    int duration_;
    int frequency_;
    bool isOutputing_;
};

class ContingentOutputer : public Listener{
public:
    ContingentOutputer(TaskHandle handler, int delay, int duration) : handler_(handler), delay_(delay), duration_(duration) {}
    void update(Event* event) override;
private:
    TaskHandle handler_;
    int delay_;
    int duration_;
};

class ComplexListener : public ContingentOutputer, public SimpleOutputer {
public:
    ComplexListener(TaskHandle handler, int delay, int duration, int frequency) : ContingentOutputer(handler, delay, duration), SimpleOutputer(handler, delay, duration, frequency) {}
    void update(Event* event) override;
};
#endif // __IOEvents__

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
    void set(float64 value);
private:
    std::vector<Listener*> listeners_;
    bool beenUpdated_;
};

class Listener {
public:
    virtual void update(Event* event) = 0;
};

class Outputer {
public:
    Outputer(TaskHandle handler, int duration, int delay = 0 , int frequency = 0) : handler_(handler), delay_(delay), duration_(duration), frequency_(frequency) {}
    virtual void output() = 0;
protected:
    TaskHandle handler_;
    int delay_;
    int duration_;
    int frequency_;
};

class SimpleOutputer : public Outputer {
public:
    SimpleOutputer(TaskHandle handler, int duration, int delay = 0, int frequency = 0) : Outputer(handler, duration, delay, frequency) {}
    void output() override;
};

class EnvironmentOutputer {
public:
    EnvironmentOutputer(Outputer* outputer) : outputer_(outputer) {}
    void output();
private:
    Outputer* outputer_;
};

class ContingentOutputer : public Listener {
public:
    ContingentOutputer(Outputer* outputer) : outputer_(outputer) {}
    void update(Event* event) override;
private:
    Outputer* outputer_;
};

class SerialOutputer {
public:
    SerialOutputer(Outputer* outputer) : outputer_(outputer) {}
    void run();

private:
    Outputer* outputer_;
};

#endif // __IOEvents__

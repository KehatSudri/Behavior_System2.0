#pragma once
#ifndef __IOEvents__
#define __IOEvents__
#include <NIDAQmx.h>
#include <vector>
#include <map>
#include <string>

void writeOutput(TaskHandle taskHandle, int delay, int duration);

class Listener;

class Event {
    std::vector<Listener*> _listeners;
    std::string _port;
    bool _beenUpdated;
public:
    Event(std::string port) : _port(port), _beenUpdated(false) {}
    std::string getPort() { return this->_port; }
    void attachListener(Listener* listener);
    void detachListener(Listener* listener);
    void notifyListeners();
    int gaga() {
        return _listeners.size();
    }
    void set(float64 value);
};

class Listener {
public:
    virtual void update(Event* event) = 0;
};

class Outputer {
public:
    Outputer(TaskHandle handler, std::map<std::string, int> attributes) : _attributes(attributes){}
    virtual void output() = 0;
protected:
    TaskHandle _handler;
    std::map<std::string, int> _attributes;
};

class SimpleOutputer : public Outputer {
public:
    SimpleOutputer(TaskHandle handler, std::map<std::string, int> attributes) : Outputer(handler, attributes) {}
    void output() override;
};

class EnvironmentOutputer {
public:
    EnvironmentOutputer(Outputer* outputer) : _outputer(outputer) {}
    void output();
private:
    Outputer* _outputer;
};

class ContingentOutputer : public Listener {
public:
    ContingentOutputer(Outputer* outputer) : _outputer(outputer) {}
    void update(Event* event) override;
private:
    Outputer* _outputer;
};

class SerialOutputer {
public:
    SerialOutputer(Outputer* outputer) : _outputer(outputer) {}
    void run();

private:
    Outputer* _outputer;
};

#endif // __IOEvents__

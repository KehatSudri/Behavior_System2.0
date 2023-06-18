#pragma once
#ifndef __IOEvents__
#define __IOEvents__
#include <NIDAQmx.h>
#include <iostream>
#include <vector>
#include <map>
#include "LogFileWriter.h"

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
	void set(float64 value);
};

class Listener {
public:
	virtual void update(Event* event) = 0;
};

class Outputer : public Event {
public:
	Outputer(TaskHandle handler, std::string port, std::map<std::string, int> attributes) :Event(port), _handler(handler), _attributes(attributes) {}
	virtual void output() = 0;
protected:
	TaskHandle _handler;
	std::map<std::string, int> _attributes;
};

class SimpleAnalogOutputer : public Outputer {
public:
	SimpleAnalogOutputer(TaskHandle handler, std::string port, std::map<std::string, int> attributes) : Outputer(handler, port, attributes) {}
	void output() override;
};

class SimpleDigitalOutputer : public Outputer {
public:
	SimpleDigitalOutputer(TaskHandle handler, std::string port, std::map<std::string, int> attributes) : Outputer(handler, port, attributes) {}
	void output() override;
};

class SimpleToneOutputer : public Outputer {
	std::string _wav;
public:
	SimpleToneOutputer(std::string port, std::map<std::string, int> attributes);
	void output() override;
};

class TrialKiller : public Listener {
public:
	void update(Event* event) override;
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

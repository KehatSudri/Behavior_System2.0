#pragma once
#ifndef __IOEvents__
#define __IOEvents__
#include <NIDAQmx.h>
#include <iostream>
#include <vector>
#include <map>
#include <random>
#include <numeric>
#include "Consts.h"
#include "LogFileWriter.h"

class Listener;

class Event {
	std::vector<Listener*> _listeners;
	std::string _port;
	bool _started;
	bool _beenUpdated;
public:
	Event(std::string port) : _port(port), _beenUpdated(false), _started(false) {}
	std::string getPort() { return this->_port; }
	void setDefaultState() {
		_started = false;
		_beenUpdated = false;
	}
	~Event();
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
	Outputer(TaskHandle handler, std::string port, std::map<std::string, int> attributes, bool metPrecon = true) :Event(port), _handler(handler), _attributes(attributes) {
		_metPreCon = metPrecon;
	}
	void updateMetPrecon(bool state) { _metPreCon = state; }
	bool getMetPreCon() { return _metPreCon; }
	bool getIsReward() { return _attributes[IS_REWARD_PARAM]; }
	virtual void output() = 0;
protected:
	bool _metPreCon;
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
	~SimpleToneOutputer() {};
	void output() override;
};

class TrialKiller : public Listener {
public:
	void update(Event* event) override;
};

class EnvironmentOutputer {
	Outputer* _outputer;
public:
	EnvironmentOutputer(Outputer* outputer) : _outputer(outputer) {}
	void output();
};

class ContingentOutputer : public Listener {
	bool _gaveReward;
	bool _isReward;
	std::string _preCon;
	Outputer* _outputer;
public:
	ContingentOutputer(Outputer* outputer, std::string preCon = "None") : _outputer(outputer), _preCon(preCon) {
		_gaveReward = false;
		_isReward = _outputer->getIsReward();
		if (preCon != "None") {
			_outputer->updateMetPrecon(false);
		}
	}
	bool getGaveReward() { return _gaveReward; }
	bool getMetPreCon() { return _outputer->getMetPreCon(); }
	void updateRewardState(bool state) { _gaveReward = state; }
	void setDefaultState();
	void update(Event* event) override;
};

class SerialOutputer {
	Outputer* _outputer;
public:
	SerialOutputer(Outputer* outputer) : _outputer(outputer) {}
	void run();
};

#endif // __IOEvents__

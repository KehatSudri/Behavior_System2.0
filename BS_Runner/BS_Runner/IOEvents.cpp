#define _CRT_SECURE_NO_WARNINGS

#include <windows.h>
#include "IOEvents.h"
#include "SessionControls.h"
#include "Consts.h"

struct WAVHeader {
	char chunkId[4] = { 'R', 'I', 'F', 'F' };
	int chunkSize = 0;
	char format[4] = { 'W', 'A', 'V', 'E' };
	char subchunk1Id[4] = { 'f', 'm', 't', ' ' };
	int subchunk1Size = 16;
	short audioFormat = 1;
	short numChannels = 1;
	int sampleRate = SAMPLE_RATE;
	int byteRate = SAMPLE_RATE * sizeof(short);
	short blockAlign = sizeof(short);
	short bitsPerSample = 8 * sizeof(short);
	char subchunk2Id[4] = { 'd', 'a', 't', 'a' };
	int subchunk2Size = 0;
};

void performDelay(std::map<std::string, int>& attr) {
	if (attr[MAX_DELAY_PARAM]) {
		return;
	}
	auto start_time = std::chrono::high_resolution_clock::now();
	if (attr[MAX_DELAY_PARAM]) {
		std::random_device rd;
		std::mt19937 gen(rd());
		std::uniform_real_distribution<double> dis(attr[MIN_DELAY_PARAM], attr[MAX_DELAY_PARAM]);
		double random_iti = dis(gen);
		while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < random_iti) { continue; }
	}
	else {
		while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < attr[DELAY_PARAM]) { continue; }
	}
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
	if (!_beenUpdated && value > 2) {
		_beenUpdated = true;
		notifyListeners();
		LogFileWriter::getInstance().write(INPUT_INDICATOR, this->getPort());
	}
	else if (_beenUpdated && value < 2) {
		_beenUpdated = false;
	}
}

void SimpleAnalogOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	performDelay(_attributes);
	auto start_time = std::chrono::high_resolution_clock::now();
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 3.7, NULL);
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_INDICATOR, this->getPort());
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DURATION_PARAM]) {
		continue;
	}
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 0.0, NULL);
}

void SimpleDigitalOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	performDelay(_attributes);
	uInt8 dataHigh[] = { 1 };
	uInt8 dataLow[] = { 0 };
	auto start_time = std::chrono::high_resolution_clock::now();
	DAQmxWriteDigitalLines(_handler, 1, 1, 10.0, DAQmx_Val_GroupByChannel, dataHigh, NULL, nullptr);
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_INDICATOR, this->getPort());
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DURATION_PARAM]) {
		continue;
	}
	DAQmxWriteDigitalLines(_handler, 1, 1, 10.0, DAQmx_Val_GroupByChannel, dataLow, NULL, nullptr);
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
	LogFileWriter::getInstance().write(TRIAL_END_CONDITION_INDICATOR, "");
}

SimpleToneOutputer::SimpleToneOutputer(std::string port, std::map<std::string, int> attributes) : Outputer(NULL, port, attributes) {
	int numSamples = static_cast<int>(SAMPLE_RATE * attributes[DURATION_PARAM]/1000);
	WAVHeader header;
	header.chunkSize = 36 + numSamples * sizeof(short);
	header.subchunk2Size = numSamples * sizeof(short);
	std::time_t now_c = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
	std::stringstream ss;
	ss << attributes[FREQUENCY_PARAM] << ".wav";
	std::string filename = ss.str();
	std::replace(filename.begin(), filename.end(), ':', ';');
	_wav = filename;
	std::ofstream file(filename.c_str(), std::ios::binary);
	file.write(reinterpret_cast<const char*>(&header), sizeof(header));
	for (int i = 0; i < numSamples; i++) {
		double t = static_cast<double>(i) / SAMPLE_RATE;
		double value = sin(TWO_PI * attributes[FREQUENCY_PARAM] * t);
		short sample = static_cast<short>(value * 32767);
		file.write(reinterpret_cast<const char*>(&sample), sizeof(sample));
	}
	file.close();
}

void SimpleToneOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) {
		continue;
	}
	performDelay(_attributes);
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_INDICATOR, this->getPort());
	std::wstring filePathWide(this->_wav.begin(), this->_wav.end());
	LPCWSTR filePath = filePathWide.c_str();
	PlaySound(filePath, NULL, SND_FILENAME);
	return;
}
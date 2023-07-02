#define _CRT_SECURE_NO_WARNINGS

#include <windows.h>
#include "IOEvents.h"
#include "SessionControls.h"

//struct WAVHeader {
//	char chunkId[4] = { 'R', 'I', 'F', 'F' };
//	int chunkSize = 0;
//	char format[4] = { 'W', 'A', 'V', 'E' };
//	char subchunk1Id[4] = { 'f', 'm', 't', ' ' };
//	int subchunk1Size = 16;
//	short audioFormat = 1;
//	short numChannels = 1;
//	int sampleRate = SAMPLE_RATE;
//	int byteRate = SAMPLE_RATE * sizeof(short);
//	short blockAlign = sizeof(short);
//	short bitsPerSample = 8 * sizeof(short);
//	char subchunk2Id[4] = { 'd', 'a', 't', 'a' };
//	int subchunk2Size = 0;
//};


struct WaveHeader {
	char chunkId[5];
	int chunkSize;
	char format[5];
	char subchunk1Id[5];
	int subchunk1Size;
	short audioFormat;
	short numChannels;
	int sampleRate;
	int byteRate;
	short blockAlign;
	short bitsPerSample;
	char subchunk2Id[5];
	int subchunk2Size;
};

void performDelay(std::map<std::string, int>& attr) {
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
	if (!_beenUpdated && value > MIN_THRESHOLD && _started) {
		_beenUpdated = true;
		LogFileWriter::getInstance().write(INPUT_START_INDICATOR, this->getPort());
		notifyListeners();
	}
	else if (_beenUpdated && value < MIN_THRESHOLD) {
		_beenUpdated = false;
		LogFileWriter::getInstance().write(INPUT_FINISH_INDICATOR, this->getPort());
	}
	else if (!_started && value < MIN_THRESHOLD) {
		_started = true;
	}
}

void SimpleAnalogOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) { continue; }
	performDelay(_attributes);
	auto start_time = std::chrono::high_resolution_clock::now();
	if (!SessionControls::getInstance().getIsTrialRunning()) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	if (!_metPreCon) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 3.7, NULL);
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_START_INDICATOR, this->getPort());
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DURATION_PARAM]) {
		continue;
	}
	DAQmxWriteAnalogScalarF64(_handler, true, 5.0, 0.0, NULL);
	LogFileWriter::getInstance().write(OUTPUT_FINISH_INDICATOR, this->getPort());
	SessionControls::getInstance().decOutputing();
}

void SimpleDigitalOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) { continue; }
	performDelay(_attributes);
	uInt8 dataHigh[] = { 1 };
	uInt8 dataLow[] = { 0 };
	auto start_time = std::chrono::high_resolution_clock::now();
	if (!SessionControls::getInstance().getIsTrialRunning()) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	if (!_metPreCon) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	DAQmxWriteDigitalLines(_handler, 1, 1, 10.0, DAQmx_Val_GroupByChannel, dataHigh, NULL, nullptr);
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_START_INDICATOR, this->getPort());
	while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < _attributes[DURATION_PARAM]) {
		continue;
	}
	DAQmxWriteDigitalLines(_handler, 1, 1, 10.0, DAQmx_Val_GroupByChannel, dataLow, NULL, nullptr);
	LogFileWriter::getInstance().write(OUTPUT_FINISH_INDICATOR, this->getPort());
	SessionControls::getInstance().decOutputing();
}

void EnvironmentOutputer::output() {
	SessionControls::getInstance().incOutputing();
	std::thread t(&Outputer::output, _outputer);
	t.detach();
}

void ContingentOutputer::setDefaultState() {
	updateRewardState(false);
	if (_preCon != "None") {
		_outputer->updateMetPrecon(false);
	}
}

void ContingentOutputer::update(Event* event) {
	if (_isReward && _gaveReward) { return; }
	if (_preCon != "None" && event->getPort() == _preCon) {
		_outputer->updateMetPrecon(true);
		return;
	}
	SessionControls::getInstance().incOutputing();
	std::thread t(&Outputer::output, _outputer);
	t.detach();
	if (_outputer->getMetPreCon()) {
		updateRewardState(true);
	}
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
	/*int numSamples = static_cast<int>(SAMPLE_RATE * attributes[DURATION_PARAM] / 1000);
	numSamples /= 2;
	WAVHeader header;
	header.chunkSize = 36 + numSamples * sizeof(short);
	header.subchunk2Size = numSamples * sizeof(short);
	std::time_t now_c = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
	std::stringstream ss;
	ss << attributes[FREQUENCY_PARAM] << "_" << attributes[DURATION_PARAM] << ".wav";
	std::string wav_file = ss.str();
	std::string filename = "wav_files\\" + wav_file;
	_wav = filename;
	std::ofstream file(filename.c_str(), std::ios::binary);
	file.write(reinterpret_cast<const char*>(&header), sizeof(header));
	for (int i = 0; i < numSamples; i++) {
		double t = static_cast<double>(i) / SAMPLE_RATE;
		double value = sin(TWO_PI * attributes[FREQUENCY_PARAM] * t);
		short sample = static_cast<short>(value * 32767);
		file.write(reinterpret_cast<const char*>(&sample), sizeof(sample));
	}
	file.close();*/
	WaveHeader header;
	int numSamples = static_cast<int>(SAMPLE_RATE * attributes[DURATION_PARAM] / 1000);
	std::vector<short> buffer(numSamples);

	strcpy(header.chunkId, "RIFF");
	header.chunkSize = 4 + (8 + 16) + (8 + numSamples * 2);
	strcpy(header.format, "WAVE");
	strcpy(header.subchunk1Id, "fmt ");
	header.subchunk1Size = 16;
	header.audioFormat = 1;
	header.numChannels = 1;
	header.sampleRate = SAMPLE_RATE;
	header.byteRate = SAMPLE_RATE * header.numChannels * 2;
	header.blockAlign = header.numChannels * 2;
	header.bitsPerSample = 16;
	strcpy(header.subchunk2Id, "data");
	header.subchunk2Size = numSamples * 2;

	for (int i = 0; i < numSamples; ++i) {
		double time = i / SAMPLE_RATE;
		buffer[i] = MAX_AMPLITUDE * sin(TWO_PI * attributes[FREQUENCY_PARAM] * time);
	}

	std::stringstream ss;
	ss << attributes[FREQUENCY_PARAM] << "_" << attributes[DURATION_PARAM] << ".wav";
	std::string wav_file = ss.str();
	std::string filename = "wav_files\\" + wav_file;
	_wav = filename;

	std::ofstream outFile(_wav, std::ios::binary);
	outFile.write((const char*)&header, sizeof(WaveHeader));
	outFile.write((const char*)buffer.data(), buffer.size() * sizeof(short));
	outFile.close();
}

void SimpleToneOutputer::output() {
	while (SessionControls::getInstance().getIsPaused()) { continue; }
	performDelay(_attributes);
	if (!SessionControls::getInstance().getIsTrialRunning()) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	if (!_metPreCon) {
		SessionControls::getInstance().decOutputing();
		return;
	}
	notifyListeners();
	LogFileWriter::getInstance().write(OUTPUT_START_INDICATOR, getPort());
	PlaySoundA(_wav.c_str(), NULL, SND_FILENAME);
	LogFileWriter::getInstance().write(OUTPUT_FINISH_INDICATOR, getPort());
	SessionControls::getInstance().decOutputing();
	return;
}
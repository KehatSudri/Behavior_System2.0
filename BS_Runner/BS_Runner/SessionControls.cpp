#include "SessionControls.h"
#include "Consts.h"
#include "IOEvents.h"
#include <iostream>
#include <thread>

using namespace System;
using namespace std;
using namespace System::Windows::Forms;

void SessionControls::run(char * configFilePath) {
    TaskHandle ao0InputMocker_TaskHandle = NULL;
    DAQmxCreateTask("", &ao0InputMocker_TaskHandle);
    DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    std::map<std::string, int> attr;
    attr[DELAY_PARAM] = 100;
    attr[DURATION_PARAM] = 50;
    SerialOutputer ao0InputMocker(new SimpleOutputer(ao0InputMocker_TaskHandle, attr));
    std::thread t1(&SerialOutputer::run, &ao0InputMocker);
    SessionConf conf(configFilePath);
    if (!conf.isValid()) {
        // TODO Needs work
        MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
        DAQmxClearTask(ao0InputMocker_TaskHandle);
        t1.join();
        finishSession();
    }

    _conf = &conf;
    while (!conf.isSessionComplete()) {
        TaskHandle inputTaskHandle = conf.getInputTaskHandle();
        std::vector<Event*> inputEvents = conf.getInputEvents();

        int inputPortsSize = conf.getInputEvents().size();
        std::vector<float64> data(inputPortsSize * SAMPLE_PER_PORT);
        int32 read;

        for (auto envOutputer : conf.getEnvironmentOutputer()) {
            envOutputer->output();
        }
        setIsTrialRuning(true);
        while (isTrialRunning()) {
            if (!_isPaused) {
                DAQmxReadAnalogF64(inputTaskHandle, SAMPLE_PER_PORT, 5.0, DAQmx_Val_GroupByScanNumber, data.data(), SAMPLE_PER_PORT, &read, NULL);
                for (int portIndex = 0; portIndex < inputPortsSize; ++portIndex) {
                    float64 sampleValue = data[portIndex * SAMPLE_PER_PORT];
                    std::thread t(&Event::set, inputEvents[portIndex], sampleValue);
                    t.detach();
                }
            }
            else {
                std::this_thread::sleep_for(std::chrono::milliseconds(300));
            }
        }
        conf.changeCurrentTrial();
    }
    t1.join();
    DAQmxClearTask(ao0InputMocker_TaskHandle);
}

bool SessionControls::isTrialRunning() {
    // TODO Add finish goals for trial
    return _isTrialRunning;
}

void SessionControls::startSession(char* configFilePath) {
    if (_isSessionRunning) return;
    setIsSessionRunning(true);
    setIsTrialRuning(true);
    setIsPaused(false);
    _runThread = std::thread(&SessionControls::run, this, configFilePath);
}

void SessionControls::pauseSession() {
    setIsPaused(true);
}

void SessionControls::resumeSession() {
    setIsPaused(false);
}

void SessionControls::nextTrial() {
    setIsTrialRuning(false);
}

void SessionControls::finishSession() {
    if (!_isSessionRunning) return;
    _conf->finishSession();
    setIsPaused(true);
    setIsSessionRunning(false);
    setIsTrialRuning(false);
    _runThread.join();
}
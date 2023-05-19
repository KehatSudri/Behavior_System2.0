#include "SessionControls.h"
#include "SessionConf.h"
#include "Consts.h"
#include "IOEvents.h"
#include <iostream>
#include <thread>

using namespace System;
using namespace std;
using namespace System::Windows::Forms;

SessionControls::SessionControls() {
    this->_isRunning = false;
    this->_isPaused = false;
}

std::thread serialOutputMock() {
    TaskHandle ao0InputMocker_TaskHandle = NULL;
    DAQmxCreateTask("inputMocker", &ao0InputMocker_TaskHandle);
    DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    int mockerDelay = 100;
    int mockerDuration = 50;
    SimpleOutputer* sm1 = new SimpleOutputer(ao0InputMocker_TaskHandle, mockerDuration, mockerDelay);
    SerialOutputer ao0InputMocker(sm1);
    std::thread t(&SerialOutputer::run, &ao0InputMocker);
    return t;
}

void SessionControls::run() {
    // --------------------------------------------------
    /*TaskHandle ao0InputMocker_TaskHandle = NULL;
    DAQmxCreateTask("inputMocker", &ao0InputMocker_TaskHandle);
    DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    int mockerDelay = 100;
    int mockerDuration = 50;
    SimpleOutputer* sm1 = new SimpleOutputer(ao0InputMocker_TaskHandle, mockerDuration, mockerDelay);
    SerialOutputer ao0InputMocker(sm1);
    std::thread t1(&SerialOutputer::run, &ao0InputMocker);*/
    // --------------------------------------------------
    std::thread t1 = serialOutputMock();

    SessionConf conf(CONFIGURATION_FILE_PATH);
    if (!conf.isValid()) {
        MessageBox::Show(CONFIGURATION_FILE_ERROR_MESSAGE);
        this->finishSession();
    }

    TaskHandle inputTaskHandle = conf.getInputTaskHandle();
    std::vector<Event*> inputEvents = conf.getInputEvents();

    int inputPortsSize = conf.getInputEvents().size();
    const int numSamplesPerPort = SAMPLE_PER_PORT;
    std::vector<float64> data(inputPortsSize * numSamplesPerPort);
    int32 read;
    while (this->_isRunning) {
        if (!this->_isPaused) {
            DAQmxReadAnalogF64(inputTaskHandle, numSamplesPerPort, 5.0, DAQmx_Val_GroupByScanNumber, data.data(), inputPortsSize * numSamplesPerPort, &read, NULL);
            for (int portIndex = 0; portIndex < inputPortsSize; ++portIndex) {
                for (int sampleIndex = 0; sampleIndex < numSamplesPerPort; ++sampleIndex) {
                    float64 sampleValue = data[portIndex * numSamplesPerPort + sampleIndex];
                    std::thread t(&Event::set, inputEvents[portIndex], sampleValue);
                    t.detach();
                }
            }
        }
        else {
            std::this_thread::sleep_for(std::chrono::milliseconds(300));
        }
    }
    t1.join();
}

void SessionControls::startSession() {
    if (this->_isRunning) return;
    this->_isRunning = true;
    this->_isPaused = false;
    this->_runThread = std::thread(&SessionControls::run, this);
}

void SessionControls::pauseSession() {
    this->_isPaused = true;
}

void SessionControls::resumeSession() {
    this->_isPaused = false;
}

void SessionControls::finishSession() {
    if (!this->_isRunning) return;
    this->_isPaused = true;
    this->_isRunning = false;
    this->_runThread.join();
}

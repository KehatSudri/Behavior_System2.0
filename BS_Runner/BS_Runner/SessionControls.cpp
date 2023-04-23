#include "SessionControls.h"
#include "SessionConf.h"
#include "Consts.h"
#include "IOEvents.h"
#include <iostream>
#include <thread>

using namespace System;
using namespace System::Windows::Forms;

SessionControls::SessionControls() {
    this->isRunning_ = false;
    this->isPaused_ = false;
}

void SessionControls::run() {
    SessionConf conf("temp_path");

    TaskHandle ao0InputMocker_TaskHandle = NULL;
    DAQmxCreateTask("inputMocker", &ao0InputMocker_TaskHandle);
    DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    int mockerDelay = 0;
    int mockerDuration = 50;
    int mockerfrequency = 100;
    SimpleOutputer ao0InputMocker(ao0InputMocker_TaskHandle, mockerDelay, mockerDuration, mockerfrequency);
    std::thread t1(&SimpleOutputer::run, &ao0InputMocker);

    const int size = 5;
    float64 data[size];
    int32 read;

    TaskHandle AI_TaskHandle = NULL;
    TaskHandle AO_TaskHandle = NULL;
    DAQmxCreateTask("mainReader", &AI_TaskHandle);
    DAQmxCreateTask("mainOuputer", &AO_TaskHandle);

    std::string ai_ports_s = conf.getInputPorts(AI_PORTS);
    const char* ai_ports = ai_ports_s.c_str();

    DAQmxCreateAIVoltageChan(AI_TaskHandle, ai_ports, "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
    DAQmxCreateAOVoltageChan(AO_TaskHandle, "Dev1/ao1", "", -5.0, 5.0, DAQmx_Val_Volts, "");

    ContingentOutputer* lis = new ContingentOutputer(AO_TaskHandle, 5, 30);
    Event eve;
    eve.attachListener(lis);

    while (this->isRunning_) {
        if (!this->isPaused_) {
            DAQmxReadAnalogF64(AI_TaskHandle, size, 5.0, DAQmx_Val_GroupByScanNumber, data, size, &read, NULL);
            std::thread t(&Event::update, &eve, data[0]);
            t.detach();
        }
        else {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }

    t1.join();
    DAQmxClearTask(AI_TaskHandle);
    DAQmxClearTask(AO_TaskHandle);
    DAQmxClearTask(ao0InputMocker_TaskHandle);
}

void SessionControls::startSession() {
    if (this->isRunning_) {
        return;
    }
    this->isRunning_ = true;
    this->isPaused_ = false;
    this->t_ = std::thread(&SessionControls::run, this);
}

void SessionControls::pauseSession() {
    this->isPaused_ = true;
}

void SessionControls::resumeSession() {
    this->isPaused_ = false;
}

void SessionControls::finishSession() {
    if (!this->isRunning_) {
        return;
    }
    this->isPaused_ = true;
    this->isRunning_ = false;
    this->t_.join();
}
#include "SessionControls.h"
#include "SessionConf.h"
#include "Consts.h"
#include "IOEvents.h"
#include <iostream>
#include <thread>
#include <sstream>
#include <fstream>
#include <filesystem>

using namespace System;
using namespace std;
using namespace System::Windows::Forms;

SessionControls::SessionControls() {
    this->isRunning_ = false;
    this->isPaused_ = false;
}

void SessionControls::demoRun() {
    SessionConf conf("temp_path");

    TaskHandle ao0InputMocker_TaskHandle = NULL;
    DAQmxCreateTask("inputMocker", &ao0InputMocker_TaskHandle);
    DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    int mockerDelay = 100;
    int mockerDuration = 50;
    SimpleOutputer* sm1 = new SimpleOutputer(ao0InputMocker_TaskHandle, mockerDuration, mockerDelay);
    SerialOutputer ao0InputMocker(sm1);
    std::thread t1(&SerialOutputer::run, &ao0InputMocker);

    const int size = 5;
    float64 data[size];
    int32 read;

    TaskHandle AI_TaskHandle = NULL;
    TaskHandle* AO_TaskHandle = new TaskHandle();

    DAQmxCreateTask("mainReader", &AI_TaskHandle);
    DAQmxCreateTask("mainOuputer", AO_TaskHandle);

    DAQmxCreateAIVoltageChan(AI_TaskHandle, "Dev1/ai11", "", DAQmx_Val_Cfg_Default, -5.0, 5.0, DAQmx_Val_Volts, NULL);
    DAQmxCreateAOVoltageChan(*AO_TaskHandle, "Dev1/ao1", "", -5.0, 5.0, DAQmx_Val_Volts, "");

    SimpleOutputer* sm2 = new SimpleOutputer(*AO_TaskHandle, 30,10);
    ContingentOutputer* lis = new ContingentOutputer(sm2);
    Event eve("temp");
    eve.attachListener(lis);

    while (this->isRunning_) {
        if (!this->isPaused_) {
            DAQmxReadAnalogF64(AI_TaskHandle, size, 5.0, DAQmx_Val_GroupByScanNumber, data, size, &read, NULL);
            std::thread t(&Event::set, &eve, data[0]);
            t.detach();
        }
        else
            std::this_thread::sleep_for(std::chrono::milliseconds(300));
    }

    t1.join();
    DAQmxClearTask(AI_TaskHandle);
    DAQmxClearTask(AO_TaskHandle);
    DAQmxClearTask(ao0InputMocker_TaskHandle);
}

void SessionControls::run() {
    //SessionConf conf("session_config.txt");
    //TaskHandle ao0InputMocker_TaskHandle = NULL;
    //DAQmxCreateTask("inputMocker", &ao0InputMocker_TaskHandle);
    //DAQmxCreateAOVoltageChan(ao0InputMocker_TaskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");
    //int mockerDelay = 100;
    //int mockerDuration = 50;
    //SimpleOutputer* sm1 = new SimpleOutputer(ao0InputMocker_TaskHandle, mockerDuration, mockerDelay);
    //SerialOutputer ao0InputMocker(sm1);
    //std::thread t1(&SerialOutputer::run, &ao0InputMocker);

    //const int size = 5;
    //float64 data[size];
    //int32 read;

    //TaskHandle inputTaskHandle = conf.getInputTaskHandle();
    //std::vector<TaskHandle> tasks = conf.getAnalogOutputTasks();
    //std::cout << tasks.size();
    ////SimpleOutputer* sm2 = new SimpleOutputer(tasks[0], 30, 10);
    ////ContingentOutputer* lis = new ContingentOutputer(sm2);

    ////std::vector<Event> inputEvents = conf.getInputEvents();
    ////inputEvents[0].attachListener(lis);

    //while (this->isRunning_) {
    //    if (!this->isPaused_) {
    //        /*DAQmxReadAnalogF64(inputTaskHandle, size, 5.0, DAQmx_Val_GroupByScanNumber, data, size, &read, NULL);
    //        std::thread t(&Event::set, &inputEvents[0], data[0]);
    //        t.detach();*/
    //    }
    //    else
    //        std::this_thread::sleep_for(std::chrono::milliseconds(300));
    //}

    //t1.join();
    //for (auto t : tasks) {
    //    DAQmxClearTask(t);

    //}
    //DAQmxClearTask(inputTaskHandle);
    //DAQmxClearTask(ao0InputMocker_TaskHandle);
}

void SessionControls::startSession() {
    if (this->isRunning_)
        return;
    this->isRunning_ = true;
    this->isPaused_ = false;
    this->t_ = std::thread(&SessionControls:: demoRun, this);
}

void SessionControls::pauseSession() {
    this->isPaused_ = true;
}

void SessionControls::resumeSession() {
    this->isPaused_ = false;
}

void SessionControls::finishSession() {
    if (!this->isRunning_)
        return;
    this->isPaused_ = true;
    this->isRunning_ = false;
    this->t_.join();
}

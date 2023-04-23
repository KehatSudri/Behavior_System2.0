#include "SessionControlPannel.h"
#include <NIDAQmx.h>

using namespace System;
using namespace System::Windows::Forms;

void writerMock() {
    TaskHandle taskHandle = NULL;

    // Create the task
    DAQmxCreateTask("Writer", &taskHandle);

    // Create the analog output voltage channel
    DAQmxCreateAOVoltageChan(taskHandle, "Dev1/ao0", "", -5.0, 5.0, DAQmx_Val_Volts, "");

    // Start the task
    DAQmxStartTask(taskHandle);
    const int timer_duration_ms = 50;
    while (true)
    {
        DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 4.0, NULL);
        auto start_time = std::chrono::high_resolution_clock::now();
        while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < timer_duration_ms) {
            continue;
        }
        DAQmxWriteAnalogScalarF64(taskHandle, true, 5.0, 0.0, NULL);
        start_time = std::chrono::high_resolution_clock::now();
        while (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start_time).count() < timer_duration_ms) {
            continue;
        }
    }
}

void main() {
    //std::thread wMocker(writerMock);
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	BSRunner::SessionControlPannel form;
	Application::Run(% form);
    //wMocker.join();
}

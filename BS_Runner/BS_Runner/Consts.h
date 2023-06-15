#pragma once
#ifndef __Consts__
#define __Consts__
#define AI_PORTS 1
#define AO_PORTS 2
#define DI_PORTS 3
#define DO_PORTS 4

#define MOCK1 'Dev1/ao0'
#define MOCK2 'Dev1/ao1'
#define MOCK3 'Dev1/do0'
#define MOCK4 'Dev1/do1'

#define ANALOG_OUTPUT "ao"
#define ANALOG_INPUT "ai"
#define DIGITAL_OUTPUT "port0"

#define OUTPUT_INDICATOR 1
#define INPUT_INDICATOR 2
#define TRIAL_END_CONDITION_INDICATOR 3
#define TRIAL_TIMEOUT_INDICATOR 4
#define TRIAL_START 5

#define DELAY_PARAM "delay"
#define DURATION_PARAM "duration"
#define FREQUENCY_PARAM "frequency"
#define AMPLITUDE_PARAM "amplitude"

#define TRIAL_TIMEOUT "trial_timeout"
#define TRIAL_END_CONDITION "trial_end_condition"

#define END_OF_SESSION 0
#define CONTINUE_SESSION 1
#define ERROR -1

#define MAX_WATTAGE 5.0
#define MIN_WATTAGE -5.0

#define TRUE "True"

#define NEW_LINE_CATEGORY '$'

#define SAMPLE_PER_PORT 5
#define CONFIGURATION_FILE_ERROR_MESSAGE "Failed to load session configuration file"
#endif // __Consts__

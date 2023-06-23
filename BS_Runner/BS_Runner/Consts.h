#pragma once
#ifndef __Consts__
#define __Consts__
#define AI_PORTS 1
#define AO_PORTS 2
#define DI_PORTS 3
#define DO_PORTS 4

#define TONE "Tone"

#define ANALOG_OUTPUT "ao"
#define ANALOG_INPUT "ai"
#define DIGITAL_OUTPUT "port0"

#define OUTPUT_START_INDICATOR 1
#define OUTPUT_FINISH_INDICATOR 2
#define INPUT_START_INDICATOR 3
#define INPUT_FINISH_INDICATOR 4
#define TRIAL_END_CONDITION_INDICATOR 5
#define TRIAL_TIMEOUT_INDICATOR 6
#define SESSION_TIMEOUT_INDICATOR 7
#define TRIAL_START_INDICATOR 8
#define TRIAL_END_INDICATOR 9
#define SESSION_END_INDICATOR 10
#define REWARD_INDICATOR 11

#define DELAY_PARAM "delay"
#define MIN_DELAY_PARAM "min_delay"
#define MAX_DELAY_PARAM "max_delay"
#define IS_RANDOM_PARAM "is_random"
#define IS_REWARD_PARAM "is_reward"
#define DURATION_PARAM "duration"
#define FREQUENCY_PARAM "frequency"
#define AMPLITUDE_PARAM "amplitude"

#define TRIAL_TIMEOUT "trial_timeout"
#define TRIAL_END_CONDITION "trial_end_condition"

#define NEW_TRIAL_CASE 0
#define NEW_INPUT_CASE 1
#define NEW_OUTPUT_CASE 2

#define END_OF_SESSION 0
#define CONTINUE_SESSION 1
#define INIT_ERROR -1

#define MAX_WATTAGE 5.0
#define MIN_WATTAGE -5.0

#define NEW_LINE_CATEGORY '$'
#define NONE "None"

#define SAMPLE_PER_PORT 5
#define CONFIGURATION_FILE_ERROR_MESSAGE "Failed to load session configuration file"

#define SAMPLE_RATE 44100
#define TWO_PI 6.2831853071795

#endif // __Consts__
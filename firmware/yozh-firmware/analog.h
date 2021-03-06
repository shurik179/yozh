#ifndef _YOZH_ANALOG_H
#define _YOZH_ANALOG_H
#include <Arduino.h>
#include "wiring_private.h"
#define NUM_ANALOGS 8
void setupAnalogPins();
void enableLineArray();
void disableLineArray();
void updateVsense();
void updateLineArray();
void printAnalogs();
uint16_t myAnalogRead(uint8_t pin);

#endif

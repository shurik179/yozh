// SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
// SPDX-License-Identifier: MIT
#ifndef _YOZH_ANALOG_H
#define _YOZH_ANALOG_H
#include <Arduino.h>
#include "wiring_private.h"
#define NUM_ANALOGS 7
void setupAnalogPins();
void enableLineArray();
void disableLineArray();
void updateLineArray();
void printAnalogs();
uint16_t myAnalogRead(uint8_t pin);

#endif

#include "analog.h"
#include "regmap.h"

uint8_t PINS_ANALOG[]={PIN_A0,PIN_A1,PIN_A2,PIN_A3,PIN_A4,PIN_A5,PIN_A6};


void setupAnalogPins() {
    // put your setup code here, to run once:
    for (uint8_t i=0;i<NUM_ANALOGS; i++) {
        pinPeripheral(PINS_ANALOG[i], PIO_ANALOG);
    }
    pinMode(PIN_ANALOG_CTRL, OUTPUT);
    digitalWrite(PIN_ANALOG_CTRL, LOW); //disables line array
}


void enableLineArray(){
    digitalWrite(PIN_ANALOG_CTRL, HIGH);
}

void disableLineArray(){
    digitalWrite(PIN_ANALOG_CTRL, LOW);
}



void updateLineArray(){
    for (uint8_t i=0; i<NUM_ANALOGS; i++) {
        linearrayRaw[i]=myAnalogRead(PINS_ANALOG[i]); 
    }
}

void printAnalogs(){
    Serial.print("Analogs: ");
    for (uint8_t i=0; i<NUM_ANALOGS; i++) {
        //analog input active
        Serial.print(i); Serial.print(": "); Serial.print(linearrayRaw[i]);Serial.print("    ");
    }
    Serial.println(" ");
}

uint16_t myAnalogRead(uint8_t pin){
  uint32_t valueRead;
  while (ADC->STATUS.bit.SYNCBUSY == 1);
  //configure input channel
  ADC->INPUTCTRL.bit.MUXPOS = g_APinDescription[pin].ulADCChannelNumber; // Selection for the positive ADC input
  while (ADC->STATUS.bit.SYNCBUSY == 1);
  //enable ADC
  ADC->CTRLA.bit.ENABLE = 0x01;
  while (ADC->STATUS.bit.SYNCBUSY == 1);
  // Start conversion
  ADC->SWTRIG.bit.START = 1;
  while (ADC->INTFLAG.bit.RESRDY == 0);   // Waiting for conversion to complete
  // Store the value
  valueRead = ADC->RESULT.reg;
  while (ADC->STATUS.bit.SYNCBUSY == 1);
  ADC->CTRLA.bit.ENABLE = 0x00;             // Disable ADC
  while (ADC->STATUS.bit.SYNCBUSY == 1);

  return valueRead;
}

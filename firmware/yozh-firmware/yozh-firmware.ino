// SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
// SPDX-License-Identifier: MIT

//#include "wiring_private.h"
//registers
#include "regmap.h"
#include "i2c.h"
//code for motors, encoders, and servos
#include "motors.h"
#include "analog.h"
#include "IMU.h"

#define FW_VERSION_MAJOR 4
#define FW_VERSION_MINOR 02

//uncomment to allow debugging print to Serial.
//#define DEBUG_PRINT

uint32_t loopCount=0;
uint32_t lastBlink=0;
bool heartbeat = 0;

void setup(){
    i2cMasterBegin(100000); //start I2C bus on Wire1 as master, in regular mode (100 kHz)
    i2cSlaveBegin();        //start i2c bus on Wire, as a slave
    initRegmap();
    *whoAmI=0x11;
    fwVersion[0]=FW_VERSION_MINOR;
    fwVersion[1]=FW_VERSION_MAJOR;
#ifdef DEBUG_PRINT
        Serial.begin(9600);
        /*while(!Serial){
          delay(10);
        }*/
        delay(2000);
        Serial.println("Yozh firmware started");
        delay(1000);
#endif
    for (int i=0; i<2; i++){
        servoPosition[i] = 0;
    }
    *motorMode = MOTOR_MODE_POWER;
    setupTimers();
    setupMotorPins();
    setServos();//FIXME
    *linearrayConfig = 0;
    pinMode(PIN_HEARTBEAT, OUTPUT);
    digitalWrite(PIN_HEARTBEAT, LOW);
    * imuConfig = 1;
    IMUbegin();
    Serial.println("Setup ends");
}

void loop(){
    loopCount++;
    //blink LED
    uint32_t now = millis();
    if (now-lastBlink>250) {
        lastBlink = now;
        heartbeat = ! heartbeat;
        digitalWrite(PIN_HEARTBEAT, heartbeat);
    }
    //First, update configuration/motors/servos
    if (isSet(FLAG_MOTOR_CONFIG)){
        clearFlag(FLAG_MOTOR_CONFIG);
        #ifdef DEBUG_PRINT
            Serial.println("Updating motor configuration");
        #endif
        //FIXME - need to restart all PID controllers
    }
    if (isSet(FLAG_SERVO)){
        clearFlag(FLAG_SERVO);//unset the servo flag bit
        #ifdef DEBUG_PRINT
        Serial.print("setting servo to new positions: ");
        Serial.print(servoPosition[0]); Serial.println(" ");
        Serial.print(servoPosition[1]); Serial.println(" ");
        #endif
        setServos();
    }
    if (isSet(FLAG_ENC_RESET)) {
        clearFlag(FLAG_ENC_RESET);
        #ifdef DEBUG_PRINT
        Serial.println("Resetting encoder(s)");
        #endif
        resetEncoders();
    }
    if (isSet(FLAG_MOTOR_MODE)||isSet(FLAG_MOTOR_POWER)){
        clearFlag(FLAG_MOTOR_MODE);
        clearFlag(FLAG_MOTOR_POWER);
        #ifdef DEBUG_PRINT
            Serial.println("Updating motor mode/power  configuration");
            Serial.print("Motor mode: "); Serial.print(*motorMode);
            Serial.print(" powerL: "); Serial.print(motorPower[0]);
            Serial.print(" powerR: "); Serial.println(motorPower[1]);
        #endif
        setMotors();
    }
    if (isSet(FLAG_LINEARRAY_CONFIG)){
        clearFlag(FLAG_LINEARRAY_CONFIG);
        if (*linearrayConfig) {
            enableLineArray();
        } else {
            disableLineArray();
        }
    }

    if (isSet(FLAG_IMU_CONFIG)){
        clearFlag(FLAG_IMU_CONFIG);
        #ifdef DEBUG_PRINT
        Serial.println("Configuring IMU");
        #endif
        switch (*imuConfig){
            case IMU_CONFIG_END: //stop
                *imuStatus = IMU_OFF;
                break;
            case IMU_CONFIG_BEGIN://begin
                *imuStatus = IMU_OK; //FIXME
                //Serial.println("starting IMU");
                IMUbegin();
                //Serial.println("IMU Started");
                break;
            case IMU_CONFIG_CALIBRATE: //calibrate
                IMUcalibrate();
                break;
        }
    }

    //now, update readings of sensors etc
    if (*imuConfig) {
        IMUupdate();
    }
    if (*linearrayConfig) {
        updateLineArray();
    }

    //update motor speed reading and pid speed adjustment
    //it will automatically check for elapsed  time
    updateSpeed();

}

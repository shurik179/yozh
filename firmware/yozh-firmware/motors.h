#ifndef _YOZH_MOTORS_H
#define _YOZH_MOTORS_H
#include <Arduino.h>
#include "wiring_private.h"

// Motor configuration modes
#define MOTOR_MODE_POWER 0  // motors controlled individually
#define MOTOR_MODE_DRIVE 1  // tank drive - direction determined by IMU 
// Normally, motor power is an int between -500...500
// this special value indicates that the motor should be stopped in coast state
#define POWER_COAST 1000
#define MOTOR_MAX_POWER 500


extern volatile int32_t encoderTimestamp[];     // time of last encoder update, in micros
extern int32_t prevEncoderTimestamp[]; // time of previous encoder update, in micros
extern int32_t prevEncoder[];//to hold previous values of encoders - for computing speed
//extern volatile int8_t   motorDirection[];
extern uint32_t lastUpdate;         //time of last update of motor speeds, in usec

/*
 * Configures clock sources and others for timers TCC0 (used by motors),
 * TCC1 and TCC2 (used by servos)
 */
void setupTimers();
/*
 * Correctly sets pin mode and peripherals for  motors, encoders, and servos pins
 */
void setupMotorPins();
//updates motors mode,  PID coefficients and target if they have been changed
//void updateMotorsConfig();
//resets motor encoders as needed
void resetEncoders();
//computes what power to give to motors, using PID if so instructed,
//and actually sets motors to this power
void setMotors();
/* Sets power for motors. Range is -500..500 */
void setMotorsPower(int16_t power1, int16_t power2);
//update motor speeds
void updateSpeed();
/* Sets servo positions. Position should be a pointer to an array
 * of four numbers, representing pulsewidths  for 4 servos
 */
void setServos();
/* Interrupt service routines for encoders */
void ISR_enc1_speed();
void ISR_enc2_speed();
#endif //for ifndef _YOZH_MOTORS_H

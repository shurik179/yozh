#ifndef _YOZH_REGMAP_H
#define _YOZH_REGMAP_H
#include <Arduino.h>
#define REG_SIZE32 30 //size of register bank, in 4-byte (32 bit) units
#define RW_REGISTERS 40 //number of RW registers (in bytes)
//this will be defined in regmap.cpp
extern  volatile byte * REGBANK;

/* **********************************************************************
 *  Register definitions
 *  All multibyte registers  use little-endian byte order: thus, if
 * a uint16_t value is stored in registers N, N+1,
 * then register N is low byte, and register N+1 is high byte
 * so the full value is
 * (REGBANK[N+1]<<8)|REGBANK[N]
 * This allows directly addressing them as multibyte variables, e.g.
 * uint16_t * value =(uint16_t *) &REGBANK[N]; //pointer to variable
 * *value=25;
 * Yes, it is a bit hacky
 * *********************************************************************
 */
//R/W registers
#define REG_MAX_SPEED           0
#define REG_PID_KP              2
#define REG_PID_TI              4
#define REG_PID_TD              6
#define REG_PID_ILIM            8
#define REG_MOTOR_CONFIG        10
#define REG_MOTOR_MODE          11
#define REG_POWER_L             12
#define REG_POWER_R             14
#define REG_DRIVE_DISTANCE      16
#define REG_TURN_ANGLE          20
#define REG_DRIVE_SPEED         22
#define REG_ENC_RESET           24
#define REG_IMU_INIT            25
#define REG_NEOPIXEL_L          26
#define REG_NEOPIXEL_R          29
#define REG_NEOPIXEL_BRIGHTNESS 32
#define REG_LINEARRAY_INIT      33
#define REG_SERVO1              34
#define REG_SERVO2              36

//Read-only registers
#define REG_FW_VERSION          40
#define REG_WHO_AM_I            42
#define REG_IMU_STATUS          43
#define REG_ENCODER_L           44
#define REG_ENCODER_R           48
#define REG_SPEED_L             52
#define REG_SPEED_R             54
#define REG_LINEARRAY_RAW       56
#define REG_VSENSE              72
#define REG_ACCEL               74
#define REG_GYRO                80
#define REG_MAG                 86
#define REG_YAW                 92
#define REG_PITCH               94
#define REG_ROLL                96
#define REG_QUAT                100
#define REG_DRIVE_STATUS        116



/* **********************************************************************
 *  pointer/aliases - for direct access to registers. These are forward declarations,
 * the definitions are in regmap.cpp
 * *********************************************************************
 */


extern volatile uint16_t * motorMaxspeed;
extern volatile uint16_t * motorKp;
extern volatile uint16_t * motorTi;
extern volatile uint16_t * motorTd;
extern volatile uint16_t * motorIlim;
extern volatile byte     * motorConfig;
extern volatile uint8_t  * motorMode;
extern volatile byte     * encoderReset;
extern volatile int16_t  * motorPower; //2-element array
extern volatile int32_t  * driveDistance;
extern volatile int16_t  * turnAngle; //FIXME: headign vs angle
extern volatile uint16_t * driveSpeed;
extern volatile uint8_t  * imuConfig;
extern volatile uint8_t  * neopixelColors; //6-element array: 3 colors for each of 2 neopixels
extern volatile uint8_t  * neopixelBrightness;
extern volatile uint8_t  * linearrayConfig;
extern volatile uint16_t * servoPosition; //2-element array




/* *********************************************
 *  Read-only registers
 * *********************************************
 */


//Firmware version
extern volatile uint8_t  * fwVersion; //2-element array
extern volatile uint8_t  * whoAmI;
extern volatile uint8_t  * imuStatus;
extern volatile int32_t  * encoder; //2-element array
extern volatile int16_t  * speed;   //2-element array
extern volatile uint16_t * linearrayRaw;   //8-element array of 0..1023 values
extern volatile uint16_t * vsense; //
//acceleration data: accel[0]=x accel, accel[1]=y, accel[2]=z
//scale: LSB=1/16384 g
extern volatile int16_t *  accel;
//gyro data: gyro[0]=x rotation, gyro[1]=y, gyro[2]=z
//LSB=250.0 / 32768.0 deg/s
extern volatile int16_t * gyro;
//magentometer data: accel[0]=x accel, accel[1]=y, accel[2]=z
//scale: FIXME
extern volatile int16_t * mag;
//orientation, as a unit quaternion
//quat[0] is real part, quat[1], quat[2], quat[3] are i-, j- and k-components respectively
//scaled by 2^30
extern volatile int32_t * quat;
// yaw, pitch, roll, in units of 1/10 degree
extern volatile int16_t * yaw;
extern volatile int16_t * pitch;
extern volatile int16_t * roll;

/* **********************************************************************
 * change flags.  Whenever one of the R/W registers is written to,
 * it sets one of the bits in changeFlag, to indicate
 * to the main loop that it needs processing
 * each individual flag bitmask is given a name below.
 * *********************************************************************
 */

extern uint16_t volatile changeFlag;
//function-like macros and function  declarations
#define isSet(F) (changeFlag & (uint16_t) F)
#define setFlag(F)  changeFlag |= (uint16_t) F
#define clearFlag(F) changeFlag &=~ (uint16_t)F
// Flag definitions
#define FLAG_NONE 0x0
#define FLAG_MOTOR_CONFIG      (1ul)
#define FLAG_MOTOR_MODE        ((1ul)<<1)
#define FLAG_ENC_RESET         ((1ul)<<2)
#define FLAG_MOTOR_POWER       ((1ul)<<3)
#define FLAG_DRIVE_CONFIG      ((1ul)<<4)
#define FLAG_SERVO             ((1ul)<<5)
#define FLAG_LINEARRAY_CONFIG  ((1ul)<<6)
#define FLAG_IMU_CONFIG        ((1ul)<<7)
#define FLAG_NEOPIXEL          ((1ul)<<8)
#define FLAG_NEOPIXEL_CONFIG   ((1ul)<<9)

// array to map register offsets for R/W registers to flag bits
// instead of giving it static values, we will initialize it using a function
// initRegmap, defined in regmap.cpp

extern uint32_t registerFlag[];
void initRegmap();

#endif

#include "regmap.h"
//allocate memory for registers, aligned with 32-bit words
volatile int32_t REG32[REG_SIZE32];
//cast  as byte arrays
volatile byte * REGBANK = (byte *)REG32;
//change flag
uint16_t volatile changeFlag=0;

// array to map register offsets (for REGB) to flag bits
// instead of giving it static values, we will initialize it using a function
// initRegmap
uint32_t registerFlag[RW_REGISTERS];
// *******************
void initRegmap(){
    int i;
    //first, initialize everything to zero
    for (i=0; i<RW_REGISTERS; i++)  registerFlag[i] = FLAG_NONE;
    //initialize registerFlag array, which shows, for each register, which flag it should set
    //Note: this uses hardcoded block sizes
    for (i=0; i<11; i++)  registerFlag[REG_MAX_SPEED+i] = FLAG_MOTOR_CONFIG; //11 bytes for MOTOR_CONFIG
    for (i=0; i<3; i++)  registerFlag[REG_MOTOR_MODE+i] = FLAG_MOTOR_MODE;   // 3 bytes for MOTOR_MODE
    for (i=0; i<4; i++)  registerFlag[REG_POWER_L+i] = FLAG_MOTOR_POWER;     // 4 bytes for MOTOR_POWER
    for (i=0; i<4; i++)  registerFlag[REG_SERVO1+i] = FLAG_SERVO;            // 4 bytes fro servos
    registerFlag[REG_ENC_RESET] = FLAG_ENC_RESET;
    registerFlag[REG_IMU_INIT] = FLAG_IMU_CONFIG;
    registerFlag[REG_LINEARRAY_INIT] = FLAG_LINEARRAY_CONFIG;
}

/* **********************************************************************
 *  pointer/aliases - for direct access to registers.
 * THis way, you can access, e.g., reading of left motor encoder by simply using
 *  value=encoder[0];
 *  instead of
 *  value =   REGBANK[REG_ENCODER_L]|(REGBANK[REG_ENCODER_L+1]<<8)|(REGBANK[REG_ENCODER_L+2]<<16)|(REGBANK[REG_ENCODER_L+3]<<24);
 */


volatile uint16_t * motorMaxspeed   =(uint16_t *) &REGBANK[REG_MAX_SPEED];
volatile uint16_t * motorKp         =(uint16_t *) &REGBANK[REG_PID_KP];
volatile uint16_t * motorTi         =(uint16_t *) &REGBANK[REG_PID_TI];
volatile uint16_t * motorTd         =(uint16_t *) &REGBANK[REG_PID_TD];
volatile uint16_t * motorIlim       =(uint16_t *) &REGBANK[REG_PID_ILIM];
volatile byte     * motorConfig     = &REGBANK[REG_MOTOR_CONFIG];
volatile uint8_t  * motorMode       =(uint8_t *)  &REGBANK[REG_MOTOR_MODE];
volatile uint8_t  * motorMode       =(uint8_t *)  &REGBANK[REG_MOTOR_MODE];
volatile byte     * encoderReset    = &REGBANK[REG_ENC_RESET];
volatile int16_t  * motorPower      =(int16_t *)  &REGBANK[REG_POWER_L]; //2-element array
volatile uint16_t * servoPosition   =(uint16_t *) &REGBANK[REG_SERVO1]; //2-element array
volatile uint8_t  * imuConfig       =(uint8_t *)  &REGBANK[REG_IMU_INIT];
volatile uint8_t  * linearrayConfig =(uint8_t *)  &REGBANK[REG_LINEARRAY_INIT];

//Read-only registers

//Firmware version
volatile uint8_t * fwVersion        = (uint8_t *)&REGBANK[REG_FW_VERSION];//2-element array
//whoami
volatile uint8_t * whoAmI           = (uint8_t *)&REGBANK[REG_WHO_AM_I];
volatile uint8_t * imuStatus        = (uint8_t *)&REGBANK[REG_IMU_STATUS];

//encoders
volatile int32_t  * encoder         = (int32_t *) &REGBANK[REG_ENCODER_L]; //2-element array
volatile int16_t  * speed           = (int16_t *) &REGBANK[REG_SPEED_L]; //speed in encoder counts/s
//line array
volatile uint16_t * linearrayRaw    = (uint16_t *) &REGBANK[REG_LINEARRAY_RAW];   //7-element array
//acceleration data: accel[0]=x accel, accel[1]=y, accel[2]=z
//scale: LSB=1/16384 g
volatile int16_t * accel            = (int16_t *) &REGBANK[REG_ACCEL];   //3-element array
//gyro data: gyro[0]=x rotation, gyro[1]=y, gyro[2]=z
//LSB=250.0 / 32768.0 deg/s
volatile int16_t * gyro             = (int16_t *) &REGBANK[REG_GYRO];   //3-element array
//orientation, as a unit quaternion
//quat[0] is real part, quat[1], quat[2], quat[3] are i-, j- and k-components respectively
//scaled by 2^30
volatile int32_t * quat_converted   = (int32_t *) &REGBANK[REG_QUAT];   //4-element array

// yaw, pitch, roll, in units of 1/10 degree
volatile int16_t * yaw              = (int16_t *) &REGBANK[REG_YAW];
volatile int16_t * pitch            = (int16_t *) &REGBANK[REG_PITCH];
volatile int16_t * roll             = (int16_t *) &REGBANK[REG_ROLL];

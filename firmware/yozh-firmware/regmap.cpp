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
    for (i=0; i<11; i++)  registerFlag[REG_MAX_SPEED+i] = FLAG_MOTOR_CONFIG;
    registerFlag[REG_MOTOR_MODE] = FLAG_MOTOR_MODE;
    registerFlag[REG_ENC_RESET] = FLAG_ENC_RESET;
    for (i=0; i<4; i++)  registerFlag[REG_POWER_L+i] = FLAG_MOTOR_POWER;
    for (i=0; i<8; i++)  registerFlag[REG_DRIVE_DISTANCE+i] = FLAG_DRIVE_CONFIG; //includes distange or angle target or drive speed
    registerFlag[REG_IMU_INIT] = FLAG_IMU_CONFIG;
    for (i=0; i<6; i++)  registerFlag[REG_NEOPIXEL_L+i] = FLAG_NEOPIXEL; //Neopixel setup
    registerFlag[REG_NEOPIXEL_BRIGHTNESS] = FLAG_NEOPIXEL_CONFIG;
    registerFlag[REG_LINEARRAY_INIT] = FLAG_LINEARRAY_CONFIG;
    for (i=0; i<4; i++)  registerFlag[REG_SERVO1+i] = FLAG_SERVO;
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
volatile byte     * encoderReset    = &REGBANK[REG_ENC_RESET];
volatile int16_t  * motorPower      =(int16_t *)  &REGBANK[REG_POWER_L]; //2-element array
volatile int32_t  * driveDistance   =(int32_t *)  &REGBANK[REG_DRIVE_DISTANCE];
volatile int16_t  * turnAngle       =(int16_t *)  &REGBANK[REG_TURN_ANGLE];
volatile uint16_t * driveSpeed      =(uint16_t *) &REGBANK[REG_DRIVE_SPEED];
volatile uint8_t  * imuConfig       =(uint8_t *)  &REGBANK[REG_IMU_INIT];
volatile uint8_t  * neopixelColors  =(uint8_t *)  &REGBANK[REG_NEOPIXEL_L]; //6-element array: 3 colors for each of 2 neopixels; order is RGB
volatile uint8_t  * neopixelBrightness = (uint8_t *) &REGBANK[REG_NEOPIXEL_BRIGHTNESS];
volatile uint8_t  * linearrayConfig =(uint8_t *)  &REGBANK[REG_LINEARRAY_INIT];
volatile uint16_t * servoPosition   =(uint16_t *) &REGBANK[REG_SERVO1]; //2-element array

//Read-only registers

//Firmware version
volatile uint8_t * fwVersion        = (uint8_t *)&REGBANK[REG_FW_VERSION];//2-element array
//whoami
volatile uint8_t * whoAmI           = (uint8_t *)&REGBANK[REG_WHO_AM_I];

//encoders
volatile int32_t  * encoder         = (int32_t *) &REGBANK[REG_ENCODER_L]; //2-element array
volatile int16_t  * speed           = (int16_t *) &REGBANK[REG_SPEED_L]; //speed in encoder counts/s
volatile uint16_t * linearrayRaw    = (uint16_t *) &REGBANK[REG_LINEARRAY_RAW];   //8-element array
volatile uint16_t * vsense          = (uint16_t *) &REGBANK[REG_VSENSE];
//acceleration data: accel[0]=x accel, accel[1]=y, accel[2]=z
//scale: LSB=1/16384 g
volatile int16_t * accel            = (int16_t *) &REGBANK[REG_ACCEL];   //3-element array
//gyro data: gyro[0]=x rotation, gyro[1]=y, gyro[2]=z
//LSB=250.0 / 32768.0 deg/s
volatile int16_t * gyro             = (int16_t *) &REGBANK[REG_GYRO];   //3-element array
//magentometer data: accel[0]=x accel, accel[1]=y, accel[2]=z
//scale: FIXME
volatile int16_t * mag              = (int16_t *) &REGBANK[REG_MAG];   //3-element array
//orientation, as a unit quaternion
//quat[0] is real part, quat[1], quat[2], quat[3] are i-, j- and k-components respectively
//scaled by 2^30
volatile int32_t * quat             = (int32_t *) &REGBANK[REG_QUAT];   //3-element array

// yaw, pitch, roll, in units of 1/10 degree
volatile int16_t * yaw              = (int16_t *) &REGBANK[REG_YAW];   //3-element array
volatile int16_t * pitch            = (int16_t *) &REGBANK[REG_PITCH];   //3-element array
volatile int16_t * roll             = (int16_t *) &REGBANK[REG_ROLL];   //3-element array
volatile uint8_t * regDriveStatus   = (uint8_t *) &REGBANK[REG_DRIVE_STATUS];

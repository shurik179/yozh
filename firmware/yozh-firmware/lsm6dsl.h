#ifndef _YOZH_IMU_H
#define _YOZH_IMU_H
#include "Arduino.h"
#include <FlashStorage.h>
#include "regmap.h"
#define LSM6DSL_ADDRESS    0x6A   // Address of LSM6DSL accel/gyro when ADO = LOW
#define LSM6DSL_WHO_AM_I   0x6A   // Value of WHO_AM_I register 

//offsets data
//flash storage stuff
typedef struct {
  boolean valid;
  int16_t gyro[3];
  int16_t accel[3];
} offsets_t;




//statuses
#define IMU_OFF 0x00
#define IMU_OK  0x01
#define IMU_CALIBRATING 0x02
#define IMU_ERROR 0x04
//configuration mode used in communication with SAMD21
#define IMU_CONFIG_BEGIN 0x01
#define IMU_CONFIG_CALIBRATE 0x02
#define IMU_CONFIG_END 0x00



// Set initial parameters
/* value to write to CTRL2_G register for setting gyro parameters
   This will set ODR to 833hz and  gyro full scale to 500 dps
*/
#define GYRO_CTRL2_INIT 0b01110100
/* value to write to CTRL6_C register for setting gyro parameters
   This will set high-performance mode and  activate low-pass filter with  bandwidth of 237 Hz
*/
#define GYRO_CTRL6_INIT 0b00000001



/* value to write to CTRL1_XL register for setting accelerometer parameters
   This will set ODR to 833hz and  accel full scale to 2 g
   We do not change the default low-pass/high-pass filter settings for the
   accelerometer
*/
#define ACCEL_CTRL1_INIT 0b01110000

/*Registers
  This is not a full list but only those we need.
  All 2-byte registers go in (low_byte, high_byte) order.
  E.g. 0x20 is low byte of temperature, and 0x21 is high byte
*/
// For testing connections. Always holds value of 0x6A
#define LSM6DSL_REG_WHO_AM_I      0x0F
// Status, aka data ready register. Bit 0 is accel data, bit 1 is gyro data,
// and bit 2 is temp data. If new data is available, corresp. bit is set to 1
#define LSM6DSL_REG_STATUS        0x1E
#define LSM6DSL_REG_CTRL1_XL      0x10
#define LSM6DSL_REG_CTRL2_G       0x11
#define LSM6DSL_REG_CTRL6_C       0x15
// Temperature (two bytes)
#define LSM6DSL_REG_OUT_TEMP      0x20
// Gyro (6 bytes:  Xlow, Xhigh, Ylow, Yhigh, Zlow, Zhigh)
#define LSM6DSL_REG_OUT_G         0x22
// Accel (6 bytes:  Xlow, Xhigh, Ylow, Yhigh, Zlow, Zhigh)
#define LSM6DSL_REG_OUT_XL        0x28



const float aRes = 1.0f/16384.0f;    //accel resolution, in g/LSB
const int16_t G = 16384;           // g in units of accelerometer raw data =1/aRes
const float gRes = 500.0f / 32768.0f; //gyro resolution, in (deg/s)/LSB
const float gResRad = gRes * PI/180.0f; //gyro resolution, in (rad/s)/LSB


const float radToDeg=180.0f/PI;      //converstion factor from radians to degrees s
const float GyroMeasError = PI * (40.0f / 180.0f);     // gyroscope measurement error in rads/s (start at 60 deg/s), then reduce after ~10 s to 3
const float beta = sqrtf(3.0f / 4.0f) * GyroMeasError;  // compute beta
const float GyroMeasDrift = PI * (2.0f / 180.0f);      // gyroscope measurement drift in rad/s/s (start at 0.0 deg/s/s)
const float zeta = sqrtf(3.0f / 4.0f) * GyroMeasDrift;  // compute zeta, the other free parameter in the Madgwick scheme usually set to a small or zero value





//checks if IMU is available
//assumes Wire1 has already been started
bool IMUisAvailable();
// starts  IMU
// returns 1 on success, 0 on failure
bool IMUbegin();
void IMUcalibrate();
void readAccelData();
void readGyroData();

//need to be called regularly - as frequently as possible - to update the orientation;
//saves accel, gyro, and orientation to regmap
void IMUupdate();
// Define output variables from updated quaternion---these are Tait-Bryan angles, commonly used in aircraft orientation.
// In this coordinate system, the positive z-axis is down toward Earth.
// Yaw is the angle between Sensor x-axis and Earth magnetic North (or true North if corrected for local declination, looking down on the sensor positive yaw is counterclockwise.
// Pitch is angle between sensor x-axis and Earth ground plane, toward the Earth is positive, up toward the sky is negative.
// Roll is angle between sensor y-axis and Earth ground plane, y-axis up is positive roll.
// These arise from the definition of the homogeneous rotation matrix constructed from quaternions.
// Tait-Bryan angles as well as Euler angles are non-commutative; that is, the get the correct orientation the rotations must be
// applied in the correct order which for this configuration is yaw, pitch, and then roll.
// For more see http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles which has additional links.
float getYaw();
float getPitch();
float getRoll();
//print IMU readings to serial monitor, for debugging
void IMUprint();

void _MadgwickQuaternionUpdate(float deltat);

#endif

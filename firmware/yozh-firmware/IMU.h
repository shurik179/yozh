#ifndef _YOZH_IMU_H
#define _YOZH_IMU_H
#include "Arduino.h"
#include <FlashStorage.h>
#include "regmap.h"

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




//The follwoing constants assume setting gyro scale of 500DPS and accelerometere scael of 2G

const float aRes = 1.0f/16384.0f;    //accel resolution, in g/LSB
const int16_t G = 16384;           // g in units of accelerometer raw data =1/aRes
const float gRes = 500.0f / 32768.0f; //gyro resolution, in (deg/s)/LSB
const float gResRad = gRes * PI/180.0f; //gyro resolution, in (rad/s)/LSB


const float radToDeg=57.29578;      //converstion factor from radians to degrees s
const float GyroMeasError = PI * (40.0f / 180.0f);     // gyroscope measurement error in rads/s (start at 60 deg/s), then reduce after ~10 s to 3
const float beta = sqrtf(3.0f / 4.0f) * GyroMeasError;  // compute beta
//const float GyroMeasDrift = PI * (2.0f / 180.0f);      // gyroscope measurement drift in rad/s/s (start at 0.0 deg/s/s)
const float GyroMeasDrift = PI * (0.0f / 180.0f);      // gyroscope measurement drift in rad/s/s (start at 0.0 deg/s/s)
const float zeta = sqrtf(3.0f / 4.0f) * GyroMeasDrift;  // compute zeta, the other free parameter in the Madgwick scheme usually set to a small or zero value





//checks if IMU is available
//assumes Wire1 has already been started
bool IMUisAvailable();
// starts  IMU
// returns 1 on success, 0 on failure
bool IMUbegin();
void IMUcalibrate();
void readData();

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

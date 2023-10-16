Inertial Motion Unit
====================

The top plate also contains an inertial motion unit (IMU):
`LSM6DSL <https://www.st.com/en/mems-and-sensors/lsm6dsl.html>`__ by
ST Microelectronics. This chip contains an accelerometer and a gyroscope,
allowing the user to measure acceleration and rotation velocity. In addition
to  raw readings, the secondary MCU also runs a sensor fusion algorithm which
uses the accelerometer and gyro data to constantly compute robot orientation
in space, giving yaw, pitch, and roll angles. This can be used for precise
navigation.   

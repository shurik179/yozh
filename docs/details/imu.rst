Inertial Motion Unit
====================

The robot also contains an inertial motion unit (IMU):
`ICM 42688 <https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42688-p/>`__ by
Invensense. This chip contains an accelerometer and a gyroscope,
allowing the user to measure acceleration and rotation velocity. In addition
to  raw readings, the secondary MCU also runs a sensor fusion algorithm which
uses the accelerometer and gyro data to constantly compute robot orientation
in space, giving yaw, pitch, and roll angles. This can be used for precise
navigation.   



.. _imu:

Inertial Motion Unit
====================

This section describes the functions for using the built-in Inertial Motion
Unit (IMU).

Yozh contains a built-in Inertial Motion Unit (IMU), which is based on
LSM6DSL chip from ST Microelectronics. This chip combines a 3-axis accelerometer and a
3-axis gyro sensor, which provide information about acceleration and rotational
speed. The sensor is placed on the back side of the top plate.
Yozh firmware combines the sensor data to provide information
about robot's orientation in space, in the form of Yaw, Pitch, and Roll angles.
(Yozh firmware is based on the work of
`Kris Winer <https://github.com/kriswiner>`__ and uses data fusion
algorithm invented by Sebastian Madgwick.)

Below is the description of functions related to IMU. You can also  check sample
code in :guilabel:`imu_test` example sketch included with Yozh CircuitPython library.



Initialization
--------------

By default, the IMU is inactive. To start/stop  it, use the functions below.

.. function:: void  IMU_start()

   Activate IMU


.. function:: void IMU_stop()

   Stop the IMU


.. function::  bool IMU_status()

   Returns IMU status. This function can be used to verify that IMU
   activation was successful. Possible values are:

   * 0: IMU is inactive
   * 1: IMU is active
   * 2: IMU is currently in the process of calibration



Calibration
-----------

Before use, the IMU needs to be calibrated. The calibration process determines
and then applies corrections (offsets)  to the raw data; without these
corrections, the  data returned by the sensor is very inaccurate.

If you haven't  calibrated the sensor before (or want to recalibrate it),
use the following function:

.. function:: void IMU_calibrate()

       This function will determine and
       apply the corrections; it will also save these corrections in the
       flash storage of the Yozh slave microcontroller, where they will be
       stored for future use.  This data is preserved even after you power
       off the robot (much like the usual USB flash drive).

       This function will take about 10  seconds to execute; during this time,
       the robot must be completely stationary on a flat horizontal surface.

If you had previously calibrated the sensor, you do not need to repeat the
calibration process - by default, upon initialization the IMU loads previously
saved calibration values.

Note that the IMU is somewhat sensitive to temperature changes, so if the
temperature changes (e.g., you moved your robot from indoors to the street for
testing), it is advised that you recalibrate the IMU.

Reading Values
--------------

Yozh  allows you to read both the raw data (accelerometer and gyro readings)
and computed orientation, using the following functions:

.. function:: void IMU_get_accel()

   Fetches from  the sensor  raw acceleration data and saves it using member
   variables ``ax``, ``ay``, ``az``, which give the acceleration
   in x-, y-, and z- directions respectively in in units of 1g
   (9.81 m/:math:`sec^2`) as floats.

.. function:: void IMU_get_gyro()

   Fetches from the sensor  raw gyro data and saves it using member variables
   ``gx``, ``gy``, ``gz``, which give the angular rotation velocity around
   x-, y-, and z- axes respectively, in degree/s (as floats).

.. function:: float IMU_yaw()

.. function:: float IMU_pitch()

.. function:: float IMU_roll()

   These functions return yaw, pitch, and roll angles for the robot, in degrees. 
   These three angles determine the robot orientation as described below:

   * yaw is the rotation around the vertical axis (positive angle corresponds to
     clockwise rotation, i.e. right turns), relative to the starting position of
     the robot
   * pitch is the rotation around the horizontal line, running from
     left to right. Positive pitch angle corresponds to raising the front of the
     robot and lowering the back
   * roll is the rotation around the horizontal line running from front to back.
     Positive roll angle corresponds to raising the left side of the robot and
     lowering the right.
   For more information about yaw, pitch, and roll angles, please visit
   https://en.wikipedia.org/wiki/Aircraft_principal_axes

Commonly used functions
====================================

Below is the list of most commonly used functions from Yozh CircuitPython library. 
This is not a full list! See :ref:`Library reference <library>`  for full list and details. 

To begin using the library, you need to put the following in the beginning of
your `code.py` file:

.. code-block:: python

   import time
   from  yozh import *
   bot = Yozh()

This creates and initializes an  object with name ``bot``, representing your robot.  From now
on, all commands you give to the robot will be functions and properties of ``bot``
object. We will not include the name bot in our references below; for example,
to use a command :func:`stop_motors()` described below, you would need to write
:func:`bot.stop_motors()`.

Display, buttons
----------------
.. function:: clear_display()

   Clears all text and graphics from display

.. function:: set_text(line_number, message)

   Print given message on a given line of the display. Line number can range 0--5. 
   Note: this command supports more options; check the library reference. 

.. function:: wait_for(button)

   Waits until the user presses the given button. There are three  possible
   pre-defined buttons: ``BUTTON_A``, ``BUTTON_B``, ``BUTTON_C``.


There are also functions for checking if a given button is currently pressed, 
or waiting until the user presses one of 3 buttons. 


LEDs, buzzer, headlights
------------------------
.. function:: set_lights(power)

   Turns the headlights on/off. Power should be between 0-100; setting the power to zero 
   turns the headlights off.


.. function:: set_leds(color_l, color_r)

   Set colors of both LEDs at the same time. Each color can be a triple 
   giving values of red, green, and blue (each 0-255) or a hex number:
   ``set_leds( (255,0,0), 0xFF0000)``. You can also use one of predefined colors: 
   RED, GREEN, BLUE, YELLOW, WHITE, OFF, e.g. ``set_leds(BLUE)``. 
   Parameter ``color_r`` is optional; if omitted, both LEDs will
   be set to the same color.

.. function:: buzz(freq, dur=0.5)

    Buzz at given frequency (in hertz) for given duration (in seconds).
    Second parameter is optional; if omitted, duration of 0.5 seconds is used.

Driving
-------
.. function:: go_forward (distance, speed=60)

.. function:: go_backward(distance, speed=60)

   Move forward/backward  by given distance (in centimeters). Parameter ``speed``, which ranges 
   between 0-100,  is optional; if not given, default speed of 60 is used.
   Note that distance and speed should always be positive, even when moving backward.

   Behind the scenes, these commands try to maintain constant robot speed and direction. 
   To learn more about how it is done check section FIXME.  

.. function:: turn(angle, speed=60)

   Turn by given angle, in degrees. Positive values correspond to turning right (clockwise).
   Parameter ``speed`` is  optional; if not given, default speed of 50 (i.e. half of maximal) is used.

.. function:: set_motors(power_L, power_R)

   Set power for left and right motors. ``power_L`` is power to left motor,
   ``power_R`` is power to right motor. Each of them should be  between 100
   (full speed forward) and -100 (full speed backward).

   Note that because no two motors are exactly identical, even if you give
   both motors same power (e.g. ``set_motors(60,60)``), their speeds might be
   slightly different, causing the robot to veer to one side instead of moving
   straight. To avoid this, use ``go_forward()`` command described above. 

.. function:: stop_motors()

   Stop  both motors.

Inertial Motion Unit (IMU)
--------------------------
Before use, the IMU needs to be calibrated. The calibration process determines
and then applies corrections (offsets)  to the raw data; without these
corrections, the  data returned by the sensor is very inaccurate.

If you haven't  calibrated the sensor before (or want to recalibrate it),
use the following function:

.. function::  IMU_calibrate()

       This function will determine and
       apply the corrections; it will also save these corrections in the
       flash storage of the Yozh secondary microcontroller, where they will be
       stored for future use.  This data is preserved even after you power
       off the robot (much like the usual USB flash drive).

       This function will take about 10  seconds to execute; during this time,
       the robot must be completely stationary on a flat horizontal surface.

If you had previously calibrated the sensor, you do not need to repeat the
calibration process - by default, upon initialization the IMU loads previously
saved calibration values.


.. function:: IMU_yaw()

   Returns robot yaw, i.e. heading in horizontal plane. Note that zero heading 
   is rather random (it is not the starting position of the robot!). Positive 
   values correspond to turning right (clockwise). 




Reflectance array
-----------------
.. function:: linearray_on()

.. function:: linearray_off()

   Turns reflectance array on/off. By default, it is off (to save power).

.. function:: calibrate()

   Calibrates the sensors, recording the black  values. This
   command should be called when all  of the sensors are on the black  area of the field.
   This is necessary for the commands below. 

.. function:: sensor_on_white(i)

.. function:: sensor_on_black(i)

   Returns ``True`` if sensor ``i`` is on white (respectively, black) and false otherwise. Index `i` 
   ranges from 0 (rightmost sensor) to 6 (leftmost)

.. function:: all_on_white()

.. function:: all_on_black()

   Returns ``True`` if all sensors are  on black (respectively, white) and false otherwise.




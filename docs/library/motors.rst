Motor control
=============

Of course, main use of this robot is to drive around, and for this, we need to
control the motors.

Basic control
-------------

.. function:: set_motors(power_L, power_R)

   Set power for left and right motors. ``power_L`` is power to left motor,
   ``power_R`` is power to right motor. Each of them should be  between 100
   (full speed forward) and -100 (full speed backward).

   Note that because no two motors are exactly identical, even if you give
   both motors same power (e.g. ``set_motors(60,60)``), their speeds might be
   slightly different, causing the robot to veer to one side instead of moving
   straight. To fix that, use PID control as described below.

.. function:: stop_motors()

   Stop  both motors.

Encoders
--------

  Both motors are equipped with encoders (essentially, rotation counters).
  For 75:1 HP motors, each motor at full speed produces about 4200 encoder ticks
  per second.

.. function:: reset_encoders()

  Resets both encoders


.. function:: get_encoders()

   Gets values of both encoders and saves them. These values can be accessed as
   described below

.. function:: encoder_L

.. function:: encoder_R

   Value of left and right  encoders, in ticks, as fetched at last call of
   ``get_encoders()``. Note that these values are not automatically updated:
   you need to call ``get_encoders()`` to update them


.. function:: get_speeds()


   Gets the  speeds of both motors  and saves them. These values can be accessed as
   described below

.. function:: speed_L

.. function:: speed_R

   Speed of left and right motors,  in ticks/second, as fetched at last call of
   ``get_speeds()``. Note that these values are not automatically updated:
   you need to call ``get_speeds()`` to update them



PID
---

PID is an abbreviation for Proportional-Integral-Differential control. This is
the industry standard way of using feedback (in this case, encoder values) to
maintain some parameter (in this case, motor speed) as close as possible to
target value.

Yozh bot has PID control built-in; however, it is not enabled by default. To
enable/disable PID, use the functions below.

Before enabling PID, you need to provide some information necessary for its
proper operation.  At the very minimum, you need to provide the speed of the
motors when running at maximal power. For 75:1 motors, it is about 4200
ticks/second; for other motors, you can find it by running ``motors_test.py`` example.

.. function:: configure_PID(maxspeed)

   Configures parameters of PID algorithm, using motors maximal speed in
   encoder ticks/second.

.. function:: PID_on()

.. function:: PID_off()

   Enables/disables  PID control (for both motors).

Once PID is enabled, you can use same functions as before (``set_motors()``,
``stop_motors()``) to control the motors, but now these functions will use
encoder feedback to maintain desired motor speed.


Drive control
-------------

Yozh python library also provides higher level commands for controlling the robot.


.. function:: go_forward (distance, speed=50)

.. function:: go_backward(distance, speed=50)

   Move forward/backward  by given distance (in centimeters). Parameter ``speed`` is
   optional; if not given, default speed of 50 (i.e. half of maximal) is used.

   Note that distance and speed should always be positive, even when moving backward.

.. function:: turn(angle, speed=50)

   Turn by given angle, in degrees. Positive values correspond to turning right (clockwise).
   Parameter ``speed`` is  optional; if not given, default speed of 50 (i.e. half of maximal) is used.


Note that all of these commands use encoder readings to determine how far to
drive or turn. Of course, to do this one needs to know how to convert from
centimeters or degrees to encoder ticks. This information is stored in properties
``bot.CM_TO_TICKS`` and ``bot.DEG_TO_TICKS``. By default, Yozh library uses
``CM_TO_TICKS = 150``, ``DEG_TO_TICKS=14``, which should be correct for 75:1 motors.
If you find that the robot consistently turns too much (or too little), you can change these values, e.g.

.. code-block:: python

    bot.DEG_TO_TICKS=15
    bot.turn(90)

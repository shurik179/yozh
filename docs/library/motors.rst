Motor control
=============

Of course, main use of this robot is to drive around, and for this, we need to
control the motors.


Basic driving 
--------------------

Yozh python library  provides high level commands for controlling the robot.


.. function:: go_forward (distance, speed=60)

.. function:: go_backward(distance, speed=60)

   Move forward/backward  by given distance (in centimeters). Parameter ``speed``, which ranges 
   between 0-100,  is optional; if not given, default speed of 60 is used.
   Note that distance and speed should always be positive, even when moving backward.    Behind the scenes, these commands try to maintain constant robot speed and direction. 
   To learn more about how it is done check section FIXME.  

   You can use special value `UNLIMITED` for distance; in this case, the command 
   starts the  robot moving forward without any distance limit. You will need to issue 
   a separate command to stop it, e.g. 


.. code-block:: python

   bot.go_forward(UNLIMITED, 50) #start moving forward a 50% speed
   time.sleep(1.0)  # wait for 1 second 
   bot.stop_motors()

   




.. function:: turn(angle, speed=60)

   Turn by given angle, in degrees. Positive values correspond to turning right 
   (clockwise). Parameter ``speed`` is  optional; if not given, default speed 
   of 50 (i.e. half of maximal) is used. Note that this fucntion relies on 
   Inertial Motion Unit (IMU) for operation, so you need to calibrate IMU at 
   least once prior to using it. See Section on IMU later. 



Driving using heading 
---------------------

If you need to make repeated turns, the errors at each turn add up, so at 
the end we might get a significant course deviation. To help combat that, 
you can use the following modification of drive and turn commands:

.. function:: turn_to(heading, direction, speed=60)

   Turn to a given heading (yaw angle), in degrees. Parameter `heading` 
   can be one of two predefined values: either `CW` (clockwise) or `CCW`
   (counterclockwise). As before, parameter ``speed`` is  optional.
   Below is an example: 

.. code-block:: python

   # bad: accumulating errors
   bot.turn(90)
   bot.go_forward(50)
   bot.turn(-90)
   bot.go_forward(50)





.. code-block:: python
   #better: errors do not accumulate

   # give name to curent robot heading 
   North = bot.IMU_get_yaw()
   bot.turn_to(North + 90, CW)
   bot.go_forward(50)
   bot.turn_to(North, CCW)
   bot.go_forward(50)

   









Low level commands 
------------------
You can also control robot motors directly: 

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

Encoders
--------

  Both motors are equipped with encoders (essentially, rotation counters).
  For 75:1 HP motors, each motor at full speed produces about 4200 encoder ticks
  per second.

.. function:: reset_encoders()

   Resets (sets to zero) both encoders. Note that encoders are also reset by commands 
   `go_forward()`, `go_backward()`, `turn()`. 


.. function:: get_encoders()

   Gets values of both encoders and saves them. These values can be accessed as
   described below

.. function:: encoder_L

.. function:: encoder_R

   Value of left and right  encoders, in ticks, as fetched at last call of
   ``get_encoders()``. Note that these values are not automatically updated:
   you need to call ``get_encoders()`` to update them


.. function:: distance_traveled()

   Returns the distance traveled by the robot since the last encoder reset. 
   It can be very useful in combination with `go_forward(UNLIMITED)`, e.g. 




.. code-block:: python

   bot.go_forward(UNLIMITED, 50) #start moving forward a 50% speed
   while (bot.all_on_black() and bot.distance_traveled() < 20):
      pass
   # stop once we have traveled 20 cm or one of reflectacne sensors sees white, whatever comes first 
   bot.stop_motors()



   



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

FIXME 

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


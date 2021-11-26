Reflectance sensor array
========================
Yozh has a built-in array of reflectance sensors, pointed down. These sensors
can be used to detect filed borders, for following the line, and other similar
tasks.

Basic usage
-----------
.. function:: linearray_on()

.. function:: linearray_off()

   Turns reflectance array on/off. By default, it is off (to save power).


.. function:: linearray_raw(i)

   Returns raw reading of sensor ``i``. One can use either indices 0...7 or
   (preferred) named values ``bot.A1 = 0`` ... ``bot.A8 = 7``.
   Readings range 0-1023 depending on amount of reflected light: the more light
   reflected, the **lower** the value. Typical reading on white paper is about 50-80, and on
   black painted plywood,  950. Note that black surfaces can be unexpectedly
   reflective; on some materials which look black to human eye, the reading
   can be as low as 600.

Calibration
-----------

Process of calibration refers to learning the values corresponding to black
and white areas of the field and then using these values to rescale the raw
readings.

.. function:: calibrate()

   Calibrates the sensors, recording the lowest and highest values. This
   command should be called when some of the sensors are on the white area
   and some, on black.

.. function:: linearray_cal(i)

   Returns reading of sensor ``i``, rescaled to 0-100:  white corresponds to 0
   and black to 100. It uses the calibration data, so should only be used after
   the sensor array  has been calibrated.

.. function:: sensor_on_white(i)

   Returns ``True`` if sensor ``i`` is on white and false otherwise. A sensor
   is considered to be on white if calibrated value is below 50.

.. function:: sensor_on_black(i)

   Returns ``True`` if sensor ``i`` is on black and false otherwise.


Line following
--------------

A common task for such robots is following the line. To help with that,
Yozh library provides the helper function.

.. function:: line_position_white()

    Returns a number showing position of the line under the robot, assuming
    white line on black background.   The number
    ranges between -5 (line far to the left of the robot) to 5 (line far to
    the right of the robot). 0 is central position: line is exactly under the
    center of the robot.

    Slightly simplifying, this command works by counting how many sensors are
    to the left of the line, how many are to the right, and then taking the
    difference. It works best for lines of width 1-2cm; in particular, electric
    tape or gaffers tape  (1/2" or 3/4") works well.

    This command only uses the central 6 sensors; rightmost and leftmost sensor
    (A1 and A8) are not used.

    If there is no line under these sensors, the value returned by this command
    will be close to 0, but can not be relied on.

.. function:: line_position_black()

    Same as above, but assuming black line on white background.

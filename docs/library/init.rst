Initialization and general functions
====================================

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



Here are some basic functions:

.. function:: fw_version()

   Returns firmware version as a string. e.g. `2.1`.

.. function:: battery_voltage()

   Returns battery voltage, in volts. For normal operation it should be at
   least 3.7 V. Fully charge battery produces about 4.1 - 4.2 V. 

.. function:: battery_percent()

   Returns charge percent (0 - 100).

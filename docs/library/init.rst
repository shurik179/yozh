Initialization and general functions
====================================

To begin using the library, you need to put the following in the beginning of
your `code.py` file:

.. code-block:: python
   import yozh
   bot = yozh.Yozh()


This creates  an  object with name `bot`, representing your robot.  From now
on, all commands you give to the robot will be functions and properties of `bot`
object. We will not include the name bot in our references below; for example,
to use a command :func:`stop_motors()` described below, you would need to write
:func:`bot.stop_motors()`.

Here are some basic functions:

.. function:: battery()

   Returns battery voltage, in volts. For normal operation it should be at
   least 4.5 V.

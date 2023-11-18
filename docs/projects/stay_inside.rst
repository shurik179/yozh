Stay inside the field
=====================

We begin with a very simple project: staying in the field. Here, we assume
that we have a black field (such as black painted plywood) with boundary
marked by white tape. The goal is to program the robot to stay within the field
boundaries.

First attempt (in pseudocode, not including the intialization):

.. code-block:: python

    go forward until robot sees white boundary
    turn around


To see the boundary, we use reflectance sensor array, namely function
`all_on_black()`: if this function returns `False`, at least one of the sensors
sees the white boundary. We also replace "go forward until..." by more common `while` loop:

.. code-block:: python

    bot.set_motors(30,30)
    while bot.all_on_black():
        pass
    #if we are here, it means at least one of sensors sees white
    bot.stop_motors()
    bot.turn(180)


Note that there is no need to set motor speed inside `while bot.all_on_black()`
loop: the motors are already running and will continue doing so until you
explicitly stop them .
`

Finally, we enclose it in `while True` loop to make it repeat forever:

.. code-block:: python

    while True:
        bot.set_motors(30,30)
        while bot.all_on_black():
            pass
        #if we are here, it means at least one of sensors sees white
        bot.stop_motors()
        bot.turn(180)

This is far from optimal. For example, if it is the right sensor that sees the
boundary, it makes sense to turn left rather than turn 180 degrees:

.. code-block:: python

    while True:
        bot.set_motors(30,30)
        while bot.all_on_black:
            pass
        #if we are here, it means at least one of sensors sees white
        if bot.sensor_on_white(bot.A1):
            turn(-120)
        else:
            turn(120)

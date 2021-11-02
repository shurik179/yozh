Display, buttons, LEDs
======================

LEDs
-----



.. function:: set_led_R(color)

   These commands set the left (respectively, right) LED to given color. Color
   must be a list of 3 numbers, showing the values of Red, Green, and Blue
   colors, each ranging between 0--255, e.g. ``bot.set_color_L([255,0,0])`` to set
   the left LED red.  You can also define named colors for easier use, e.g.

.. code-block:: python

   RED=[255,0,0]
   GREEN=[0,255,0]
   BLUE=[0,0,255]
   bot.set_led_L(BLUE)
   bot.set_led_R(GREEN)

.. function:: set_leds(color_l, color_r)

   Set colors of both LEDs at the same time. As before, each color is a list of
   three values. Parameter ``color_r`` is optional; if omitted, both LEDs will
   be set to the same color.

.. function:: set_led_brightness(value)

   Set the maximal brightness of both LEDs to a given value (ranging 0-255).
   Default value is 32 (i.e., 1/8 of maximal brightness), and it is quite
   adequate for most purposes, so there is rarely a need to change it. Setting
   brightness to 255 would produce light bright enough to hurt your eyes (and
   drain the batteries rather quickly)


Buttons
-------

.. function:: wait_for(button)

   Waits until the user presses the given button. There are two possible
   pre-defined buttons: ``bot.button_A`` and ``bot.button_B``

.. function:: is_pressed(button)

   Returns ``True`` if given button is currently pressed and ``False`` otherwise.

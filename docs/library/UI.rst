Display, buttons, LEDs
======================

Yozh contains a buzzer,  two NeoPixel  LEDs in the back and an 240x135 color TFT screen and
three buttons on the top plate, for interaction with the user. To control them,
use the functions below.

LEDs
-----
.. function:: set_led_L(color)

.. function:: set_led_R(color)

   These commands set the left (respectively, right) LED to given color. Color
   must be one of the following: 

   * a tuple of 3 numbers, showing the values of Red, Green, and Blue
     colors, each ranging between 0--255, e.g. ``bot.set_led_L( (255,0,0))`` to set
     the left LED red.  

   * A 32-bit integer, usually written in the hexadecimal form: ``0xRRGGBB``, where each letter 
     stands for a hexadecimal digit 0...F. 
     E.g. ``0xFF0000`` is the same as ``(255,0,0)`` ande defines the red color. 

   * One of predefined colors, e.g. ``RED``. Full list of predefined colors is: 
     RED, GREEN, BLUE, YELLOW, WHITE, OFF. You can also define your own colors, e.g. 

.. code-block:: python

    ORANGE=0xFFA500

    bot.set_led_L(ORANGE)

.. function:: set_leds(color_l, color_r)

   Set colors of both LEDs at the same time. Parameter ``color_r`` is optional; if omitted, both LEDs will
   be set to the same color.

Buzzer
------

.. function:: buzz(freq, dur=0.5)

    Buzz at given frequency (in hertz) for given duration (in seconds).
    Second parameter is optional; if omitted, duration of 0.5 seconds is used.

Buttons
-------

.. function:: wait_for(button)

   Waits until the user presses the given button. There are three  possible
   pre-defined buttons: ``BUTTON_A``, ``BUTTON_B``, ``BUTTON_C``.

.. function:: is_pressed(button)

   Returns ``True`` if given button is currently pressed and ``False`` otherwise.

.. function:: choose_button()

    Waits until the user presses one of the  buttons. This function returns
    string literal ``A``, ``B``,  or ``C`` depending on the pressed  button:

.. code-block:: python

    bot.set_text(1, "Press any button")
    #wait until user presses one of buttons
    if (bot.choose_button()=="A"):
        # do something
    else:
        # do something else


Display
-------

The easiest way to interact with the TFT  display is by using the commands below.

.. function:: clear_display()

   Clears all text and graphics from display

.. function:: set_text(line_number, message, font, color)

   Print given message on a given line of the display. Line number can range 0--5. Parameters 
   ``font``  and ``color`` are optional: if omitted, default font and white color are used. 

   The basic use of this command is

.. code-block:: python

   bot.set_text(0, "Press A to continue")

You can print multi-line messages, separating lines by ``\n``, e.g. 

.. code-block:: python

   bot.set_text(1, "Put robot on black \nand press A to continue")

This will print ``Put robot on black`` on line 1 and ``and press A to continue`` on line 2. 

To use a different font, use optional parameter ``font``. Posible choices are: 

* ``FONT_REGULAR``: usual font 

* ``FONT_BOLD``: slightly larger bold font 

* ``FONT_SMALL``: really small font, useful for long messages 



Advanced users may also use any commands from CircuitPython ``displayio`` module
to put text and graphics on the TFT display as described in  https://learn.adafruit.com/circuitpython-display-support-using-displayio.
The display object of the robot  can be accessed as ``bot.display``,  and the root group of the display is 
``bot.canvas``. E.g., one could use 

.. code-block:: python


   label=bitmap_label.Label(font = FONT_BOLD, text="DANGER", color = 0xFF0000, scale = 2, x=50, y=30)
   bot.canvas.append(label)
   bot.display.refresh()

Note that ``display.auto_refresh`` property is set to ``False``, so you need to 
explicitly call ``display.refresh()`` function. 
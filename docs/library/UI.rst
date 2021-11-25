Display, buttons, LEDs
======================

Yozh contains  two NeoPixel  LEDs in the back and an 128x64 OLED screen and
two buttons on the top plate, for interaction with the user. To control them,
use the functions below.

LEDs
-----
.. function:: set_led_L(color)

.. function:: set_led_R(color)

   These commands set the left (respectively, right) LED to given color. Color
   must be a list of 3 numbers, showing the values of Red, Green, and Blue
   colors, each ranging between 0--255, e.g. ``bot.set_led_L([255,0,0])`` to set
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
   Default value is 64 (i.e., 1/4 of maximal brightness), and it is more than
   adequate for most purposes, so there is rarely a need to change it. Setting
   brightness to 255 would produce light bright enough to hurt your eyes (and
   drain the batteries rather quickly)


Buzzer
------

.. function:: buzz(freq, dur=0.5)

    Buzz at given frequency (in hertz) for given duration (in seconds).
    Second parameter is optional; if omitted, duration of 0.5 seconds is used.
       
Buttons
-------

.. function:: wait_for(button)

   Waits until the user presses the given button. There are two possible
   pre-defined buttons: ``bot.button_A`` and ``bot.button_B``

.. function:: is_pressed(button)

   Returns ``True`` if given button is currently pressed and ``False`` otherwise.


OLED
----

The easiest way to interact with OLED display is by using the commands below.

.. function:: clear_display()

   Clears all text and graphics from display

.. function:: add_textbox()

   Add textbox (also known as label) to display. You can enter the actual text
   when creating the textbox, or replace it later. The command returns index
   of the textbox, which can be used to update teh contents of the textbox later.

   The basic use of this command is

.. code-block:: python

   line1 = bot.add_textbox(text_position=(0,10), text="Yozh is happy!")


The command accepts a number of optional parameters, documented below.

  :param  text_font: The path to your font file for your data text display.

  :param text_position: The position of  text on the display in an (x, y) tuple.

  :param text_wrap:  When non-zero, the maximum number of characters on each
                     line before text is wrapped. (for long text data chunks).
                     Defaults to 0, no wrapping.

  :param text_maxlen: The max length of the text. If non-zero, it will be
                      truncated to this length. Defaults to 0, no truncation.

  :param text_scale: The factor to scale the default size of the text by

  :param line_spacing: The factor to space the lines apart

  :type line_spacing: float

  :param (float,float) text_anchor_point: Values between 0 and 1 to indicate where the text
                                          position is relative to the label

  :type text_anchor_point: (float, float)

  :param text: If this is provided, it will set the initial text of the textbox.

.. function:: set_text(text, i)

   Replaces  text in textbox  with index ``i``, e.g.

.. code-block:: python

   line1 = bot.add_textbox(text_position=(0,10), text="Yozh is happy!")
   time.sleep(1.0)
   bot.set_text("Press any button", line1)

Writing empty text into a textbox deletes it. Thus, if you want to erase
current text but keep the textbox for future use, replace the text with a
single space ``bot.set_text(" ", i)``

Advanced users may also use any commands from CircuitPython ``displayio`` module
to put text and graphics on the OLED display as described in  https://learn.adafruit.com/circuitpython-display-support-using-displayio.
The display object of the robot  can be accessed as ``bot.display``, e.g.

.. code-block:: python

   display = bot.display
   # Setup the file as the bitmap data source
   bitmap = displayio.OnDiskBitmap("/purple.bmp")

  # Create a TileGrid to hold the bitmap
  tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

  # Create a Group to hold the TileGrid
  group = displayio.Group()

  # Add the TileGrid to the Group
  group.append(tile_grid)

  # Add the Group to the Display
  display.show(group)

Power
=====

Batteries
---------
Yozh is powered by one or two 18650 Li-Ion batteries, inserted in the
battery compartment inside the robot; to access it, you need to remove
the top plate.  See the section below for discussion of whether you
need one or two batteries.

**Warning**: Li-Ion batteries can be dangerous if not handled right! please
make sure to place them with  correct polarity, and follow the instructions in the
next section if you use two batteries. Always turn the power switch off before
removing the top plate or doing any other work on the robot.


It is highly recommended that you use batteries from a trusted manufacturer,
such as Panasonic, Samsung,  or Sanyo; do not try to save a couple of dollars by
buying a no-name battery from   Amazon or  eBay - instead, use one of
specialized shops such as https://www.18650batterystore.com/.  You need  **flat
top unprotected batteries**; look for batteries with capacity 3000 mAh or more.
Current rating is less important (you need a battery rated for 4A continuous
current or more  -- this is  low by the standards of 18650 battery cells). A
good choice is this battery:
https://www.18650batterystore.com/products/samsung-35e



The robot also contains power switch, for disconnecting the battery, and a
power indicator LED.
You can check the battery voltage in software, using ``battery_voltage()`` function as
described in  :ref:`Yozh Library Guide <library>`. Fully charged Li-Ion batteries
should read about 4.2v.

One or two batteries?
---------------------

For most purposes, one 18650 battery is sufficient. Place it in the slot
closest to the back of the robot. Make sure to place it with correct polarity;
positive and negative terminals are labeled on the robot PCB.

If you are planning on using accessories that might use significant current,
such as large size servos or AI cameras, or if you want to run the robot for
long periods, you might want to add a second battery; these two batteries will
be connected in parallel.

If you want to use two batteries, please observe these precautions. Please
take them seriously!

* it is best to use the two identical batteries (same manufacturer and model)

* before inserting the batteries, turn the power switch to off and **remove the
jumper  J14** next to the batteries. After this, insert the batteries;  leave
them inserted for a couple of hours or so, keeping the power switch off. After
two hours, put the jumper J14 back on.    (This allows the
two batteries to equalize the voltage. The positive terminals are connected
through on-board 1 Ohm resistor. Jumper J14 shorts it.)


Voltages used by the robot
--------------------------
The robot contains a voltage regulator, which converts battery voltage
to regulated 3.3v. This regulator provides power to the secondary MCU, IMU
and distance sensors, leaving about 300 mA available for use by extra sensors
you might connect to  Yozh.

Yozh also contains a boost converter, converting battery voltage to regulated 6V.
This is used to power the motors and servos.

Finally, some of the on-board electronics are powered directly from the battery voltage:
the main MCU and TFT  screen, Neopixels and headlights.

Connecting the ESP32-S3 microcontroller to a computer by USB cable provides power
to the MCU  even if the main battery is off. This would activate the main  MCU
and some of the electronics, but not the secondary MCU, motors or servos.



.. figure:: ../images/overview-back.png
    :alt: Rear view
    :width: 80%

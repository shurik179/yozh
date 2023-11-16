Power
=====

Batteries
---------
Yozh is powered by one or two 18650 Li-Ion batteries, inserted in the
battery compartment inside the robot; to access it, you need to remove
the top plate.  See the section below for discussion of whether you
need one or two batteries.



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

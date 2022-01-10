Top plate
=========
On the top of Yozh robot, there is a top plate containing the following
elements:

* an OLED display (1.3" size, 128x64 pixels)

* two buttons

* two Qwiic/Stemma QT I2C connectors (on the back side of the plate)

* a number of 3mm mounting holes for attaching additional electronics

The top plate is mounted on the robot using 22mm long M2.5 standoffs. If
necessary, it can be removed -- just make sure to modify the code as by default
initialization code tries to initialize the OLED display.

The diagram below shows dimensions and hole locations.

.. figure:: ../images/yozh-top-plate.png
   :alt: Top plate engineering drawing
   :width: 80%

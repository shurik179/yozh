Connecting additional sensors
=============================
Yozh uses some of the ItsyBitsy pins for controlling built-in electronics as
shown in the table below. All other pins are available for connecting additional
sensors or other electronics.

+--------------+--------------------------------------+
| Pin          | Function                             |
+==============+======================================+
| SDA          | Used by I2C bus.                     |
+--------------+                                      |
| SCL          |                                      |
+--------------+--------------------------------------+
| 5            |         Buzzer                       |
+--------------+--------------------------------------+
| 7            | Used by front distance sensors board |
+--------------+--------------------------------------+
| 12           | Button B                             |
+--------------+--------------------------------------+
| 13           | Button A                             |
+--------------+--------------------------------------+
| 25           | Used by front distance sensors board |
+--------------+--------------------------------------+

I2C bus
-------
Pins SDA and SCL of ItsyBitsy are used for I2C communication with the following
components of the robot:

* Secondary MCU (I2C address: `0x11`)

* OLED display (I2c address: `0x3c`)

* Front distance sensors (I2C addresses `0x29`, `0x30`)

You can connect additional devices to the same bus as long as they have addresses
different from those listed above.

The bus operates at 3.3v; the main board contains pull-up resistors for i2c bus,
so additional pull-ups are not necessary.

To connect new devices, you can use either the 5-pin connectors at the front
of the robot or Qwiic/Stemma QT connectors at the bottom of the top plate.


Connectors
----------


Yozh provides a number of connectors for connecting additional electronics to ItsyBitsy:

* On each side of the ItsyBitsy there are three rows of **male headers** (you need
  to remove the top plate to access these headers). The outer row is ground,
  the middle row is 3.3V, and each pin in the row closest to ItsyBitsy is
  connected to the corresponding pin of ItsyBitsy (except the VBUS pin of
  ItsyBitsy which is not connected). This allows you to connect to any pin of
  ItsyBitsy - including those used for other components.

* In the front of the robot, there are two 5-pin male connectors. They follow
  the pinout convention of Pimoroni breakout garden:

  - pin 1:  

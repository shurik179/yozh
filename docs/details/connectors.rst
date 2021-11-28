Connecting additional sensors
=============================
Yozh uses some of the ItsyBitsy pins for controlling built-in electronics;
however, many pins are available for attaching additional sensors or
other electronics. Many of these pins are broken out to easily accessible
connectors on the board.

+--------------+----------------------------+
| Pin          | Function                   |
+==============+============================+
| RX           | Available; broken out to   |
+--------------+ left Grove connector       |
| TX           |                            |
+--------------+----------------------------+
| SDA          | Used by I2C bus.           |
+--------------+                            |
| SCL          |                            |
+--------------+----------------------------+
| 5            | Used by buzzer             |
+--------------+----------------------------+
| 7            |                            |
+--------------+----------------------------+
| 9            |                            |
+--------------+----------------------------+
| 10           |                            |
+--------------+----------------------------+
| 11           |                            |
+--------------+----------------------------+
| 12           |                            |
+--------------+----------------------------+
| 13           |                            |
+--------------+----------------------------+
| USB          |  5V USB                    |
+--------------+----------------------------+
| G            |  Connected to common ground|
+--------------+----------------------------+
| BAT          | Do not use                 |
+--------------+----------------------------+
| RST          |Connected to Reset button   |
+--------------+----------------------------+
|  VHI         | Available                  |
+--------------+----------------------------+
| A0           | Available; broken out to   |
+--------------+                            |
|  A1          | right Grove connector      |
+--------------+----------------------------+
| A2           | Available; broken out to   |
|              |  right 5-pin connector     |
+--------------+----------------------------+
|  A3          | Available                  |
+--------------+----------------------------+
| 24           |                            |
+--------------+----------------------------+
|  25          | Available                  |
+--------------+----------------------------+
|  SCK         | Available                  |
+--------------+----------------------------+
|  MO          | Available                  |
+--------------+----------------------------+
|  MI          | Available                  |
+--------------+----------------------------+
|  2           | Available                  |
+--------------+----------------------------+

Yozh provides a number of connectors for connecting additional electronics.

* On each side of the ItsyBitsy there are three rows of male headers (you need
  to remove the top plate to access these headers). The outer row is ground,
  the middle row is 3.3V, and each pin in the row closest to ItsyBitsy is
  connected to the corresponding pin of ItsyBitsy (except the VBUS pin of
  ItsyBitsy which is not connected).  **Note**: some pins of ItsyBotsy

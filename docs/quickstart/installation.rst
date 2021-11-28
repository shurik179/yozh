Circuit Python library  installation
====================================
Yozh is intended to be programmed in CircuitPython 7 - an implementation of
Python programming language for microcontrollers, created by Adafruit (based on
Micropython, another Python implementation). For general background on Circuit
Python, please visit `What is CircuitPython? <https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython>`__
page.

You must have already installed CircuitPython on the ItsyBitsy microcontroller
serving as the brains of Yozh robot during assembly. If not, please do so now
following `Adafruit's  instructions <https://learn.adafruit.com/adafruit-itsybitsy-rp2040/circuitpython>`__
(you will need to remove the top plate to access the BOOTSEL button of ItsyBitsy).

Next step is installing  some CircuitPython libraries. Download the Adafruit's library bundle
as a zip file from https://circuitpython.org/libraries. Unzip the archive to your hard drive.

Connect Yozh robot to the computer using a micro USB cable. (It should be
plugged into the USB port on the ItsyBitsy RP2040.) It should appear in
your file browser as an external drive with the name `CIRCUITPY`. Open it to
view contents. It might contain a folder named `lib`; if not, create one. Now,
install the necessary libraries by copying the following files and folders from
Adafruit Circuit Python bundle to `lib` folder in `CIRCUITPY` drive:

* `adafruit_bus_device`
* `adafruit_register`
* `adafruit_display_text.mpy`
* `adafruit_displayio_ssd1306.mpy`
* `simpleio.mpy`



Next, you need to install Yozh Circuit Python library. Download the zip file of
this library from FIXME and unzip to your computer. Find in the extracted archive file
`yozh.mpy` and copy it to `lib` folder. Now, you have all the libraries you need.

Please note that extracted Yozh library archive also contains a folder `examples`.
Move this folder to some convenient location on your computer - you will use it shortly.

Circuit Python library  installation
====================================
Yozh is intended to be programmed in CircuitPython 7 - an implementation of
Python programming language for microcontrollers, created by Adafruit (based on
Micropython, another Python implementation). For general background on Circuit
Python, please visit `What is CircuitPython? <https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython>`__
page.

CircuitPython must already be installed on the ESP32-S3 microcontroller
serving as the brains of Yozh Robot. If not, please do so now
following `Adafruit's  instructions <https://learn.adafruit.com/esp32-s3-reverse-tft-feather/install-circuitpython>`__.


Next, you need to install Yozh Circuit Python library. Go to |github| and click
on green ``Code`` button to download the zip file containing all Yozh designs
and software.  Extract the zip file to your computer. Find in the extracted archive folder 
`circuitpython_library` 

Connect Yozh robot to the computer using a  USB-C cable.  It should appear in
your file browser as an external drive with the name `CIRCUITPY`. Open it to
view contents. 
Now, copy the following files and folders from the downloaded `circuitpython_library` folder to the 
`CIRCUITPY` folder: 

* `yozh.py`
* `yozh_registers.py`
* `hedgehog.bmp`
* `fonts` folder 
* `lib` folder (`CIRCUITPY` may already contain folder `lib`; if so, copy 
  all contents of `circuitpython_library/lib` to `CIRCUITPY/lib`)

Please note that extracted Yozh  archive also contains a folder `circuitpython_library/examples`.
Move this folder to some convenient location on your computer - you will use it shortly.

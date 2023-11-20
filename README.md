# Yozh Robot
Yozh is a small tracked  robot programmable in CircuitPython. 
It was  inspired by  Pololu's Zumo, but has numerous improvements over it. 
It was created by shurik179 for a robotics class at SigmaCamp.

The project description and logs are posted on Hackaday: 
https://hackaday.io/project/193665-yozh-robot. 
Detailed  user documentation is available at http://yozh.rtfd.io. 



## Status
Version 4 is mostly finished, working on documentation and fine-tuning 
various PID controllers. 





## Structure of this repository
* `docs`: documentation (used to produce docs at http://yozh.rtfd.io)
* `hardware`: design files for the custom electronics boards, BOM, etc.
* `board_support_package`: bootloader and packeg to have the secondary MCU 
   supported in Arduino IDE. Only needed fro uploading the firmware - end 
   users do not need this. 
* `firmware`: firmware for secondary MCU
* `circuitpython_library`: Circuit Python user library

## License
Ecept as noted below, all components (hardware, software, documentation) are
copyright by Alexander Kirillov  and are  released under MIT license.
See file LICENSE in this directory for full text of the license.

Circuit Python librabries included in circuitpython_library/lib are copyright by Adafruit, see
https://github.com/adafruit/Adafruit_CircuitPython_Bundle . They are released under MIT License.

Fonts included with Circuit Python library are released under SIL Open Font License.
See LICENSE file in directory circuitpython_library/fonts

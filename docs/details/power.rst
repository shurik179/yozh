Power
=====
Yozh is powered by 4 AA (also known as LR6) batteries, inserted in the
battery compartment at the bottom of the robot. It is highly recommended
that you use heavy-duty rechargeable NiMh batteries such as
`Panasonic Eneloop Pro <https://www.amazon.com/Panasonic-BK-3HCCA4BA-eneloop-Pre-Charged-Rechargeable/dp/B00JHKSL28/>`__.
You will also need a charger.

The robot also contains power switch, for disconnecting the battery, and a
power indicator LED.

The robot contains a voltage regulator, which converts battery voltage
to regulated 3.3v. Most of the robot electronics, including the microcontrollers
and most of the sensors, are powered from 3.3v bus. Motors, servos
(if connected), buzzer,  and reflectance array are powered directly from the battery.

Note that NiMh batteries are not designed for high currents. Depending on
the battery, you could count on 4-5A maximum; this would be enough for all
on-board electronics and  motors, and leave 1-2A for any electronics you want to add.
This should be OK for micro servos and a couple of sensors, but if you want to
use standard size servos or power-hungry devices such as AI cameras, you might
have issues.

Connecting the ItsyBitsy microcontroller to a computer by USB cable provides power
to 3.3v bus, even if the main battery is off. This would activate the  microcontrollers
and some of the electronics, but not the motors or servos.

You can check the battery voltage in software, using ``battery()`` function as
described in Library reference. Fully charged NiMH batteries should give about 5.5v.

Parts and materials
===================

To build Yozh Robot, you will need the following parts and materials:

* `Zumo chassis <https://www.pololu.com/product/1418>`__ by Pololu
* Two 6V N20 size micro gear motors with extended shafts. We recommend
  `these motors <https://www.pololu.com/product/2215>`__ from Pololu
* Magnetic `encoder disk <https://www.pololu.com/product/2599>`__ fitting on
  the extended shaft of the motor. (You only need two, but Pololu sells them in
  packs of 5). Note that you do not need to buy encoders, only the disks -
  encoder sensors are built into the main Yozh board.
* Yozh robot kit, available from Tindie (SOON - link coming). Contents of this kit,
  together with alternatives for those who
  prefer to build your own, is described below.
* Four AA batteries. Usual alkaline batteries will work but won't last long,  
  so use of  heavy-duty NiMH rechargeable batteries such as
  `Panasonic Eneloop Pro <https://www.amazon.com/Panasonic-BK-3HCCA4BA-eneloop-Pre-Charged-Rechargeable/dp/B00JHKSL28/>`__
  is strongly recommended. You will also need a charger for these batteries.


Yozh kit contents
-----------------
Below is the contents of the Yozh kit, together with alternative sources
for buying these parts if for some reason you prefer not to use the kit.

*  Itsy Bitsy RP2040 microcontroller (available from `Adafruit <https://www.adafruit.com/product/4888>`__)
   and male headers

* Five custom PCBs:

  * Main electronics board
  * Spacer board
  * Reflectance sensor array board
  * Top cover with OLED display
  * Front distance sensor board
  Design files and BOM for these boards are available from Yozh |github|.

* Steel front blade to be attached to the robot. The blade is made of  0.030" stainless
  steel; DXF file for the blade is in |github|. You can use Pololu's `lasercutting
  services <https://www.pololu.com/product/749>`__ to cut the blade for you.

* Mounting hardware:

  * Four 22mm M2.5 female brass standoffs and 8 M2.5 screws (8mm length), for mounting
    the top plate
  * Two 15mm M3 brass female standoffs and two M3 screws, for attaching the
    reflectance sensor board
  * Two 6mm M3 M-F standoffs. Note: it is required that the male thread length be at
    least 6mm, which is somewhat unusual. You can find such standoffs on AliExpress,
    e.g. here: https://www.aliexpress.com/item/32872847199.html?spm=a2g0s.9042311.0.0.27424c4dmfu9xI
    (choose option **M3 (thread 8mm)**, and length 6mm).

* Two long (15mm) 4-pin male headers

Tools
-----
You will also need to have a computer to program the robot, and some basic tools:
soldering iron, wire strippers, flush cutters, screwdriver, pliers.

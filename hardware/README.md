# Hardware components for Yozh

This directory contains various hardware design files for Yozh. It includes
the following files and directories:

* `mainboard`: directory with design files for the main electronics board
* `spacer`: design files for the  spacer,  which goes between the main board and the chassis
* `reflectance_sensor_array`: design files for the reflectance sensor array   
* `top_plate`, `top_plate-LSM6`: design files for two different versions of the  
   top plate, containingin OLED display, buttons, and IMU. Current version of
   the robot uses `top_plate-LSM6`, which is based on LSM6DSL 6 degree of freedom
   Inertial Motion Unit.
   Folder `top_plate` contains design based on ICM42968 9DOF IMU; this is work in progress to be used in future versions.
* `front_sensors`: design files for  the removable board containing the two front-facing distance sensors
* `blade.dxf`: the DXF file of the front blade. This blade is to be lasercut
  from 0.030" stainless steel (you can use Pololu [laser-cutting service](https://www.pololu.com/product/749)  for it. )
* `pins.xlsx`: spreadsheet listing all pins of SAMD21 MCU and their use
* `board frame.stl`: STL file of the 3d printed holder I used to hold the mainboard
   for stenciling solder paste

Each design directory contains KiCad 6.0  design files, BOM, and gerbers.  
I assembled the mainboard myself; the top plate, reflectance sensor array, and front sensor board I ordered assembled from JLCPCB. These directories  have two versions of BOM: general and for JLCPCB assembly.

All PCBs use 1.6mm thickness, black soldermask and white screen. The main board
is a 4-layer PCB, all others are 2-layer.

Servos
======

Yozh has two ports for connecting servos. To control them, use the commands below.

.. function:: set_servo1(position)

.. function:: set_servo2(position)

   Sets servo 1/servo 2  to given position. Position ranges between 0 and 1;
   value of 0.5 corresponds to middle (neutral) position.

   Note that these commands expect that the servo is capable of accepting
   pulsewidths from  500 to 2500 microseconds. If the servo you are using has
   smaller range (e.g. HiTec servos have range of 900 to 2100 microseconds),
   it means that maximal position of the servo will be achieved for values
   smaller than 1. FIXME 

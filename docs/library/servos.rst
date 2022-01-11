Servos
======

Yozh has two ports for connecting servos. To control them, use the commands below.

.. function:: set_servo1(position)

.. function:: set_servo2(position)

   Sets servo 1/servo 2  to given position. Position ranges between 0 and 1;
   value of 0.5 corresponds to middle (neutral) position.

   Note that these commands expect that the servo is capable of accepting
   pulsewidths from  500 to 2500 microseconds. Many servos use
   smaller range; for example, HiTec servos have range of 900 to 2100 microseconds.
   For such a servo, it will reach maximal turning angle for position value less
   than one (e.g., for HiTec servo, this value will be 0.8); increasing position
   value from 0.8 to 1 will have no effect. Similarly, minimal angle  will be
   achieved for ``position = 0.2``.


   **Warning**: please remember that if a servo is unable to reach the set
   position because of some mechanical obstacle (e.g., grabber claws can not
   fully close because there is an object between them), it will keep trying,
   drawing significant current. This can lead to servo motor overheating quickly;
   it can also lead to voltage drop of Yozh battery, interfering with
   operation of motors or other electronics. Thus, it is best to avoid such
   situtations.

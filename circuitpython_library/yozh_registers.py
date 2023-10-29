# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
#
# SPDX-License-Identifier: MIT
#
# This file contains definitions and basic functions for
# interaction between Yozh master (ESP32-S3) and slave MCU

# Registers
# R/W registers
YOZH_REG_MAX_SPEED           =const(0)
YOZH_REG_PID_KP              =const(2)
YOZH_REG_PID_TI              =const(4)
YOZH_REG_PID_TD              =const(6)
YOZH_REG_PID_ILIM            =const(8)
YOZH_REG_MOTOR_CONFIG        =const(10)
YOZH_REG_MOTOR_MODE          =const(11)
YOZH_REG_DIRECTION           =const(12)
YOZH_REG_POWER_L             =const(14)
YOZH_REG_POWER_R             =const(16)
YOZH_REG_SERVO1              =const(18)
YOZH_REG_SERVO2              =const(20)
YOZH_REG_ENC_RESET           =const(22)
YOZH_REG_IMU_INIT            =const(23)
YOZH_REG_LINEARRAY_INIT      =const(24)

#Read-only registers
YOZH_REG_FW_VERSION          =const(40)
YOZH_REG_WHO_AM_I            =const(42)
YOZH_REG_IMU_STATUS          =const(43)
YOZH_REG_ENCODER_L           =const(44)
YOZH_REG_ENCODER_R           =const(48)
YOZH_REG_SPEED_L             =const(52)
YOZH_REG_SPEED_R             =const(54)
YOZH_REG_LINEARRAY_RAW       =const(56)
YOZH_REG_ACCEL               =const(74)
YOZH_REG_GYRO                =const(80)
YOZH_REG_YAW                 =const(86)
YOZH_REG_PITCH               =const(88)
YOZH_REG_ROLL                =const(90)
YOZH_REG_QUAT                =const(92)

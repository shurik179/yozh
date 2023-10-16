# The MIT License (MIT)
#
# Copyright (c) 2021 Alexander Kirillov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`yozh`
====================================================

This is a MicroPython library for Yozh robot.

* Author(s): Alexander Kirillov
* Version: 2.0
"""
from machine import Pin, PWM, I2C
from micropython import const
from time import sleep
from ssd1306 import SSD1306_I2C
# https://www.tomshardware.com/how-to/oled-display-raspberry-pi-pico

YOZH_DEFAULT_I2C_ADDR   =const(0x11)
# buttons
YOZH_BUTTON_A   = 11 # D13 = GPIO11
YOZH_BUTTON_B   = 10 # D12 = GPIO10
# buzzer
YOZH_BUZZER     = 14 # D5 = GPIO14
# distance sensors XSHUT pins
YOZH_XSHUT_L    = 6  #XSHUT1=I1 - pin D7 = GPIO6
YOZH_XSHUT_R    = 25 #XSHUT2=I2 - pin D25 = GPIO25

# Registers
# R/W registers
YOZH_REG_MAX_SPEED           =const(0)
YOZH_REG_PID_KP              =const(2)
YOZH_REG_PID_TI              =const(4)
YOZH_REG_PID_TD              =const(6)
YOZH_REG_PID_ILIM            =const(8)
YOZH_REG_MOTOR_CONFIG        =const(10)
YOZH_REG_MOTOR_MODE          =const(11)
YOZH_REG_POWER_L             =const(12)
YOZH_REG_POWER_R             =const(14)
YOZH_REG_DRIVE_DISTANCE      =const(16)
YOZH_REG_TURN_ANGLE          =const(20)
YOZH_REG_DRIVE_SPEED         =const(22)
YOZH_REG_ENC_RESET           =const(24)
YOZH_REG_IMU_INIT            =const(25)
YOZH_REG_NEOPIXEL_L          =const(26)
YOZH_REG_NEOPIXEL_R          =const(29)
YOZH_REG_NEOPIXEL_BRIGHTNESS =const(32)
YOZH_REG_LINEARRAY_INIT      =const(33)
YOZH_REG_SERVO1              =const(34)
YOZH_REG_SERVO2              =const(36)

#Read-only registers
YOZH_REG_FW_VERSION          =const(40)
YOZH_REG_WHO_AM_I            =const(42)
YOZH_REG_IMU_STATUS          =const(43)
YOZH_REG_ENCODER_L           =const(44)
YOZH_REG_ENCODER_R           =const(48)
YOZH_REG_SPEED_L             =const(52)
YOZH_REG_SPEED_R             =const(54)
YOZH_REG_LINEARRAY_RAW       =const(56)
YOZH_REG_VSENSE              =const(72)
YOZH_REG_ACCEL               =const(74)
YOZH_REG_GYRO                =const(80)
YOZH_REG_MAG                 =const(86)
YOZH_REG_YAW                 =const(92)
YOZH_REG_PITCH               =const(94)
YOZH_REG_ROLL                =const(96)
YOZH_REG_QUAT                =const(100)
YOZH_REG_DRIVE_STATUS        =const(116)

# imu constants
gRes = 500.0 / 32768.0   # gyro resolution, in (deg/s)/LSB
aRes = 2.0 / 32768.0     # accelerometer resolution, in g/LSB


#colors


class Yozh:
# color constants


    def __init__(self,  oled=0x3C, address=YOZH_DEFAULT_I2C_ADDR, distance_sensors=True):
        self._i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
        self._addr = address
        self.button_A=Pin(YOZH_BUTTON_A, Pin.IN, Pin.PULL_UP)
        self.button_B=Pin(YOZH_BUTTON_B, Pin.IN, Pin.PULL_UP)
        self.buzzer = PWM(Pin(YOZH_BUZZER))
        self.encoder_L = 0
        self.encoder_R = 0
        self.speed_L   = 0
        self.speed_R   = 0
        self.ax        = 0    #acceleration
        self.ay        = 0
        self.az        = 0
        self.gx        = 0    #gyro
        self.gy        = 0
        self.gz        = 0
        self._calibrate_W = 70   #reasonable defaults for black and white sensor readings
        self._calibrate_B = 950
        self._threshold = 500    # black/white threshold
        self._yaw_offset = 0
        sleep(0.2)
        # probe yozh
        try:
            who_am_i = self._read_8(YOZH_REG_WHO_AM_I)
        except OSError:
            who_am_i = 0

        if who_am_i != YOZH_DEFAULT_I2C_ADDR:
            print(who_am_i);
            raise RuntimeError("Could not find Yozh robot at   address 0x{:X}".format(address))
        else:
            print("Yozh bot initialized")
        # now initialize the display and buttons
        if oled is not None:
            self._oled = SSD1306_I2C(128, 64, self._i2c)

        '''
        if distance_sensors:
            YOZH_XSHUT_L.off() #turn off left
            YOZH_XSHUT_R.on()  #turn on right
            # configure i2c address of right sensor
            self.distance_R = VL53L0X(i2c)
            self.distance_R.set_address(0x30)
            # now, turn on the left one as well; it iwll use default address of 0x29
            YOZH_XSHUT_L.on()
            self.distance_L = VL53L0X(i2c)
        '''

        #give names to reflectance sensors
        self.A1=0
        self.A2=1
        self.A3=2
        self.A4=3
        self.A5=4
        self.A6=5
        self.A7=6
        self.A8=7
        # various constants
        self.CM_TO_TICKS = 150
        self.DEG_TO_TICKS = 14
        # basic configuration of PID
        self.configure_PID(maxspeed=4200)
        self._pid = False


######## start and basic diagnostics
    def begin(self):
        self.clear_display()
        self.set_text("Yozh initialized!", 0)
        sleep(1.0)
        # show  basic info
        self.set_text("FW version: "+ self.fw_version(), 1)
        voltage = self.battery()
        self.set_text("Voltage: {}".format(voltage), 2)
        # set both LEDs to Blue. Allowed predefined colors: RED, BLUE, GREEN
        self.set_leds([0,0,255])


######## Firmware version
    def fw_version(self):
        """Returns firmware version as a string"""
        minor = self._read_8(YOZH_REG_FW_VERSION)
        major = self._read_8(YOZH_REG_FW_VERSION + 1)
        version="{}.{}"
        return(version.format(major,minor))
######## BATTERY LEVEL

    def battery(self):
        """Returns battery level, in volts"""
        raw = self._read_16(YOZH_REG_VSENSE)
        voltage = raw*6.6/1023.0 # reference voltage =3.3V; taking into acct voltage divider
                                 # we get 1023 = 6.6V
        return(round(voltage,2))

##########  BUTTONS ########################################

    def wait_for(self,pin):
        while (pin.value()):
            pass

    def is_pressed(self, pin):
        return(not pin.value())


    def choose_button(self):
        while (self.button_A.value() and self.button_B.value()):
            pass
        if (not self.button_A.value()):
            # Button A was pressed
            return "A"
        else:
            return "B"


##########  MOTORS ########################################
    def set_motors(self, power_left, power_right):
        """Sets the power for motors. Each value ranges from -100..100."""
        if power_left>100:
            power_left=100
        elif power_left<-100:
            power_left=-100
        if power_right>100:
            power_right=100
        elif power_right<-100:
            power_right=-100

        self._write_16_array(YOZH_REG_POWER_L,[(int)(power_left*5), (int)(power_right*5)])

    def stop_motors(self):
        """Stops both motors."""
        self._write_16_array(YOZH_REG_POWER_L,[0,0])

    def get_encoders(self):
        """
        Gets and saves values of the two encoders
        """
        self.encoder_L = self._read_32(YOZH_REG_ENCODER_L)
        self.encoder_R = self._read_32(YOZH_REG_ENCODER_R)

    def get_distance(self):
        """
        returns the distance driven since last encoder reset
        """
        self.get_encoders()
        return ((self.encoder_L+self.encoder_R)/self.CM_TO_TICKS)

    def reset_encoders(self):
        self._write_8(YOZH_REG_ENC_RESET, 0x01)
        self.encoder_L=0
        self.encoder_R=0
        self.speed_L=0
        self.speed_R=0



    def get_speeds(self):
        """
        Gets and saves speeds (ticks/s) of the two motors
        """
        self.speed_L = self._read_16(YOZH_REG_SPEED_L)
        self.speed_R = self._read_16(YOZH_REG_SPEED_R)


##########  Motor/PID config ########################################
    def configure_PID(self, maxspeed, Kp = None, Ti = None, Td = None, Ilim = None ):
        """
        Configures PID.
        Maxspeed is motor free rotation speed, in ticks/s.
        The rest is documented in yozh.rtfd.org
        """
        if Kp is None:
            Kp = 0.8/maxspeed
            Ti = 0.3
            Td = 0.03
            Ilim = 1000
        data = [round(maxspeed), round(Kp*10000000), round(Ti*1000), round (Td*1000), round(Ilim)]
        self._write_16_array(YOZH_REG_MAX_SPEED, data)

    def PID_on(self):
        self._write_8(YOZH_REG_MOTOR_MODE, 0x02)
        self._pid = True

    def PID_off(self):
        self._write_8(YOZH_REG_MOTOR_MODE, 0x00)
        self._pid = False


##########  DRIVING ########################################

    def go_forward(self, distance, speed=50):
        self.reset_encoders()
        old_pid_mode = self._pid
        self.PID_on()
        self.set_motors(speed, speed)
        target = self.CM_TO_TICKS * distance # travel for given number of  cm
        while (self.encoder_L+self.encoder_R<target):
            self.get_encoders()
        self.stop_motors()
        # restore old pid setting
        if not old_pid_mode:
            self.PID_off()


    def go_backward(self, distance, speed=50):
        self.reset_encoders()
        old_pid_mode = self._pid
        self.set_motors(-speed, -speed)
        target = -self.CM_TO_TICKS * distance # travel for given number of  cm
        while (self.encoder_L+self.encoder_R>target):
            self.get_encoders()
        self.stop_motors()
        # restore old pid setting
        if not old_pid_mode:
            self.PID_off()

    def turn(self, angle, speed=50):
        self.reset_encoders()
        target = self.DEG_TO_TICKS * angle # turn by given number of degrees
        if angle>0:
            self.set_motors(speed, -speed)
            while (self.encoder_L-self.encoder_R<target):
                self.get_encoders()
                #print(self.encoder_L, self.encoder_R)
        else:
            self.set_motors(-speed, speed)
            while (self.encoder_L-self.encoder_R>target):
                self.get_encoders()
        self.stop_motors()

##########  SERVOS ########################################

    def set_servo1(self, pos):
        """
        Sets servo 1 to given position. Position ranges from 0...1
        """
        self._write_16(YOZH_REG_SERVO1, (int) (500+pos*2000))

    def set_servo2(self, pos):
        """
        Sets servo 2 to given position. Position ranges from 0...1
        """
        self._write_16(YOZH_REG_SERVO2, (int) (500+pos*2000))

##########  BUZZER ########################################
    def buzz(self, freq, dur=0.5):
        self.buzzer.freq(freq)            # set frequency
        self.buzzer.duty_u16(32768)       # set duty cycle, range 0-65535
        sleep(dur)
        self.buzzer.duty_u16(0)           # set duty cycle, range 0-65535
##########  IMU    ########################################
    def IMU_start(self):
        self._write_8(YOZH_REG_IMU_INIT, 1)
        self._yaw_offset = self._read_16(YOZH_REG_YAW)*0.1

    def IMU_calibrate(self):
        self._write_8(YOZH_REG_IMU_INIT, 2)
        sleep(1.0)
        while (self._read_8(YOZH_REG_IMU_STATUS)==2):
            pass
        self._yaw_offset = self._read_16(YOZH_REG_YAW)*0.1


    def IMU_stop(self):
        self._write_8(YOZH_REG_IMU_INIT, 0)

    def IMU_status(self):
        return(self._read_8(YOZH_REG_IMU_STATUS))

    def IMU_get_accel(self):
        accel=[0,0,0]
        self._read_16_array(YOZH_REG_ACCEL, accel)
        self.ax=accel[0]*aRes
        self.ay=accel[1]*aRes
        self.az=accel[2]*aRes

    def IMU_get_gyro(self):
        gyro=[0,0,0]
        self._read_16_array(YOZH_REG_GYRO, gyro)
        self.gx=gyro[0]*gRes
        self.gy=gyro[1]*gRes
        self.gz=gyro[2]*gRes

    def IMU_yaw_reset(self):
        self._yaw_offset = self._read_16(YOZH_REG_YAW)*0.1

    def IMU_yaw(self):
        yaw = self._read_16(YOZH_REG_YAW)*0.1 - self._yaw_offset
        if (yaw >180):
            yaw = yaw - 360
        elif (yaw < - 180 ):
            yaw = yaw + 360
        return(yaw)

    def IMU_pitch(self):
        return(self._read_16(YOZH_REG_PITCH)*0.1)

    def IMU_roll(self):
        return(self._read_16(YOZH_REG_ROLL)*0.1)

##########  LEDS   ########################################

    def set_led_L(self, color):
        """
        Sets color of left  LED.
        Color should be list of 3 values, R, G, B, each ranging 0...255
        e.g. color = [0,0,255]
        """
        self._write_8_array(YOZH_REG_NEOPIXEL_L, color)
    def set_led_R(self, color):
        """
        Sets color of right LED.
        Color should be list of 3 values, R, G, B, each ranging 0...255
        e.g. color = [0,0,255]
        """
        self._write_8_array(YOZH_REG_NEOPIXEL_R, bytes(color))

    def set_leds(self, color_l, color_r = None):
        """
        Sets color of both  LEDs.
        Each color should be list of 3 values, R, G, B, each ranging 0...255
        e.g. color = [0,0,255]
        """
        if color_r is None:
            color_r=color_l
        self._write_8_array(YOZH_REG_NEOPIXEL_L, bytes(color_l+color_r))

    def set_led_brightness(self, value):
        """
        Sets  LED brightness
        """
        self._write_8(YOZH_REG_NEOPIXEL_BRIGHTNESS, value)

##########  REFL. ARRAY  ########################################

    def linearray_on(self):
        """
        Turns the bottom line array of reflectance sensors ON
        """
        self._write_8(YOZH_REG_LINEARRAY_INIT, 1)


    def linearray_off(self):
        """
        Turns the bottom line array of reflectance sensors OFF
        """
        self._write_8(YOZH_REG_LINEARRAY_INIT, 0)

    def linearray_raw(self,i):
        """
        Returns the raw reading of i-th  of reflectance sensor, i=0...7
        """
        return self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)

    def linearray_cal(self,i):
        """
        Returns the scaled  reading of i-th  of reflectance sensor, i=0...7
        Results are scaled to be between 0...100
        White is 0, black is 100
        """
        raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        if (raw<self._calibrate_W):
            return(0.0)
        elif (raw>self._calibrate_B):
            return(100.0)
        else:
            return 100.0*(raw-self._calibrate_W)/(self._calibrate_B - self._calibrate_W)

    def calibrate(self):
        self.linearray_on()
        min=1023
        max=0
        for i in range (8):
            x=self.linearray_raw(i)
            if (x<min):
                min = x
            elif (x>max):
                max = x
        self._calibrate_B = max
        self._calibrate_W = min
        self._threshold = 0.5*(max+min)
        print(max, min)
        print("Calibration complete")
        print("The two values above should be about 900 and 100.")

    def sensor_on_white(self,i):
        """
        Is reflectance sensor i (i=0...7) on white?
        """
        raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        return(raw<self._threshold)

    def sensor_on_black(self,i):
        """
        Is reflectance sensor i (i=0...7) on black?
        """
        raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        return(raw>=self._threshold)

    def all_on_black(self):
        raw_values = [0]*8
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        on_black = True
        for i in range(8):
            if raw_values[i] <self._threshold:
                on_black = False
        return on_black       


    def line_position_white(self):
        """
        returns position of while line under the bot.
        """
        upper_bound=self._calibrate_B*0.8+self._calibrate_W*0.2
        lower_bound=self._calibrate_B*0.3+self._calibrate_W*0.7
        #print(lower_bound, upper_bound)
        spread=upper_bound-lower_bound
        raw_values = [0]*8
        position=0
        right=0.0
        left=0.0
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        i=0
        # count sensors on the right of the white line
        while (i<8) and (raw_values[i]>lower_bound):
            if (raw_values[i]>upper_bound):
                right+=1.0
            else:
                right+=1.0*(raw_values[i]-lower_bound)/spread
            i +=1
        #print(right, end=' ')
        if (i==8):
            # all sensors were on the right of the line!!!
            return(None)

        # now count sensors n the left of white line
        i=7
        while (i>=0) and (raw_values[i]>lower_bound):
            if (raw_values[i]>upper_bound):
                left+=1.0
            else:
                left+=1.0*(raw_values[i]-lower_bound)/spread
            i -=1
        #print(left)
        return(left-right)

    def line_position_black(self):
        """
        returns position of black line under the bot.
        """
        upper_bound=self._calibrate_B*0.7+self._calibrate_W*0.3
        lower_bound=self._calibrate_B*0.2+self._calibrate_W*0.8
        #print(lower_bound, upper_bound)
        spread=upper_bound-lower_bound
        raw_values = [0]*8
        position=0
        right=0.0
        left=0.0
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        i=0
        while (i<8) and (raw_values[i]<upper_bound):
            if (raw_values[i]<lower_bound):
                right+=1.0
            else:
                right+=1.0*(upper_bound-raw_values[i])/spread
            i +=1
        #print(right, end=' ')
        i=7
        while (i>=0) and (raw_values[i]<upper_bound):
            if (raw_values[i]<lower_bound):
                left+=1.0
            else:
                left+=1.0*(upper_bound-raw_values[i])/spread
            i -=1
        #print(left)
        return(left-right)


##########  DISPLAY  ########################################

    def clear_display(self):
        self._oled.fill_rect(0,0,128,64,0)
        self._oled.show()

    def set_text(self, text, line):
        lines = text.splitlines()
        i = 0
        for l in lines:
            if (i < 6):
                self._oled.text(l, 0, (line+i)*11)
            i+=1

        self._oled.show()



##########  I2C UTILITY  ########################################
    def _write_8(self, register, data):
        # Write 1 byte of data to the specified  register address.
        # Data MUST BE 1 byte
        self._i2c.writeto_mem(self._addr, register, bytes([data]) )

    def _write_8_array(self, register, data):
        # write an array of 1-byte  values  to specified register address
        # data MUST BE array of bytes
        self._i2c.writeto_mem(self._addr, register, data)


    def _write_16(self, register, data):
        # Write a 16-bit little endian value to the specified register
        # address.
        self._i2c.writeto_mem(self._addr, register, bytes([data & 0xFF,(data >> 8) & 0xFF]) )

    def _write_16_array(self, register, data):
        # write an array of littel endian 16-bit values  to specified register address
        l=len(data)
        buffer=bytearray(2*l)
        for i in range(l):
            buffer[2*i]=data[i] & 0xFF
            buffer[2*i+1]=(data[i]>>8) & 0xFF
        self._i2c.writeto_mem(self._addr, register, buffer)

    def _read_8(self, register):
        # Read and return a byte from  the specified register address.
        self._i2c.writeto(self._addr, bytes([register]))
        result = self._i2c.readfrom(self._addr, 1)
        return result[0]

    def _read_16(self, register):
        # Read and return a 16-bit signed little  endian value  from the
        # specified  register address.
        self._i2c.writeto(self._addr, bytes([register]))
        in_buffer = self._i2c.readfrom(self._addr, 2)
        raw =  (in_buffer[1] << 8) | in_buffer[0]
        if (raw & (1<<15)): # sign bit is set
            return (raw - (1<<16))
        else:
            return raw

    def _read_16_array(self, register, result_array):
        # Read and  saves into result_arrray a sequence of 16-bit little  endian
        # values  starting from the specified  register address.
        l=len(result_array)
        self._i2c.writeto(self._addr, bytes([register]))
        in_buffer = self._i2c.readfrom(self._addr, 2*l)
        for i in range(l):
            raw = (in_buffer[2*i+1] << 8) | in_buffer[2*i]
            if (raw & (1<<15)): # sign bit is set
                result_array[i] = (raw - (1<<16))
            else:
                result_array[i] = raw

    def _read_32(self, register):
        # Read and return a 32-bit signed little  endian value  from the
        # specified  register address.

        self._i2c.writeto(self._addr, bytes([register]))
        in_buffer = self._i2c.readfrom(self._addr, 4)
        raw = (in_buffer[3] << 24) |(in_buffer[2] << 16) | (in_buffer[1] << 8) | in_buffer[0]
        if (raw & (1<<31)): # sign bit is set
            return (raw - (1<<32))
        else:
            return raw

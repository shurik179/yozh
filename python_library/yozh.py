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

This is a CircuitPython library for Yozh robot.

* Author(s): Alexander Kirillov
* Version: 2.0
"""
import gc
import board
from adafruit_bus_device.i2c_device import I2CDevice
import time
import simpleio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_vl53l0x import VL53L0X

# now display-related things
import displayio
import adafruit_displayio_ssd1306
import terminalio
# from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.bitmap_label import Label
from adafruit_display_text import wrap_text_to_lines

YOZH_DEFAULT_I2C_ADDR        =const(0x11)
# buttons
YOZH_BUTTON_A   = DigitalInOut(board.D13)
YOZH_BUTTON_B   = DigitalInOut(board.D12)
# buzzer
YOZH_BUZZER     = board.D5
# distance sensors XSHUT pins
YOZH_XSHUT_L    = DigitalInOut(board.D7)  #XSHUT1=I1 - pin D7
YOZH_XSHUT_R    = DigitalInOut(board.D25) #XSHUT2=I2 - pin D25

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



class Yozh:

    def __init__(self, i2c=board.I2C(), oled=0x3C, address=YOZH_DEFAULT_I2C_ADDR, distance_sensors=True):
        self._device = I2CDevice(i2c, address)
        self._out_buffer = bytearray(16)
        self._in_buffer = bytearray(16)
        self.button_A=YOZH_BUTTON_A
        self.button_B=YOZH_BUTTON_B
        self.encoder_L = 0
        self.encoder_R = 0
        self.speed_L   = 0
        self.speed_R   = 0
        self._calibrate_W = 70   #reasonable defaults for black and white sensor readings
        self._calibrate_B = 950
        self._threshold = 500    # black/white threshold
        time.sleep(0.2)
        with self._device:
            result = bytearray(1)
            self._device.write(bytes([YOZH_REG_WHO_AM_I]))
            self._device.readinto(result)
            who_am_i = result[0]
        if who_am_i != YOZH_DEFAULT_I2C_ADDR:
            print(who_am_i);
            raise RuntimeError('Could not find Yozh Bot, is it connected and powered? ')
        else:
            print("Yozh bot initialized")
        # now initialize the display and buttons
        if oled is not None:
            displayio.release_displays()
            self._display_bus = displayio.I2CDisplay(i2c, device_address=oled)
            self.display = adafruit_displayio_ssd1306.SSD1306(self._display_bus, width=128, height=64)
            self.splash=displayio.Group()
            self.display.show(self.splash)
            self._fonts = {}
            self._textboxes = []

            # Draw a label
            self.add_textbox(text_position =(10,20), text_scale=2, text="Yozh")

        self.button_A.direction = Direction.INPUT
        self.button_A.pull = Pull.UP
        self.button_B.direction = Direction.INPUT
        self.button_B.pull = Pull.UP
        if distance_sensors:
            YOZH_XSHUT_L.switch_to_output(value=False) #turn off left
            YOZH_XSHUT_R.switch_to_output(value=True)  #turn on right
            # configure i2c address of right sensor
            self.distance_R = VL53L0X(i2c)
            self.distance_R.set_address(0x30)
            # now, turn on the left one as well; it iwll use default address of 0x29
            YOZH_XSHUT_L.value = True
            self.distance_L = VL53L0X(i2c)

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
        while (pin.value):
            pass

    def is_pressed(self, pin):
        return(not pin.value)

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
        simpleio.tone(YOZH_BUZZER, freq, duration=dur)


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
        self._write_8_array(YOZH_REG_NEOPIXEL_R, color)

    def set_leds(self, color_l, color_r = None):
        """
        Sets color of both  LEDs.
        Each color should be list of 3 values, R, G, B, each ranging 0...255
        e.g. color = [0,0,255]
        """
        if color_r is None:
            color_r=color_l
        self._write_8_array(YOZH_REG_NEOPIXEL_L, color_l+color_r)

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
        self._textboxes=[]
        N=len(self.splash)
        for i in range(N):
            self.splash.pop()
        gc.collect()

    def _load_font(self, font):
        """
        Load and cache a font if not previously loaded
        Return the key of the cached font
        :param font: Either terminalio.FONT or the path to the bdf font file
        """
        if font is terminalio.FONT:
            if "terminal" not in self._fonts:
                self._fonts["terminal"] = terminalio.FONT
            return "terminal"
        if font not in self._fonts:
            self._fonts[font] = bitmap_font.load_font(font)
        return font

    @staticmethod
    def wrap_nicely(string, max_chars):
        """A helper that will return a list of lines with word-break wrapping.
        :param str string: The text to be wrapped.
        :param int max_chars: The maximum number of characters on a line before wrapping.
        """
        return wrap_text_to_lines(string, max_chars)


    def add_textbox(
        self,
        text_position=(0, 0),
        text_font=terminalio.FONT,
        text_wrap=0,
        text_maxlen=0,
        text_scale=1,
        line_spacing=1.15,
        text_anchor_point=(0, 0),
        text=None,
    ):
        """
        Add text labels with settings
        :param str text_font: The path to your font file for your data text display.
        :param text_position: The position of your extracted text on the display in an (x, y) tuple.
                              Can be a list of tuples for when there's a list of json_paths, for
                              example.
        :param text_wrap: When non-zero, the maximum number of characters on each line before text
                          is wrapped. (for long text data chunks). Defaults to 0, no wrapping.
        :param text_maxlen: The max length of the text. If non-zero, it will be truncated to this
                            length. Defaults to 0.
        :param int text_scale: The factor to scale the default size of the text by
        :param float line_spacing: The factor to space the lines apart
        :param (float,float) text_anchor_point: Values between 0 and 1 to indicate where the text
                                                 position is relative to the label
        :param str text: If this is provided, it will set the initial text of the label.
        """
        if not self.display:
            return(-1)

        if not text_wrap:
            text_wrap = 0
        if not text_maxlen:
            text_maxlen = 0
        if not isinstance(text_scale, (int, float)) or text_scale < 1:
            text_scale = 1
        if not isinstance(text_anchor_point, (tuple, list)):
            text_anchor_point = (0, 0.5)
        if not 0 <= text_anchor_point[0] <= 1 or not 0 <= text_anchor_point[1] <= 1:
            raise ValueError("Text anchor point values should be between 0 and 1.")
        text_scale = round(text_scale)
        gc.collect()

        text_field = {
            "label": None,
            "font": self._load_font(text_font),
            "position": text_position,
            "wrap": text_wrap,
            "maxlen": text_maxlen,
            "scale": text_scale,
            "line_spacing": line_spacing,
            "anchor_point": text_anchor_point,
        }
        self._textboxes.append(text_field)

        text_index = len(self._textboxes) - 1
        if text is not None:
            self.set_text(text, text_index)

        return text_index


    def set_text(self, val, index=0):
        """Display text, with indexing into our list of text boxes.
        :param str val: The text to be displayed
        :param index: Defaults to 0.
        """
        if not self.display:
            return
        # Make sure at least a single label exists
        if not self._textboxes:
            self.add_textbox()
        string = str(val)
        if self._textboxes[index]["maxlen"] and len(string) > self._textboxes[index]["maxlen"]:
            # too long! shorten it
            if len(string) >= 3:
                string = string[: self._textboxes[index]["maxlen"] - 3] + "..."
            else:
                string = string[: self._textboxes[index]["maxlen"]]
        index_in_splash = None

        if len(string) > 0 and self._textboxes[index]["wrap"]:
            lines = self.wrap_nicely(string, self._textboxes[index]["wrap"])
            string = "\n".join(lines)

        if self._textboxes[index]["label"] is not None:
            index_in_splash = self.splash.index(self._textboxes[index]["label"])
        if len(string) > 0:
            if self._textboxes[index]["label"] is None:
                self._textboxes[index]["label"] = Label(
                    self._fonts[self._textboxes[index]["font"]],
                    text=string,
                    scale=self._textboxes[index]["scale"],
                )
                if index_in_splash is not None:
                    self.splash[index_in_splash] = self._textboxes[index]["label"]
                else:
                    self.splash.append(self._textboxes[index]["label"])
            else:
                self._textboxes[index]["label"].text = string
            self._textboxes[index]["label"].anchor_point = self._textboxes[index]["anchor_point"]
            self._textboxes[index]["label"].anchored_position = self._textboxes[index]["position"]
            self._textboxes[index]["label"].line_spacing = self._textboxes[index]["line_spacing"]
        elif index_in_splash is not None:
            self._textboxes[index]["label"] = None

        # Remove the label from splash
        if index_in_splash is not None and self._textboxes[index]["label"] is None:
            del self.splash[index_in_splash]
        gc.collect()



##########  I2C UTILITY  ########################################
    def _write_8(self, address, data):
        # Write 1 byte of data to the specified  register address.
        with self._device:
            self._device.write(bytes([address & 0xFF,
                                       data]))

    def _write_8_array(self, address, data):
        # write an array of bytes to specified register address
        self._out_buffer[0] = address & 0xFF
        l=len(data)
        for i in range(l):
            self._out_buffer[i+1]=data[i]& 0xFF
        with self._device:
            self._device.write(self._out_buffer,end=l+1)

    def _write_16(self, address, data):
        # Write a 16-bit little endian value to the specified register
        # address.
        with self._device:
            self._device.write(bytes([address & 0xFF,
                                      data & 0xFF,
                                      (data >> 8) & 0xFF]))

    def _write_16_array(self, address, data):
        # write an array of littel endian 16-bit values  to specified register address
        self._out_buffer[0] = address & 0xFF
        l=len(data)
        for i in range(l):
            self._out_buffer[2*i+1]=data[i] & 0xFF
            self._out_buffer[2*i+2]=(data[i]>>8) & 0xFF

        with self._device:
            self._device.write(self._out_buffer,end=2*l+1)

    def _read_8(self, address):
        # Read and return a byte from  the specified register address.
        with self._device:
            result = bytearray(1)
            self._device.write(bytes([address & 0xFF]))
            self._device.readinto(result)
            #self._device.write_then_readinto(bytes([address & 0xFF]),result)
            return result[0]

    def _read_16(self, address):
        # Read and return a 16-bit signed little  endian value  from the
        # specified  register address.
        with self._device:
            self._device.write(bytes([address & 0xFF]))
            self._device.readinto(self._in_buffer, end = 2)
            raw =  (self._in_buffer[1] << 8) | self._in_buffer[0]
            if (raw & (1<<15)): # sign bit is set
                return (raw - (1<<16))
            else:
                return raw

    def _read_16_array(self, address, result_array):
        # Read and  saves into result_arrray a sequence of 16-bit little  endian
        # values  starting from the specified  register address.
        # FIXME: signed
        count=len(result_array)
        with self._device:
            self._device.write(bytes([address & 0xFF]))
            self._device.readinto(self._in_buffer, end = 2*count)
            #self._device.write_then_readinto(bytes([address & 0xFF]),self._in_buffer,in_end = 2*count )
        for i in range(count):
            result_array[i]=self._in_buffer[2*i] |(self._in_buffer[2*i+1]<<8)

    def _read_32(self, address):
        # Read and return a 32-bit signed little  endian value  from the
        # specified  register address.
        with self._device:
            self._device.write(bytes([address & 0xFF]))
            self._device.readinto(self._in_buffer, end = 4)
            #self._device.write_then_readinto(bytes([address & 0xFF]),self._in_buffer, in_end = 4)
            raw = (self._in_buffer[3] << 24) | (self._in_buffer[2] << 16) | (self._in_buffer[1] << 8) | self._in_buffer[0]
            if (raw & (1<<31)): # sign bit is set
                return (raw - (1<<32))
            else:
                return raw

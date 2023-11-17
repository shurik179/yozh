# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
#
# SPDX-License-Identifier: MIT

"""
`yozh`
====================================================

This is a CircuitPython library for Yozh robot.

* Author(s): Alexander Kirillov
* Version: 4.0
"""
import gc
import board
from adafruit_bus_device.i2c_device import I2CDevice
import time
import simpleio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_vl53l0x import VL53L0X
import neopixel
import adafruit_max1704x

# now display-related things
import displayio
import terminalio
import adafruit_imageload
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font

# now our own regsiter definitions
from yozh_registers import *

# now, some colors
RED    = 0xFF0000
GREEN  = 0x00FF00
BLUE   = 0x0000FF
YELLOW = 0xFFFF00
WHITE  = 0xFFFFFF
BLACK  = 0x000000
OFF    = 0x000000

YOZH_DEFAULT_I2C_ADDR        =const(0x11)
# buttons
BUTTON_A   =  DigitalInOut(board.D2)
BUTTON_B   = DigitalInOut(board.D1)
BUTTON_C   = DigitalInOut(board.D0)
# buzzer
YOZH_BUZZER     = board.D13
#neopixel leds
YOZH_LEDS       = board.A0
#neopixel leds
YOZH_LIGHTS       = board.D12

# distance sensors XSHUT pins
YOZH_XSHUT_L    = DigitalInOut(board.D5)  #XSHUT1  pin D5
YOZH_XSHUT_R    = DigitalInOut(board.D11)  #XSHUT2 pin D11

# fonts
FONT_BATTERY = bitmap_font.load_font("fonts/battery-16.bdf")
FONT_SMALL = terminalio.FONT
FONT_REGULAR = bitmap_font.load_font("fonts/PTSans-Narrow-24.bdf")
FONT_BOLD = bitmap_font.load_font("fonts/PTSans-NarrowBold-32.bdf")
# LiPo battery monitor
monitor = adafruit_max1704x.MAX17048(board.I2C())


# imu constants
gRes = 500.0 / 32768.0   # gyro resolution, in (deg/s)/LSB
aRes = 2.0 / 32768.0     # accelerometer resolution, in g/LSB

# technical: constants for turns
CW = 1     #clockwise
CCW = - 1  #counterclockwise

# special value of distance for go_forward/backward command
UNLIMITED = -1


class Yozh:

    def __init__(self, address=YOZH_DEFAULT_I2C_ADDR, distance_sensors=True):
        self._out_buffer = bytearray(16)
        self._in_buffer = bytearray(16)
        # motors and encoders
        self.encoder_L = 0
        self.encoder_R = 0
        self.speed_L   = 0
        self.speed_R   = 0
        # IMU
        self.ax        = 0    #acceleration
        self.ay        = 0
        self.az        = 0
        self.gx        = 0    #gyro
        self.gy        = 0
        self.gz        = 0
        #Line array
        self._calibrate_W = [50,50,50,50,50,50,50]   #reasonable defaults for black and white sensor readings
        self._calibrate_B = [850,850,850,850,850,850,850]
        self._threshold = [450,450,450,450,450,450,450]    # black/white threshold
        # buttons
        BUTTON_A.direction = Direction.INPUT
        BUTTON_A.pull = Pull.DOWN
        BUTTON_B.direction = Direction.INPUT
        BUTTON_B.pull = Pull.DOWN
        BUTTON_C.direction = Direction.INPUT
        BUTTON_C.pull = Pull.UP
        #leds
        self._leds = neopixel.NeoPixel(YOZH_LEDS, 2, brightness=0.25, auto_write=True, pixel_order=neopixel.GRB)
        #headlights
        self._lights = neopixel.NeoPixel(YOZH_LIGHTS, 4, brightness=1.0, auto_write=True, pixel_order=neopixel.GRBW)

        # display
        self.display = board.DISPLAY
        self.display.rotation=180
        self.canvas=displayio.Group()
        self.display.show(self.canvas)
        self.display.auto_refresh=False
        self._charge_mode = False

        # other settings
        self.min_turn_power = 25 

        #############################################################################################
        # now that we have the definitions, let us put things on display and initilaize the slave MCU

        self.set_leds(GREEN)
        # put splash screen on display
        title=bitmap_label.Label(font = FONT_BOLD, text="YOZH", scale = 2, x=105, y=30)
        self.canvas.append(title)
        logo, palette = adafruit_imageload.load("/hedgehog.bmp",
                                                  bitmap=displayio.Bitmap,
                                                  palette=displayio.Palette)
        #redefine colors
        palette[0] = 0xFFFF80
        palette[1] = 0x000000
        # Create a TileGrid to hold the bitmap
        logo_tile_grid = displayio.TileGrid(logo, pixel_shader=palette)
        self.canvas.append(logo_tile_grid)
        self.display.refresh()
        if self.is_pressed(BUTTON_B):
            self._charge_mode = True
        # now, get firmware version and battery voltage

        # check that the slave MCU is available:
        self._device = I2CDevice(board.I2C(), address, probe = False)
        try:
            chipid = self._read_8(YOZH_REG_WHO_AM_I)
        except:
            chipid = 0
            board.I2C().unlock()
            print("Failed to find slave MCU")

        if chipid == 0 :
            self.canvas.append(bitmap_label.Label(font = FONT_BOLD, text="INIT FAILED", color = RED, scale = 1, x=100, y=82))
            self.display.refresh()
            #raise RuntimeError('Could not find Yozh Bot, is it connected and powered? ')
        else:
            self.IMU_start()
            self.canvas.append(bitmap_label.Label(font = FONT_REGULAR, text="Firmware: "+self.fw_version(), scale = 1, x=110, y=82))
            self.display.refresh()

        voltage_message="Battery:    {:.1f}V".format(monitor.cell_voltage)
        self.canvas.append(bitmap_label.Label(font = FONT_REGULAR, text=voltage_message, scale = 1, x=110, y=107))
        self.display.refresh()
        #load glyphs
        glyphs = (
            b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-_,.:?!'\n "
        )
        FONT_REGULAR.load_glyphs(glyphs)
        #FONT_BOLD.load_glyphs(glyphs)
        ##clear display
        del self.canvas[3]
        del self.canvas[2]
        del self.canvas[1]
        del self.canvas[0]
        self.display.refresh()
        #create battery info block
        self.battery_percent_label=bitmap_label.Label(font = terminalio.FONT, color = 0x00FF00, text="100%", scale = 1, x=190, y=8)
        self.battery_icon=bitmap_label.Label(font = FONT_BATTERY, text="P", scale = 1, x=217, y=7)
        self.canvas.append(self.battery_percent_label)
        self.canvas.append(self.battery_icon)
        #create text_lines
        #textlines = [bitmap_label.Label(font = FONT_BOLD, base_alignment=True, text="My title",  x=0, y=23)]
        self.textlines=[]
        for i in range(5):
            self.textlines.append(bitmap_label.Label(font = FONT_BOLD, base_alignment=True,  text="Mg", scale = 1, x=0, y=23+27*i))
        for i in range (5):
            self.textlines[i].text=""
            self.canvas.append(self.textlines[i])
        self.update_battery_display()


        YOZH_XSHUT_L.switch_to_output(value=False) #turn off left
        YOZH_XSHUT_R.switch_to_output(value=True)  #turn on right
        # configure i2c address of right sensor
        self.distance_R = VL53L0X(board.I2C())
        self.distance_R.set_address(0x30)
        # now, turn on the left one as well; it iwll use default address of 0x29
        YOZH_XSHUT_L.value = True
        self.distance_L = VL53L0X(board.I2C())


        # various constants
        self.CM_TO_TICKS = 150.0
        # basic configuration of PID - FIXME
        self.configure_PID(maxspeed=4200)
        self._pid = False
        self.linearray_off()
        self.angle_error = 0 #actual yaw - desired yaw, in degrees
        self._write_8(YOZH_REG_MOTOR_CONFIG, 3) # b00000011
        if self._charge_mode:
            self.charge_mode()
            
######## Firmware version
    def fw_version(self):
        """Returns firmware version as a string"""
        minor = self._read_8(YOZH_REG_FW_VERSION)
        major = self._read_8(YOZH_REG_FW_VERSION + 1)
        version="{}.{}"
        return(version.format(major,minor))

######## BATTERY LEVEL
    def battery_voltage(self):
        """Returns battery level, in volts"""
        return monitor.cell_voltage

    def battery_percent(self):
        """Returns battery charge, in percent"""
        return monitor.cell_percent

    def update_battery_display(self):
        percent = monitor.cell_percent
        self.battery_percent_label.text="{:.0f}%".format(percent)
        if (percent>90):
            self.battery_icon.text="M" #full
            color=0x00FF00 #green
        elif percent>65:
            self.battery_icon.text="N" #3/4 full
            color=0x00FF00 #green
        elif percent>40:
            self.battery_icon.text="O" #1/2 full
            color=0xFFFFFF #white
        elif percent>15:
            self.battery_icon.text="P" #1/4 full
            color=0xFFFF00 #yellow
        else:
            self.battery_icon.text="Q" #empty
            color=0xFF0000 #red
        self.battery_icon.color=color
        self.battery_percent_label.color = color
        self.display.refresh()

######## Charge mode
    def charge_mode(self):
        self.set_leds(OFF)
        self.clear_display()
        self.stop_motors()
        self.disable_servos()
        self.linearray_off()
        while True:
            self.update_battery_display()
            self.set_text(2, "Charging: {:.1f}%".format(self.battery_percent()), font = FONT_BOLD)
            time.sleep(10)
            self.set_text(2, " ")
            time.sleep(30)

##########  BUTTONS ########################################

    def wait_for(self,pin):
        if pin == BUTTON_C : # this pin (D0) is HIGH by default
            while (pin.value):
                pass
        else:
            while (not pin.value):
                pass

    def is_pressed(self, pin):
        if pin == BUTTON_C : # this pin is HIGH by default
                return(not pin.value)
        else:
                return(pin.value)

    def choose_button(self):
        while ( (not BUTTON_A.value)  and (not  BUTTON_B.value) and BUTTON_C.value ):
            pass
        if (BUTTON_A.value):
            # Button A was pressed
            return "A"
        elif (BUTTON_B.value):
            return "B"
        else:
            return "C"

##########  LEDS/HEADLIGHTS    ########################################
    def set_lights(self, power = 100):
        """
        Sets headlights on at given power (0..100)
        """
        brightness = (int) (power*2.54)
        self._lights.fill((0,0,0,brightness))

    def set_led_L(self, color):
        """
        Sets color of left  LED.
        Color should be tuple of 3 values, R, G, B, each ranging 0...255
        e.g. color = (0,0,255)
        or color = 0xFFFF00
        """
        self._leds[1] = color

    def set_led_R(self, color):
        """
        Sets color of right LED.
        Color should be tuple  of 3 values, R, G, B, each ranging 0...255
        e.g. color = (0,0,255)
        or color = 0xFFFF00
        """
        self._leds[0] = color

    def set_leds(self, color_l, color_r = None):
        """
        Sets color of both  LEDs.
        Each color should be tuple of 3 values, R, G, B, each ranging 0...255
        e.g. color = (0,0,255)
        or color = 0xFFFF00
        """
        if color_r is None:
            color_r=color_l
        self._leds[0] = color_r
        self._leds[1] = color_l

##########  DISPLAY  ########################################

    def clear_display(self,hide_battery = False):
        for t in self.textlines:
            t.text = ""
        if hide_battery:
            self.battery_icon.text=""
            self.battery_percent.text=""
        self.display.refresh()

    def set_text(self, line_number, message, font = FONT_REGULAR, color = WHITE):
        """Display text, with indexing into our list of text boxes.
           :param index: Defaults to 0.
           :param str message: The text to be displayed
        """
        lines = str(message).splitlines()
        num_lines = min(5-line_number,len(lines))
        #print(num_lines)
        for i in range(num_lines):
            self.textlines[i+line_number].text=lines[i]
            self.textlines[i+line_number].color=color
            self.textlines[i+line_number].font=font
        self.display.refresh()

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
        self._write_8(YOZH_REG_MOTOR_MODE, 0x00)
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
            Kp = 0.05 # 1 degree deviation = 5% correction
            Ti = 100 #make large, to effectively disabel integral term
            Td = 0.00
            Ilim = 1000
        data = [round(maxspeed), round(Kp*1000), round(Ti*1000), round (Td*1000), round(Ilim)]
        self._write_16_array(YOZH_REG_MAX_SPEED, data)

##########  DRIVING ########################################

    def go_forward(self, distance, speed=60, correct_error = False):
        self.reset_encoders()
        if correct_error:
            heading  = self.normalize(self.IMU_yaw()-self.angle_error)
        else:
            heading = self.IMU_yaw()
        #print(direction)
        self._write_16(YOZH_REG_DIRECTION, (int) (heading*10) )
        self._write_8(YOZH_REG_MOTOR_MODE, 0x01)
        self.set_motors(speed, speed)
        if distance == UNLIMITED:
            return()

        target = self.CM_TO_TICKS * distance # travel for given number of  cm
        while (self.encoder_L+self.encoder_R<target):
            self.get_encoders()
        self.stop_motors()
        self.angle_error = 0

    def distance_traveled(self):
        self.get_encoders()
        return ((self.encoder_L+self.encoder_R)/self.CM_TO_TICKS)

    def go_backward(self, distance, speed=60):
        self.reset_encoders()
        self._write_8(YOZH_REG_MOTOR_MODE, 0x01)
        self.set_motors(-speed, -speed)
        target = -self.CM_TO_TICKS * distance # travel for given number of  cm
        while (self.encoder_L+self.encoder_R>target):
            self.get_encoders()
        self.stop_motors()
        # restore old motor mode  setting
        self._write_8(YOZH_REG_MOTOR_MODE, 0x00)

    def turn_to(self, heading, direction, speed=50):
        target_yaw = self.normalize(heading)
        if direction == CW:
            sign = 1
        else:
            sign = -1
        self.set_motors(sign*speed, -sign*speed)
        diff=90 # just a random positive number
        while (diff > 10): 
            diff = self.angle_diff(self.IMU_yaw(),target_yaw, direction)
        # when we are close, let's slow down to 25% speed
        self.set_motors(sign*self.min_turn_power, -sign*self.min_turn_power)
        while (diff > 1  and  diff <355): #subtract 2 degrees to account for robot not stopping instantly
            #print(diff)
            diff = self.angle_diff(self.IMU_yaw(),target_yaw, direction)
        self.stop_motors()
        error = self.normalize(self.IMU_yaw()- target_yaw)
        self.angle_error = error


    def turn(self, angle, speed=50):
        start_yaw = self.IMU_yaw()
        target_yaw = start_yaw + angle
        #print("turn ",angle)
        #print(start_yaw)
        if angle>0:
            self.turn_to(target_yaw, CW, speed)
        else:
            self.turn_to(target_yaw, CCW, speed)


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

    def disable_servos(self):
        self._write_16(YOZH_REG_SERVO1, 0)
        self._write_16(YOZH_REG_SERVO2, 0)

##########  BUZZER ########################################
    def buzz(self, freq, dur=0.5):
        simpleio.tone(YOZH_BUZZER, freq, duration=dur)

##########  IMU    ########################################
    def IMU_start(self):
        self._write_8(YOZH_REG_IMU_INIT, 1)
        #time.sleep(1.0)

    def IMU_calibrate(self):
        self._write_8(YOZH_REG_IMU_INIT, 2)
        time.sleep(5.0)
        while (self._read_8(YOZH_REG_IMU_STATUS)==2):
            time.sleep(0.5)

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

    def IMU_yaw(self):
        yaw = self._read_16(YOZH_REG_YAW)*0.1
        if (yaw >180):
            yaw = yaw - 360
        elif (yaw < - 180 ):
            yaw = yaw + 360
        return(yaw)

    def IMU_pitch(self):
        return(self._read_16(YOZH_REG_PITCH)*0.1)

    def IMU_roll(self):
        return(self._read_16(YOZH_REG_ROLL)*0.1)

    def angle_diff(self, angle1, angle2, direction = CW):
        """
        returns angle difference between two angles, measured in a given direction.
        Each angle should be between -180 and 180
        Alwasy returns a number between 0 and 360
        E.g. if angle1 = 5, angle2= 30, dir = clockwise, returns 25
             if angle1 = 5, angle2= -10, dir = clockwise, returns 345
             if angle1 = 5, angle2= 30, dir = counterclockwise, returns 335
             if angle1 = 5, angle2= -10, dir = counterclockwise, returns 15

        """
        if direction == CW:
            if angle2 >angle1:
                return (angle2 - angle1)
            else:
                return (angle2 +360 - angle1)
        else:
            if angle2<angle1:
                return (angle1-angle2)
            else:
                return (angle1 +360 -angle2)

    def normalize(self, angle):
        while angle >180:
            angle = angle - 360
        while angle <=-180:
            angle = angle + 360
        return(angle)

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
        Returns the raw reading of i-th  of reflectance sensor, i=0...6
        """
        return self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)

    def linearray_cal(self,i, raw = None):
        """
        Returns the scaled  reading of i-th  of reflectance sensor, i=0...6
        Results are scaled to be between 0...100
        White is 0, black is 100
        Last argument is the raw reading; normally it is omitted, so the program requests it
        """
        if raw is None:
            raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        if (raw<self._calibrate_W[i]):
            return(0.0)
        elif (raw>self._calibrate_B[i]):
            return(100.0)
        else:
            return 100.0*(raw-self._calibrate_W[i])/(self._calibrate_B[i] - self._calibrate_W[i])

    def calibrate(self):
        self.linearray_on()
        for i in range (7):
                self._calibrate_B[i]=self.linearray_raw(i)
                self._threshold[i] = 0.5*(self._calibrate_B[i]+self._calibrate_W[i])
        #print(max, min)
        print("Calibration complete. Black values are below:")
        for i in range (7):
            print(self._calibrate_B[i])

    def sensor_on_white(self,i):
        """
        Is reflectance sensor i (i=0...6) on white?
        """
        raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        return(raw<self._threshold[i])

    def sensor_on_black(self,i):
        """
        Is reflectance sensor i (i=0...6) on black?
        """
        raw = self._read_16(YOZH_REG_LINEARRAY_RAW+2*i)
        return(raw>=self._threshold[i])

    def all_on_black(self):
        """
        Are all sensors on black?
        """
        raw_values = [0]*7
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        for i in range(7):
            if raw_values[i]<self._threshold[i]:
                return False
        return True

    def all_on_white(self):
        """
        Are all sensors on white?
        """
        raw_values = [0]*7
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        for i in range(7):
            if raw_values[i]>self._threshold[i]:
                return False
        return True

    def line_position_white(self):
        """
        returns position of while line under the bot.
        """
        #get raw values
        raw_values = [0]*7
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        position=0
        right=0.0
        left=0.0
        i=1
        # count sensors on the right of the white line
        for i in range (1,6):
            x = raw_values[i]
            if x>self._threshold[i]:
                right +=1
            else:
                right += self.linearray_cal(i,x)*0.01
                break
        if right == 5:
            # no line found
            return(None)


        #print(right, end=' ')
        # now count sensors n the left of white line
        for j in range (1,6):
            i=6-j # as j ranges 1 through 5, i will range 5 to 1
            x = raw_values[i]
            if x>self._threshold[i]:
                left +=1
            else:
                left  += self.linearray_cal(i,x)*0.01
                break
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
        raw_values = [0]*7
        position=0
        right=0.0
        left=0.0
        self._read_16_array(YOZH_REG_LINEARRAY_RAW, raw_values)
        i=0
        while (i<7) and (raw_values[i]<upper_bound):
            if (raw_values[i]<lower_bound):
                right+=1.0
            else:
                right+=1.0*(upper_bound-raw_values[i])/spread
            i +=1
        #print(right, end=' ')
        i=6
        while (i>=0) and (raw_values[i]<upper_bound):
            if (raw_values[i]<lower_bound):
                left+=1.0
            else:
                left+=1.0*(upper_bound-raw_values[i])/spread
            i -=1
        #print(left)
        return(left-right)

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
            raw=self._in_buffer[2*i] |(self._in_buffer[2*i+1]<<8)
            if (raw & (1<<15)): # sign bit is set
                result_array[i] = (raw - (1<<16))
            else:
                result_array[i] = raw

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


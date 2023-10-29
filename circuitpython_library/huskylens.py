# SPDX-FileCopyrightText: Copyright 2021-2023 Alexander Kirillov <shurik179@gmail.com>
#
# SPDX-License-Identifier: MIT
#

# main reference:
# https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md
# Huskylens Wiki:
# https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336

import time
import board
from adafruit_bus_device.i2c_device import I2CDevice


# return codes
COMMAND_RETURN_INFO      = 0x29
COMMAND_RETURN_OK        = 0x2E
COMMAND_RETURN_BUSY      = 0x3D
COMMAND_RETURN_NEED_PRO  = 0x3E
COMMAND_RETURN_IS_PRO    = 0x3B

# functions (aka algorithms)
FACE_RECOGNITION      = 0x00
OBJECT_TRACKING       = 0x01
OBJECT_RECOGNITION    = 0x02
LINE_TRACKING         = 0x03
COLOR_RECOGNITION     = 0x04
TAG_RECOGNITION       = 0x05
OBJECT_CLASSIFICATION = 0x06

# object types
TYPE_BLOCK            = 0x2A
TYPE_ARROW            = 0x2B

class Block:
    def __init__(self, frame):
        self.type = frame[4];
        if self.type == TYPE_BLOCK:
            # Block
            self.x = (frame[6]<<8) | frame[5]
            self.y = (frame[8]<<8) | frame[7]
            self.width = (frame[10]<<8) | frame[9]
            self.height = (frame[12]<<8) | frame[11]
            self.ID = (frame[14]<<8) | frame[13]
        elif self.type == TYPE_ARROW:
            # Arrow
            self.x0 = (frame[6]<<8) | frame[5]
            self.y0 = (frame[8]<<8) | frame[7]
            self.x1 = (frame[10]<<8) | frame[9]
            self.y1 = (frame[12]<<8) | frame[7]
            self.ID = (frame[14]<<8) | frame[13]

class Huskylens:
    def __init__(self, i2c=board.I2C()):
        self.device = I2CDevice(i2c, 0x32)
        # temporary buffers for storing outgoing and incoming frames
        self.out_buffer = bytearray(26)
        self.out_buffer[0]=0x55
        self.out_buffer[1]=0xAA
        self.out_buffer[2]=0x11
        self.in_buffer = bytearray(26)
        # variables for recording received responses
        self.response    = 0x00   # received command
        self.numLearned  = 0      # number of objects learned by HuskyLens
        self.numReceived = 0      # number of received blocks/arrows
        self.receivedObjects = [] # list of received blocks/arrows, each an object of type Block

    def _getFrame(self):
        with self.device:
            self.device.readinto(self.in_buffer, end=5)
            self.device.readinto(self.in_buffer, start=5, end=self.in_buffer[3]+6)




    def send(self, cmd, data = None):
        """
        Send a specified command (with optional data)
        to HuskyLens, using the protocol described in
        https://github.com/HuskyLens/HUSKYLENSArduino/blob/master/HUSKYLENS%20Protocol.md
        and immediately reads the response
        """
        # clear previously received data
        self.response = 0x00
        self.numReceived = 0
        self.receivedObjects.clear()
        if data is None:
            data_length = 0
        else:
            data_length=len(data)
        #construct command frame in buffer. Bytes 0-2 have already been set
        self.out_buffer[3]=data_length & 0xFF
        self.out_buffer[4]=cmd
        if data is not None:
            self.out_buffer[5:5+data_length]=data
        #now, compute checksum
        checksum=0
        for i in range(5+data_length):
            checksum += self.out_buffer[i]
        #take the low byte
        self.out_buffer[5+data_length]=checksum & 0xFF
        #now, write it using i2c and immediately read 5 bytes of response
        with self.device:
            self.device.write_then_readinto(self.out_buffer, self.in_buffer, out_end=6+data_length, in_end=5)
            # use received data to determine length of the frame and read the rest of it
            self.device.readinto(self.in_buffer, start=5, end=self.in_buffer[3]+6)
        #process the received frame and if necessary, get remaining frames
        self._processResponse()


    def _processResponse(self):
        self.response=self.in_buffer[4]
        if self.response == 0x29:
            # COMMAND_RESPONSE_INFO
            numObjects = ( self.in_buffer[6]<<8 )| self.in_buffer[5]
            self.numLearned = ( self.in_buffer[8]<<8 )| self.in_buffer[7]
            for i in range (numObjects):
                self._getFrame()
                self.receivedObjects.append(Block(self.in_buffer))
            self.numReceived = len(self.receivedObjects)


    def ping(self):
        """
        Checks connection. Returns True on success, False otherwise.
        """
        self.send(0x2C) # COMMAND_REQUEST_KNOCK
        return (self.response == COMMAND_RETURN_OK)


    def setFunction(self,function):
        data = bytearray([function & 0xFF, 0x00])
        self.send(0x2D, data) # COMMAND_REQUEST_ALGORITHM

    def getObjects(self, ID = None ):
        """
        Get all identified blocks/arrows seen by HuskyLens
        at this moment(including those
        not yet learned, with ID = 0).
        Saves the objects in self.receivedObjects list
        and returns number of detected objects.
        If ID is provided, only returns objects with given ID
        """
        if ID is None:
            self.send(0x20) #COMMAND_REQUEST
        else:
            data = bytearray([ID&0xFF, (ID>>8)&0xFF])
            self.send(0x26, data) #COMMAND_REQUEST_BY_ID
        return(self.numReceived)

    def getLearned(self):
        """
        Returns the number of objects HuskyLens has learned
        for the current function.
        """
        self.getObjects()
        return(self.numLearned)

    def saveToCard(self, fileNum):
        """
        Saves the learned model (for current function!)
        to SD card as file
        functionName_Backup_fileNum.conf
        """
        data =  bytearray([fileNum&0xFF, (fileNum>>8)&0xFF])
        self.send(0x32, data)
        return (self.response == COMMAND_RETURN_OK)

    def loadFromCard(self, fileNum):
        """
        Load a model file for current function from the SD Card
        The loaded file will be the following format
        functionName_Backup_fileNum.conf
        """
        data =  bytearray([fileNum&0xFF, (fileNum>>8)&0xFF])
        self.send(0x33, data)
        return (self.response == COMMAND_RETURN_OK)


    def setCustomName(self, ID, name):
        """
        Sets custom name (up to 20 chars) for learned object
        with given ID. This name will be used by Huskylens UI:
        e.g. instead of 'Face1:ID1', it will show 'Jack:ID1'
        """

        data = bytearray ([(ID&0xFF), (len(name)+1)&0xFF])
        data +=name.encode()
        data.append(0x00)
        self.send(0x2F, data) # COMMAND_REQUEST_CUSTOMNAMES

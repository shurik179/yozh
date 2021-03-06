/*



  Copyright (c) 2014-2015 Arduino LLC.  All right reserved.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  See the GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#ifndef _VARIANT_YOZH_
#define _VARIANT_YOZH_

// The definitions here needs a SAMD core >=1.6.10
#define ARDUINO_SAMD_VARIANT_COMPLIANCE 10610

/*----------------------------------------------------------------------------
 *        Definitions
 *----------------------------------------------------------------------------*/

/** Frequency of the board main oscillator */
#define VARIANT_MAINOSC		(32768ul)

/** Master clock frequency */
#define VARIANT_MCK			  (48000000ul)

/*----------------------------------------------------------------------------
 *        Headers
 *----------------------------------------------------------------------------*/

#include "WVariant.h"

#ifdef __cplusplus
#include "SERCOM.h"
#include "Uart.h"
#endif // __cplusplus

#ifdef __cplusplus
extern "C"
{
#endif // __cplusplus

/*----------------------------------------------------------------------------
 *        Pins
 *----------------------------------------------------------------------------*/

// Number of pins defined in PinDescription array
#define PINS_COUNT           (28u)
#define NUM_DIGITAL_PINS     (17u)
#define NUM_ANALOG_INPUTS    (9u)
#define NUM_ANALOG_OUTPUTS   (0u)
#define analogInputToDigitalPin(p)  ((p < 9u) ? (p) : -1)

#define digitalPinToPort(P)        ( &(PORT->Group[g_APinDescription[P].ulPort]) )
#define digitalPinToBitMask(P)     ( 1 << g_APinDescription[P].ulPin )
//#define analogInPinToBit(P)        ( )
#define portOutputRegister(port)   ( &(port->OUT.reg) )
#define portInputRegister(port)    ( &(port->IN.reg) )
#define portModeRegister(port)     ( &(port->DIR.reg) )
#define digitalPinHasPWM(P)        ( g_APinDescription[P].ulPWMChannel != NOT_ON_PWM || g_APinDescription[P].ulTCChannel != NOT_ON_TIMER )

/*
 * digitalPinToTimer(..) is AVR-specific and is not defined for SAMD
 * architecture. If you need to check if a pin supports PWM you must
 * use digitalPinHasPWM(..).
 *
 * https://github.com/arduino/Arduino/issues/1833
 */
// #define digitalPinToTimer(P)


/*
 * Pin definitions
 */
 #define PIN_VSENSE    (0ul)

//there is no pin A0, but it is used as an offset in wiring_analog.c in core....
#define PIN_A0         (0ul)
#define PIN_A1         (1ul)
#define PIN_A2         (2ul)
#define PIN_A3         (3ul)
#define PIN_A4         (4ul)
#define PIN_A5         (5ul)
#define PIN_A6         (6ul)
#define PIN_A7         (7ul)
#define PIN_A8         (8ul)

static const uint8_t A0  = PIN_A0;
static const uint8_t A1  = PIN_A1;
static const uint8_t A2  = PIN_A2;
static const uint8_t A3  = PIN_A3;
static const uint8_t A4  = PIN_A4;
static const uint8_t A5  = PIN_A5;
static const uint8_t A6  = PIN_A6 ;
static const uint8_t A7  = PIN_A7 ;
static const uint8_t A8  = PIN_A8 ;



#define PIN_SERVO1       (10ul)
#define PIN_SERVO2       (9ul)


#define PIN_ENC1_DIR     (15ul)
#define PIN_ENC1_SPEED   (16ul)
#define PIN_MOTOR1A      (17ul)
#define PIN_MOTOR1B      (18ul)

#define PIN_ENC2_DIR     (19ul)
#define PIN_ENC2_SPEED   (20ul)
#define PIN_MOTOR2A      (22ul)
#define PIN_MOTOR2B      (21ul)

#define PIN_ANALOG_CTRL  (25ul)


#define PIN_NEOPIXEL     (26ul)

// dummy
#define PIN_DAC0         (27ul)


/*
 * Serial interfaces
 */


/*
 * SPI Interfaces
 */
#define SPI_INTERFACES_COUNT 0

/*
 * Wire Interfaces
 */
#define WIRE_INTERFACES_COUNT 2
//wire: connection to ItsyBitsy; Yozh is a slave on this bus
#define PIN_WIRE_SDA             (11ul)
#define PIN_WIRE_SCL             (12ul)
#define PERIPH_WIRE              sercom2
#define WIRE_IT_HANDLER          SERCOM2_Handler
//wire1: connection to IMU; Yozh is a master on this bus
#define PIN_WIRE1_SDA            (13ul)
#define PIN_WIRE1_SCL            (14ul)
#define PERIPH_WIRE1             sercom1
#define WIRE1_IT_HANDLER         SERCOM1_Handler


/*
 * USB
 */
#define PIN_USB_DM          (23ul)
#define PIN_USB_DP          (24ul)
//fake - in fact, host enable pin is not connected
#define PIN_USB_HOST_ENABLE (27ul)
/*
 * I2S Interfaces
 */
#define I2S_INTERFACES_COUNT 0


#ifdef __cplusplus
}
#endif

/*----------------------------------------------------------------------------
 *        Arduino objects - C++ only
 *----------------------------------------------------------------------------*/

#ifdef __cplusplus

/*	=========================
 *	===== SERCOM DEFINITION
 *	=========================
*/
extern SERCOM sercom0;
extern SERCOM sercom1;
extern SERCOM sercom2;
extern SERCOM sercom3;
extern SERCOM sercom4;
extern SERCOM sercom5;


#endif

// These serial port names are intended to allow libraries and architecture-neutral
// sketches to automatically default to the correct port name for a particular type
// of use.  For example, a GPS module would normally connect to SERIAL_PORT_HARDWARE_OPEN,
// the first hardware serial port whose RX/TX pins are not dedicated to another use.
//
// SERIAL_PORT_MONITOR        Port which normally prints to the Arduino Serial Monitor
//
// SERIAL_PORT_USBVIRTUAL     Port which is USB virtual serial
//
// SERIAL_PORT_LINUXBRIDGE    Port which connects to a Linux system via Bridge library
//
// SERIAL_PORT_HARDWARE       Hardware serial port, physical RX & TX pins.
//
// SERIAL_PORT_HARDWARE_OPEN  Hardware serial ports which are open for use.  Their RX & TX
//                            pins are NOT connected to anything by default.
#define SERIAL_PORT_USBVIRTUAL      Serial
#define SERIAL_PORT_MONITOR         Serial
// Serial has no physical pins broken out, so it's not listed as HARDWARE port
//#define SERIAL_PORT_HARDWARE        Serial1
//#define SERIAL_PORT_HARDWARE_OPEN   Serial1

#endif /* _VARIANT_YOZH_ */

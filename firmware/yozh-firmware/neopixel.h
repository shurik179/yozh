#ifndef _YOZH_NEOPIXEL_H
#define _YOZH_NEOPIXEL_H
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#define RED    0x00FF0000
#define GREEN  0x0000FF00
#define BLUE   0x000000FF
#define YELLOW 0x00FFFF00
#define OFF    0x00000000
#define RGBcolor(R,G,B) ((R<<16)|(G<<8)|B)
void pixelBegin();
void pixelUpdateConfig();
void pixelUpdate();
#endif

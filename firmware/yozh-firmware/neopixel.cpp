#include "regmap.h"
#include "neopixel.h"

Adafruit_NeoPixel pixels(2, PIN_NEOPIXEL, NEO_GRB); //two pixels

void pixelBegin(){
    pixels.begin();
    pixels.setBrightness(*neopixelBrightness);
    pixels.setPixelColor(0,GREEN);
    pixels.setPixelColor(1,GREEN);
    pixels.show();
}

void pixelUpdateConfig(){
    pixels.setBrightness(*neopixelBrightness);
    pixels.show();
}

void pixelUpdate(){
    pixels.setPixelColor(0, RGBcolor(neopixelColors[0],neopixelColors[1],neopixelColors[2] ));
    pixels.setPixelColor(1, RGBcolor(neopixelColors[3],neopixelColors[4],neopixelColors[5] ));
    pixels.show();
}

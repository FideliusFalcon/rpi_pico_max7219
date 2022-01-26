from sys import platform
import max7219
from machine import Pin, SPI, freq
from time import sleep
import gc
from print_error import print_error  # Optional print of error codes
# Import all implemented classes
from nec import NEC_8, NEC_16
from sony import SONY_12, SONY_15, SONY_20
from philips import RC5_IR, RC6_M0
from mce import MCE

# Define pin according to platform
p = Pin(15, Pin.IN)


class matrix():
    def __init__(self):
        self.MAX7219_NUM = 1
        self.MAX7219_INVERT = False
#        self.MAX7219_SCROLL_DELAY = 0.15
        self.MAX7219_SCROLL_DELAY = 25
        cs_pin = 5
        self.LECTURE = ""
        self.VISIBLE = "Ceci"

        spi = SPI(0)
        self.display = max7219.Matrix8x8(spi=spi, cs=Pin(cs_pin), num=self.MAX7219_NUM)
        self.display.brightness(2)
    
    def text_scroll(self):
        p = self.MAX7219_NUM * 8
        for p in range(self.MAX7219_NUM * 8, len(self.VISIBLE) * -8 - 1, -1):
            self.display.fill(self.MAX7219_INVERT)
            self.display.text(self.VISIBLE, p, 1, not self.MAX7219_INVERT)
            self.display.show()
            sleep(self.MAX7219_SCROLL_DELAY)
    def text_fixe(self):
        self.display.fill(self.MAX7219_INVERT)
        self.display.text(self.VISIBLE, 0, 1, not self.MAX7219_INVERT)
        self.display.show()
    def affiche(self):
        if self.MAX7219_SCROLL_DELAY > 20:
            self.text_fixe()
        else:
            self.text_scroll()
    def ir_rcv(self, data):
        if data == "FIN":
            self.VISIBLE = self.LECTURE
            self.LECTURE = ""
        if data == "Defilement":                    #Touche "Pause"
            self.LECTURE = ""
            if self.MAX7219_SCROLL_DELAY > 10:
                self.MAX7219_SCROLL_DELAY = 0.15
            else:
                self.MAX7219_SCROLL_DELAY = 25
        if data == "+":                             #Touche "+"
            self.MAX7219_SCROLL_DELAY = self.MAX7219_SCROLL_DELAY * 0.8
            self.LECTURE = ""
        if data == "-":                             #Touche "-"
            self.MAX7219_SCROLL_DELAY = self.MAX7219_SCROLL_DELAY * 1.25
            self.LECTURE = ""
        else:
            self.LECTURE = self.LECTURE + data

# User callback
def cb(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        val = str('{:02x}'.format(data))
        switch={
            '16':'0',
            '0c':'1',
            '18':'2',
            '5e':'3',
            '08':'4',
            '1c':'5',
            '5a':'6',
            '42':'7',
            '52':'8',
            '4a':'9',
            '19':'FIN',        #button 'twisted arrows' used as "Enter" to apply the changes and display new text
            '0d':'USB',
            '07':'EQ',
            '15':'-',          #button - used to decelerate the scrolling
            '09':'+',          #button + used to accelerate the scrolling
            '44':'Pause',
            '40':'Recule',
            '43':'Avance',
            '45':'ON/OFF',      #button ON/OFF used to turn the panel OFF
            '46':'Defilement',  #buttun Mode used for stop/start the scrolling
            '47':'Sourdine'     #button MUTE
            }
        led.ir_rcv(switch.get(val, "Rien"))

#Objects definitions
led = matrix()
classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE)
ir = classes[0](p, cb)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

try:
    while True:
        gc.collect()
        led.affiche()
#        if valeurLue != "Rien" and valeurLue != None:
#            print(valeurLue)
except KeyboardInterrupt:
    ir.close()
    print("Fin du test")

